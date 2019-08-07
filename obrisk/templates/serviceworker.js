// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "obrisk-pwa-v" + new Date().getTime();
var filesToCache = [
  '/',
];

// Cache on install
self.addEventListener("install", event => {
  this.skipWaiting();
  console.log('installing pwa');
  event.waitUntil(
    caches.open(staticCacheName)
    .then(cache => {
      return cache.addAll(filesToCache);
    })
  )
});

// Clear cache on activate
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      console.log('activating pwa')
      return Promise.all(
        cacheNames
        .filter(cacheName => (cacheName.startsWith("obrisk-pwa-v")))
        .filter(cacheName => (cacheName !== staticCacheName))
        .map(cacheName => caches.delete(cacheName))
      );
    })
  );
});

// Serve from Cache
self.addEventListener('fetch', function (e) {
  console.log('served from cache ' + e.request.url);
  e.respondWith(
    caches.match(e.request).then(function (response) {
      return response || fetch(e.request);
    })
  );
});

self.addEventListener('beforeinstallprompt', (e) => {
  // Prevent Chrome 76 and later from showing the mini-infobar
  e.preventDefault();
  // Stash the event so it can be triggered later.
  deferredPrompt = e;
  console.log('ask to install')
});
