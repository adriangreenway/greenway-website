import { createServer } from 'node:http';
import { access, readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const host = '127.0.0.1';
const port = Number(process.env.PORT || 4178);
const root = resolve(fileURLToPath(new URL('./site/', import.meta.url)));

const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.mp3': 'audio/mpeg',
  '.png': 'image/png'
};

async function existingFile(pathname) {
  const relative = normalize(decodeURIComponent(pathname)).replace(/^[/\\]+/, '');
  const base = resolve(root, relative);
  if (!base.startsWith(root)) return null;
  const candidates = pathname.endsWith('/')
    ? [join(base, 'index.html')]
    : extname(base)
      ? [base]
      : [base + '.html', join(base, 'index.html')];
  for (const candidate of candidates) {
    try {
      await access(candidate);
      if ((await stat(candidate)).isFile()) return candidate;
    } catch {}
  }
  return null;
}

createServer(async (request, response) => {
  try {
    const url = new URL(request.url || '/', `http://${host}:${port}`);
    const file = await existingFile(url.pathname);
    if (!file) {
      response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end('Not found');
      return;
    }
    const headers = {
      'Content-Type': contentTypes[extname(file)] || 'application/octet-stream',
      'Cache-Control': file.endsWith('sw.js') ? 'no-cache' : 'no-store',
      'X-Content-Type-Options': 'nosniff'
    };
    response.writeHead(200, headers);
    response.end(await readFile(file));
  } catch {
    response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Preview server error');
  }
}).listen(port, host, () => {
  console.log(`Preview: http://${host}:${port}/cassiday/10-03-26/`);
});
