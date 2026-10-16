const CACHE_NAME = 'entrenador-shell-v1';
const BASE_URL = new URL('./', self.registration.scope);
const APP_SHELL = new URL('./', BASE_URL).href;
const ASSETS = [
  APP_SHELL,
  new URL('./index.html', BASE_URL).href,
  new URL('./manifest.webmanifest', BASE_URL).href,
  new URL('./icon.svg', BASE_URL).href
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key.startsWith('entrenador-shell-') && key !== CACHE_NAME)
        .map(key => caches.delete(key))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET' || new URL(request.url).origin !== self.location.origin) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    try {
      const response = await fetch(request);
      if (response.ok) await cache.put(request, response.clone());
      return response;
    } catch {
      const cached = await cache.match(request);
      if (cached) return cached;
      if (request.mode === 'navigate') return (await cache.match(APP_SHELL)) || Response.error();
      return Response.error();
    }
  })());
});
