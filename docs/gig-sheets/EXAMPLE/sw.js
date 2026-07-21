const CACHE = 'gig-ditta-v1';

// Core pages — small, must all cache (atomic). These make the site work offline.
const CORE = [
  '/',
  '/index.html',
  '/band.html',
  '/gig.html',
  '/mc.html',
  '/listen.html',
  '/manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(CORE))
  );
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
