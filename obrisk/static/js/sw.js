
self.addEventListener('install', e => {
 e.waitUntil(
   // after the service worker is installed,
   // open a new cache
   caches.open('my-pwa-cache').then(cache => {
     // add all URLs of resources we want to cache
     return cache.addAll([
       '/',
       '/phone_signup.html',
       '/login.html',
       '/classified_list.html',
       '/stories_list.html',
       '/question_list.html',
       '/contact_list.html',
       '/images/doggo.jpg',
       '/styles/obrisk.css',
       '/scripts/obrisk.js',
     ]);
   })
 );
});