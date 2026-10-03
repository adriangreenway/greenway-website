// Live clock shared memory for gig sheets. One tiny record per wedding:
// which schedule row Adrian marked as "now" and when. Band phones poll it.
// Spec: docs/gig-sheets/LIVE_CLOCK_PLAN.md. Ship steps: README.md next to this file.
//
//   GET  /.netlify/functions/clock?w=/hess/10-03-26/          -> {row, at, set} or {}
//   POST same path, Authorization: Bearer <GIG_CLOCK_KEY>,
//        body {"row": 8, "at": 1788655200000}  or  {"reset": true}
//
// The key lives only in the Netlify site env var GIG_CLOCK_KEY and in 1Password
// ("Greenway Gig Clock Key"). Never in this file, the pages, or the docs.

import { getStore } from '@netlify/blobs';
import { timingSafeEqual } from 'node:crypto';

const WEDDING = /^\/[a-z-]+\/\d\d-\d\d-\d\d\/$/;
const DAY = 86400000;
const HEADERS = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'x-robots-tag': 'noindex, nofollow',
  'x-content-type-options': 'nosniff',
};

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: HEADERS });

function authorized(req) {
  const key = process.env.GIG_CLOCK_KEY || '';
  const auth = req.headers.get('authorization') || '';
  const given = auth.startsWith('Bearer ') ? auth.slice(7) : '';
  if (!key || !given || given.length !== key.length) return false;
  return timingSafeEqual(Buffer.from(given), Buffer.from(key));
}

export default async (req) => {
  const w = new URL(req.url).searchParams.get('w') || '';
  if (!WEDDING.test(w)) return json(400, { error: 'bad wedding path' });

  // Blob keys may not start with a slash: '/hess/10-03-26/' is stored as 'hess/10-03-26'.
  const blobKey = w.replace(/^\/|\/$/g, '');
  const store = getStore({ name: 'gig-clock', consistency: 'strong' });

  if (req.method === 'GET') {
    const v = await store.get(blobKey, { type: 'json' });
    return json(200, v && typeof v === 'object' ? v : {});
  }
  if (req.method !== 'POST') return json(405, { error: 'method not allowed' });
  if (!authorized(req)) return json(401, { error: 'unauthorized' });

  let body;
  try {
    const text = await req.text();
    if (text.length > 200) return json(413, { error: 'too large' });
    body = JSON.parse(text);
  } catch {
    return json(400, { error: 'bad json' });
  }

  if (body && body.reset === true) {
    await store.delete(blobKey);
    return json(200, {});
  }
  const row = body && body.row;
  const at = body && body.at;
  if (!Number.isInteger(row) || row < 0 || row > 200 || !Number.isFinite(at) || Math.abs(at - Date.now()) > DAY) {
    return json(400, { error: 'bad body' });
  }
  const v = { row, at, set: Date.now() };
  await store.setJSON(blobKey, v);
  return json(200, v);
};
