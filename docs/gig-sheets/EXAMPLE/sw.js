const CACHE = 'gig-ditta-v2';

// Core pages — small, must all cache (atomic). These make the site work offline.
const CORE = [
  '/',
  '/index.html',
  // Netlify rewrites internal .html links to these extensionless paths.
  '/band',
  '/band.html',
  '/gig',
  '/gig.html',
  '/mc',
  '/mc.html',
  '/listen',
  '/listen.html',
  '/manifest.json'
];

async function cacheFreshCore() {
  const fresh = await Promise.all(
    CORE.map(async path => {
      const response = await fetch(path, { cache: 'reload' });
      if (!response.ok) {
        throw new Error(`Unable to cache ${path}: ${response.status}`);
      }
      return [path, response];
    })
  );

  const cache = await caches.open(CACHE);
  await Promise.all(fresh.map(([path, response]) => cache.put(path, response)));
}

self.addEventListener('install', e => {
  e.waitUntil(cacheFreshCore());
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached =>
      cached || fetch(e.request).catch(() =>
        // offline + not cached: fall back to the landing page for navigations
        e.request.mode === 'navigate' ? caches.match('/index.html') : Response.error()
      )
    )
  );
});
