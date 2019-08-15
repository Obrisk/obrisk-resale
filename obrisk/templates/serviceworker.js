importScripts('https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js');


//Show debug logs in console
workbox.setConfig({
  debug: true
});

//Urls to prefetch
workbox.precaching.precacheAndRoute([

  '/static/js/aliyun-oss.min.js',
  '/static/js/bootbox.min.js',
  '/static/js/bootstrap.min.js',
  '/static/js/html5shiv.min.js',
  '/static/js/post-uploader.js',
  '/static/js/infinite.min.js',
  '/static/js/jquery.min.js',
  '/static/js/jquery.waypoints.min.js',
  '/static/js/listing.js',
  '/static/js/messager.js',
  '/static/js/obrisk.js',
  '/static/js/photoswipe-ui-default.min.js',
  '/static/js/photoswipe.min.js',
  '/static/js/popper.min.js',
  '/static/js/posts.js',
  '/static/js/qa.js',
  '/static/js/stories.js',
  '/static/js/swiper.min.js',
  '/static/js/uploader.js',
  '/static/js/user-form.js',
  '/static/js/websocketbridge.js',

  ///CSS cache
  '/static/css/bootstrap.css.map',
  '/static/css/bootstrap.min.css',
  '/static/css/bootstrap-grid.min.css',
  '/static/css/bootstrap-grid.min.css.map',
  '/static/css/bootstrap-reboot.min.css',
  '/static/css/bootstrap-reboot.min.css.map',
  '/static/css/classified-create.css',
  '/static/css/classified-details.css',
  '/static/css/classifieds.css',
  '/static/css/classifieds-list.css',
  '/static/css/colors.css',
  '/static/css/creative.css',
  '/static/css/default-skin.min.css',
  '/static/css/listing.css',
  '/static/css/login.css',
  '/static/css/messager.css',
  '/static/css/nav.css',
  '/static/css/notifications.css',
  '/static/css/obrisk.css',
  '/static/css/photoswipe.min.css',
  '/static/css/post-create.css',
  '/static/css/post-details.css',
  '/static/css/post-list.css',
  '/static/css/post-update.css',
  '/static/css/qa.css',
  '/static/css/stories.css',
  '/static/css/swiper.min.css',
  '/static/css/uploader.css',
  '/static/css/user_form.css',
  '/static/css/user_list.css',
  '/static/css/user_profile.css',
  '/static/css/util.css',

  //Image cache
  '/static/img/ajax-loader.gif',
  '/static/img/android-chrome-192x192.png',
  '/static/img/android-chrome-512x512.png',
  '/static/img/apple-touch-icon.png',
  '/static/img/bg.png',
  '/static/img/browserconfig.xml',
  '/static/img/chat.png',
  '/static/img/classifieds.png',
  '/static/img/default-skin.png',
  '/static/img/default-skin.svg',
  '/static/img/fail.png',
  '/static/img/favicon.ico',
  '/static/img/favicon.png',
  '/static/img/favicon-16x16.png',
  '/static/img/favicon-32x32.png',
  '/static/img/full-logo.png',
  '/static/img/header.jpg',
  '/static/img/icons.png',
  '/static/img/image.png',
  '/static/img/Jcrop.gif',
  '/static/img/loading.gif',
  '/static/img/logo.svg',
  '/static/img/mstile-144x144.png',
  '/static/img/mstile-150x150.png',
  '/static/img/mstile-310x150.png',
  '/static/img/mstile-310x310.png',
  '/static/img/mstile-70x70.png',
  '/static/img/posts.png',
  '/static/img/progress.png',
  '/static/img/safari-pinned-tab.svg',
  '/static/img/stories.png',
  '/static/img/success.png',
  '/static/img/user.png',
]);

// This will cache only the images loaded from https://obrisks.com/ all other images handle using CDN caching
// https://developers.google.com/web/tools/workbox/modules/workbox-strategies#cache_first_cache_falling_back_to_network
// https://developers.google.com/web/tools/workbox/modules/workbox-cache-expiration

workbox.routing.registerRoute(
  /\.(?:jpeg|webp|png|gif|jpg|svg)$/,
  // Whenever the app requests images, the service worker checks the
  // cache first for the resource before going to the network.
  workbox.strategies.cacheFirst({
    cacheName: 'obrisk-images-cache',
    // A maximum of 60 entries will be kept (automatically removing older
    // images) and these files will expire in 30 days.
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      })
    ]
  })
);


// JS files cache only the JS files loaded from https://obrisks.com/ all other images handle using CDN Caching
// https://developers.google.com/web/tools/workbox/modules/workbox-strategies#cache_first_cache_falling_back_to_network
// https://developers.google.com/web/tools/workbox/modules/workbox-cache-expiration
workbox.routing.registerRoute(
  /\.(?:js)$/,
  workbox.strategies.cacheFirst({
    cacheName: 'obrisk-js-cache',
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 60,
        maxAgeSeconds: 24 * 60 * 60, // 24 hours
      })
    ]
  })
);

// CSS files cache only the CSS files loaded from https://obrisks.com/ all other images handle using CDN Caching
// https://developers.google.com/web/tools/workbox/modules/workbox-strategies#cache_first_cache_falling_back_to_network
// https://developers.google.com/web/tools/workbox/modules/workbox-cache-expiration
workbox.routing.registerRoute(
  /\.(?:css)$/,
  workbox.strategies.cacheFirst({
    cacheName: 'obrisk-css-cache',
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 60,
        maxAgeSeconds: 24 * 60 * 60, // 24 hours
      })
    ]
  })
);

//CDN image cache 
workbox.routing.registerRoute(
  new RegExp('^https://obrisk.oss-cn-hangzhou.aliyuncs.com/static/img'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'CDN-img-cache'
  }),
);