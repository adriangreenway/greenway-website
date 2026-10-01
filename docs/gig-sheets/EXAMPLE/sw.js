const CACHE = 'gig-blick-09-05-26-v10';
const PREFIX = 'gig-blick-09-05-26-';
const BASE = '/blick/09-05-26/';

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
  BASE + 'manifest.json',
  BASE + 'band-sheet.pdf',
  BASE + 'gig-sheet.pdf',
  BASE + 'mc-cue-sheet.pdf',
  BASE + 'mc-cue-slides.pdf'
];

const AUDIO = [
  BASE + 'audio/cant-take-my-eyes-off-you.mp3',
  BASE + 'audio/the-way-i-love-you.mp3',
  BASE + 'audio/isnt-she-lovely.mp3',
  BASE + 'audio/you-never-even-called-me-by-my-name.mp3',
  BASE + 'audio/9-to-5.mp3',
  BASE + 'audio/dance-her-home.mp3',
  BASE + 'audio/me-and-my-kind.mp3'
];

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
  // Only the small core files block the upgrade; big MP3s download in the background.
  event.waitUntil(cacheFreshCore());
  cacheAudio();
  self.skipWaiting();
});

self.addEventListener('activate',event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    const old = keys.filter(key => key.startsWith(PREFIX) && key !== CACHE);
    await Promise.all(old.map(key => caches.delete(key)));
    await self.clients.claim();
    // An upgrade from an older version: refresh any open pages so nobody sees stale content.
    if(old.length){
      const open = await self.clients.matchAll({type:'window'});
      open.forEach(client => client.navigate(client.url).catch(() => {}));
    }
  })());
});

self.addEventListener('fetch',event => {
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).catch(() => {
    return event.request.mode === 'navigate' ? caches.match(BASE + 'index.html') : Response.error();
  })));
});
