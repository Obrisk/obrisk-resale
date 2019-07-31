
self.addEventListener('install', e => {
 e.waitUntil(
   // after the service worker is installed,
   // open a new cache
   caches.open('my-pwa-cache').then(cache => {
     // add all URLs of resources we want to cache
     return cache.addAll([
       '/',
       '../../templates/account/phone_signup.html',
       '../../templates/account/login.html',
       '../../templates/classifieds/classified_list.html',
       '../../templates/stories/stories_list.html',
       '../../templates/qa/question_list.html',
       '../../templates/messager/contact_list.html',
       '../img/.jpg',
       '../css/obrisk.css',
       './obrisk.js',
     ]);
   })
 );
});