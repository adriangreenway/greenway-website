const CACHE = 'gig-cassiday-10-03-26-v2';
const PREFIX = 'gig-cassiday-10-03-26-';
const BASE = '/cassiday/10-03-26/';

const CORE = [
  BASE,
  BASE + 'index.html',
  BASE + 'band',
  BASE + 'band.html',
  BASE + 'gig',
  BASE + 'gig.html',
  BASE + 'mc',
  BASE + 'mc.html',
  BASE + 'listen',
  BASE + 'listen.html',
  BASE + 'manifest.json'
];

const AUDIO = [];

async function cacheFreshCore(){
  const fresh = await Promise.all(CORE.map(async path => {
    const response = await fetch(path,{cache:'reload'});
    if(!response.ok) throw new Error('Unable to cache ' + path + ': ' + response.status);
    return [path,response];
  }));
  const cache = await caches.open(CACHE);
  await Promise.all(fresh.map(([path,response]) => cache.put(path,response)));
}

async function cacheAudio(){
  const cache = await caches.open(CACHE);
  await Promise.allSettled(AUDIO.map(path => fetch(path,{cache:'reload'}).then(response => {
    if(!response.ok) throw new Error('Unable to cache ' + path);
    return cache.put(path,response);
  })));
}

self.addEventListener('install',event => {
  event.waitUntil(Promise.all([cacheFreshCore(),cacheAudio()]));
  self.skipWaiting();
});

self.addEventListener('activate',event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(
    keys.filter(key => key.startsWith(PREFIX) && key !== CACHE).map(key => caches.delete(key))
  )));
  self.clients.claim();
});

self.addEventListener('fetch',event => {
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).catch(() => {
    return event.request.mode === 'navigate' ? caches.match(BASE + 'index.html') : Response.error();
  })));
});
