//To be able to skip and use the new service worker no matter what
importScripts("/static/js/workbox-v4.3.1/workbox-sw.js");
workbox.setConfig({
  modulePathPrefix: "/static/js/workbox-v4.3.1"
});
//Show debug logs in console
workbox.setConfig({
  debug: true
});

workbox.core.skipWaiting();

workbox.precaching.precacheAndRoute([
  {
    "url": "/static/css/account.css",
    "revision": "a338cc2e6f9c6c794eefab13aaf5e27d"
  },
  {
    "url": "/static/css/bootstrap-grid.min.css",
    "revision": "8997ec71a78ea4b0da89935276f4188b"
  },
  {
    "url": "/static/css/bootstrap-reboot.min.css",
    "revision": "1acc02b102fc1f6d4117be1726fb367e"
  },
  {
    "url": "/static/css/bootstrap.min.css",
    "revision": "416bb9e03b223eba66e9a3ca5a9da02e"
  },
  {
    "url": "/static/css/classified-create.css",
    "revision": "36ff5e54c3dbe754c7cad54a70e7a95d"
  },
  {
    "url": "/static/css/classified-details.css",
    "revision": "2708ccf0e952bc019b6d50d710f418fe"
  },
  {
    "url": "/static/css/classifieds-list.css",
    "revision": "cec2e8e8ab59042b170e2e5cf9040bf9"
  },
  {
    "url": "/static/css/classifieds.css",
    "revision": "c41e616083ae2619b9d8a7415b4ff216"
  },
  {
    "url": "/static/css/colors.css",
    "revision": "b6cba400eb0aacf7c0d85b6c0f9857ef"
  },
  {
    "url": "/static/css/creative.css",
    "revision": "5cd67ce3d1f423fd48826070dbf9be22"
  },
  {
    "url": "/static/css/default-skin.min.css",
    "revision": "96370330bb378f42b33670a7df03b9d5"
  },
  {
    "url": "/static/css/fancybox.css",
    "revision": "6115baf335801b1b85a34c0d48980eab"
  },
  {
    "url": "/static/css/listing.css",
    "revision": "82cb2d0cc455218a5e35998a5aea27e9"
  },
  {
    "url": "/static/css/login.css",
    "revision": "8c4d9b9bd82b0b7f5585e64eabce9904"
  },
  {
    "url": "/static/css/messager.css",
    "revision": "20d9a8af50df07dbb699c8bd77d03493"
  },
  {
    "url": "/static/css/nav.css",
    "revision": "91c02adec6b1594dbfd10defa276e4a3"
  },
  {
    "url": "/static/css/notifications.css",
    "revision": "c8c9b0217b4580c04d00c9a4aeaf2fe3"
  },
  {
    "url": "/static/css/obrisk.css",
    "revision": "50c4768839f18fbc036e1552c1fcc0e3"
  },
  {
    "url": "/static/css/photoswipe.min.css",
    "revision": "7a55d43eef1b6fe6def95b70be9d742a"
  },
  {
    "url": "/static/css/post-create.css",
    "revision": "157e23707df89649711ee7f70c470827"
  },
  {
    "url": "/static/css/post-details.css",
    "revision": "edda765773a08e81941634042fd3abed"
  },
  {
    "url": "/static/css/post-list.css",
    "revision": "dfc48eec859e06ac42fd91b0a12e31fc"
  },
  {
    "url": "/static/css/post-update.css",
    "revision": "157e23707df89649711ee7f70c470827"
  },
  {
    "url": "/static/css/preloader.gif",
    "revision": "4cc848b538580780aa52b50a7a18e1fa"
  },
  {
    "url": "/static/css/qa.css",
    "revision": "ddd3af46392bc5e6c808ab15ff48ee28"
  },
  {
    "url": "/static/css/stories.css",
    "revision": "9611d940a8a8dc29d5dd2d31ee518bb6"
  },
  {
    "url": "/static/css/swiper.min.css",
    "revision": "e7827ef3b92ce9040ca473de65143402"
  },
  {
    "url": "/static/css/uploader.css",
    "revision": "1d458c31550be3ca07bae49ade351ddd"
  },
  {
    "url": "/static/css/user_form.css",
    "revision": "d3fb601fcd0b620277abdd4411c86e77"
  },
  {
    "url": "/static/css/user_list.css",
    "revision": "a7964db0a6c7c440706cb810ab16cde5"
  },
  {
    "url": "/static/css/user_profile.css",
    "revision": "186c1b0ab492621c780def7434879ab5"
  },
  {
    "url": "/static/css/util.css",
    "revision": "9cabf2d2ce5a30ae04a9a78140e4b73e"
  },
  {
    "url": "/static/fonts/font-awesome-4.7.0/css/font-awesome.css",
    "revision": "9a3bd468dfed15febd11a01cb96dd38f"
  },
  {
    "url": "/static/fonts/font-awesome-4.7.0/css/font-awesome.min.css",
    "revision": "b5bc723666dd5b1462ea526587683e80"
  },
  {
    "url": "/static/fonts/Linearicons-Free-v1.0.0/icon-font.min.css",
    "revision": "94bcf8939dee79dd4259c0cc53cfb277"
  },
  {
    "url": "/static/img/ajax-loader.gif",
    "revision": "04836c514aea7d3d203112128be81fd6"
  },
  {
    "url": "/static/img/android-chrome-192x192.png",
    "revision": "ae983dcc3af212bed08135b5b4d11453"
  },
  {
    "url": "/static/img/android-chrome-512x512.png",
    "revision": "f57745291a6c047439b3d043197e8127"
  },
  {
    "url": "/static/img/apple-touch-icon.png",
    "revision": "1c5c1abbc872720ce794f9c4f44640fa"
  },
  {
    "url": "/static/img/bg.png",
    "revision": "8ddad23ce6dcc70bf111b23ae022f10c"
  },
  {
    "url": "/static/img/chat.png",
    "revision": "8f5c8adde80552dcee822ee1150b1510"
  },
  {
    "url": "/static/img/classifieds.png",
    "revision": "6b934496a3aecb6bfeb239f5905f1b89"
  },
  {
    "url": "/static/img/default-skin.png",
    "revision": "e3f799c6dec9af194c86decdf7392405"
  },
  {
    "url": "/static/img/fail.png",
    "revision": "73ab155b19feeae09ac49d58b95fbbf4"
  },
  {
    "url": "/static/img/favicon-16x16.png",
    "revision": "1d70a0ee61f983a28b1a848a6b1351c7"
  },
  {
    "url": "/static/img/favicon-32x32.png",
    "revision": "6a4d0322b9de2b04a4b45121e40db341"
  },
  {
    "url": "/static/img/favicon.ico",
    "revision": "85951f58526369d3779209a1594dd16e"
  },
  {
    "url": "/static/img/favicon.png",
    "revision": "32df020bf3cf44d3f5f70ab72af802e1"
  },
  {
    "url": "/static/img/full-logo.png",
    "revision": "a13a4dc172f8d57764ee034d622dbc6c"
  },
  {
    "url": "/static/img/header.jpg",
    "revision": "4022b04bd355362d9479bd9815f8618f"
  },
  {
    "url": "/static/img/icons.png",
    "revision": "c9ceb83c0a247ae47f54c3e1d3cb4bac"
  },
  {
    "url": "/static/img/image.png",
    "revision": "6b00566e6a7a54df0b83fe8a1d8b9427"
  },
  {
    "url": "/static/img/Jcrop.gif",
    "revision": "7a4b4c6ebdb549fcbe47408f9457493e"
  },
  {
    "url": "/static/img/loading.gif",
    "revision": "387d69b4eb5cdf1e050cc89cc20b5f5c"
  },
  {
    "url": "/static/img/mstile-144x144.png",
    "revision": "2d4e642f0d7326b53f4f878cf098852d"
  },
  {
    "url": "/static/img/mstile-150x150.png",
    "revision": "4a8ef4624beca0e213045d529e3a5541"
  },
  {
    "url": "/static/img/mstile-310x150.png",
    "revision": "0a52d55732dfb5985c55b29c6c513904"
  },
  {
    "url": "/static/img/mstile-310x310.png",
    "revision": "910cddbab01324d910257ece02e4719d"
  },
  {
    "url": "/static/img/mstile-70x70.png",
    "revision": "fd1ee0bd91da9f0aa6a423f957e63565"
  },
  {
    "url": "/static/img/posts.png",
    "revision": "02e998427ad52fe984c93562ba91bc54"
  },
  {
    "url": "/static/img/progress.png",
    "revision": "46732e763f50c337fecabcc42150d842"
  },
  {
    "url": "/static/img/splashscreens/ipad_splash.png",
    "revision": "df7171a93c5a2ab28d4011270552d2de"
  },
  {
    "url": "/static/img/splashscreens/ipadpro1_splash.png",
    "revision": "46a7dc1cb23a7a27eb3e971c14a10a4b"
  },
  {
    "url": "/static/img/splashscreens/ipadpro2_splash.png",
    "revision": "c223af204360e620fca989ed7be2c320"
  },
  {
    "url": "/static/img/splashscreens/ipadpro3_splash.png",
    "revision": "33863983c6e16f1444a0835ccf52dd4d"
  },
  {
    "url": "/static/img/splashscreens/iphone5_splash.png",
    "revision": "5f3497cea1628ec2dd1a5f01e6c9ebaa"
  },
  {
    "url": "/static/img/splashscreens/iphone6_splash.png",
    "revision": "54d184fd4a2077605b92b8969ef61881"
  },
  {
    "url": "/static/img/splashscreens/iphoneplus_splash.png",
    "revision": "2ff520b9ccab49ae3c5fb3a6e97497eb"
  },
  {
    "url": "/static/img/splashscreens/iphonex_splash.png",
    "revision": "814b71a601c8d9e5dee7c8fb8ba833a8"
  },
  {
    "url": "/static/img/splashscreens/iphonexr_splash.png",
    "revision": "007b1bb0e8e02cd12cd24ca17787f9e6"
  },
  {
    "url": "/static/img/splashscreens/iphonexsmax_splash.png",
    "revision": "a34f53814d16ee3a7aae497f09f32eee"
  },
  {
    "url": "/static/img/stories.png",
    "revision": "311cc8f7984fa5abe449be93e0b996ad"
  },
  {
    "url": "/static/img/success.png",
    "revision": "b80425bbf53402d499d54c86ca365870"
  },
  {
    "url": "/static/img/user.png",
    "revision": "6aadcee86193ab8e487ec40871a206ce"
  },
  {
    "url": "/static/js/aliyun-oss.min.js",
    "revision": "394d956eca3bc1d64e6b5a06d539fe94"
  },
  {
    "url": "/static/js/bootbox.min.js",
    "revision": "d70a2050eeddbd0476d757e7eb21d2b8"
  },
  {
    "url": "/static/js/bootstrap.min.js",
    "revision": "d061ab58270e692309b728296e90bba2"
  },
  {
    "url": "/static/js/browser-md5.js",
    "revision": "005d7aca45591ad4203f12ea12712ea6"
  },
  {
    "url": "/static/js/fancybox.min.js",
    "revision": "d6d71ddf529188fb35a2bc65efdca539"
  },
  {
    "url": "/static/js/html5shiv.min.js",
    "revision": "7b7a4e3a218061d489d18edc20018200"
  },
  {
    "url": "/static/js/imageClient.js",
    "revision": "4ab948f26be9ea5a0ce149e6f2b1022c"
  },
  {
    "url": "/static/js/infinite.min.js",
    "revision": "aeb9a96458b2d0c7bb3a6b95f220779a"
  },
  {
    "url": "/static/js/jquery.min.js",
    "revision": "a46fb81762396b7bf2020774a2fb4d9e"
  },
  {
    "url": "/static/js/jquery.waypoints.min.js",
    "revision": "cebc34dedef229a98275955df75e20e5"
  },
  {
    "url": "/static/js/listing.js",
    "revision": "464391cc6d6f4dc59d4a7052b70bff94"
  },
  {
    "url": "/static/js/location.js",
    "revision": "1a27a7150aefee3a045965bfd5272631"
  },
  {
    "url": "/static/js/messager.js",
    "revision": "d71e17e583aa6bbc60bc0fdaa9a776fd"
  },
  {
    "url": "/static/js/moment.min.js",
    "revision": "761502841c035afcf6a9bdc5d0a20d11"
  },
  {
    "url": "/static/js/notif-sw.js",
    "revision": "38d1cb8689e33c694cc8ff6139b1790f"
  },
  {
    "url": "/static/js/obrisk.js",
    "revision": "ec8cfa2606bbad1b8106d867da490ab5"
  },
  {
    "url": "/static/js/photoswipe-ui-default.min.js",
    "revision": "8e606a5f652bf3d96b48f5b426001885"
  },
  {
    "url": "/static/js/photoswipe.min.js",
    "revision": "c260bce75dabf9ffef99b5d743638db5"
  },
  {
    "url": "/static/js/popper.min.js",
    "revision": "354e13e7651ee5d25b68e43282911d33"
  },
  {
    "url": "/static/js/post-uploader.js",
    "revision": "d299ce34ae034e1b780b8696b636943d"
  },
  {
    "url": "/static/js/posts.js",
    "revision": "9991ed072b6ba3fb5e4ea8f96d40eebf"
  },
  {
    "url": "/static/js/profile-uploader.js",
    "revision": "7c63b99426e49c72f1262c9ddd73b1e3"
  },
  {
    "url": "/static/js/qa.js",
    "revision": "de517f44c5974b93e7b984f0570dbf15"
  },
  {
    "url": "/static/js/stories.js",
    "revision": "97df19f569dc7642b4d88d15031f90c4"
  },
  {
    "url": "/static/js/swiper.min.js",
    "revision": "d1dc6e2f65902bdfeaf88c9ef20254e0"
  },
  {
    "url": "/static/js/toast-msg.js",
    "revision": "af82356c546778cbdf17b6f9ae8b79d7"
  },
  {
    "url": "/static/js/uploader.js",
    "revision": "01f65ab229686eed300ee89b3c5c4afd"
  },
  {
    "url": "/static/js/user-form.js",
    "revision": "d3f581eb5d8717367088e752be2c57d8"
  },
  {
    "url": "/static/js/websocketbridge.js",
    "revision": "cdf4bd9dbfc48c91b2869b8f15fcb25c"
  },
  {
    "url": "/static/webpush/webpush.js",
    "revision": "c0e497b590f7058fa9cd8d0225e2eed1"
  }
]);


// This will cache only the images loaded from https://obrisks.com/ all other images handle using CDN caching
// https://developers.google.com/web/tools/workbox/modules/workbox-strategies#cache_first_cache_falling_back_to_network
// https://developers.google.com/web/tools/workbox/modules/workbox-cache-expiration
workbox.routing.registerRoute(
  /\.(?:jpeg|webp|png|gif|jpg|svg)/,
  // Whenever the app requests images, the service worker checks the
  // cache first for the resource before going to the network.
  new workbox.strategies.CacheFirst({
    cacheName: "obrisk-images-cache",
    // A maximum of 60 entries will be kept (automatically removing older
    // images) and these files will expire in 30 days.
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
      })
    ]
  })
);

// JS files cache only the JS files loaded from https://obrisks.com/ all other images handle using CDN Caching
// https://developers.google.com/web/tools/workbox/modules/workbox-strategies#cache_first_cache_falling_back_to_network
// https://developers.google.com/web/tools/workbox/modules/workbox-cache-expiration
workbox.routing.registerRoute(
  /\.(?:js)/,
  new workbox.strategies.CacheFirst({
    cacheName: "obrisk-js-cache",
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 60,
        maxAgeSeconds: 24 * 60 * 60 // 24 hours
      })
    ]
  })
);

// CSS files cache only the CSS files loaded from https://obrisks.com/ all other images handle using CDN Caching
// https://developers.google.com/web/tools/workbox/modules/workbox-strategies#cache_first_cache_falling_back_to_network
// https://developers.google.com/web/tools/workbox/modules/workbox-cache-expiration
workbox.routing.registerRoute(
  /\.(?:css)/,
  new workbox.strategies.CacheFirst({
    cacheName: "obrisk-css-cache",
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 60,
        maxAgeSeconds: 24 * 60 * 60 // 24 hours
      })
    ]
  })
);

// Font files cache only the fonts files loaded from https://obrisks.com/ all other images handle using CDN Caching
// https://developers.google.com/web/tools/workbox/modules/workbox-strategies#cache_first_cache_falling_back_to_network
// https://developers.google.com/web/tools/workbox/modules/workbox-cache-expiration
workbox.routing.registerRoute(
  /\.(?:woff2|ttf)/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "obrisk-font-cache",
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 60,
        maxAgeSeconds: 24 * 60 * 60 // 24 hours
      })
    ]
  })
);
workbox.routing.registerRoute(
  new RegExp("^https://fonts.googleapis.com/"),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "obrisk-font-cache"
  })
);

//CDN image cache
workbox.routing.registerRoute(
  new RegExp("^https://obrisk.oss-cn-hangzhou.aliyuncs.com/classifieds/"),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "CDN-img-cache"
  })
);
workbox.routing.registerRoute(
  new RegExp("^https://obrisk.oss-cn-hangzhou.aliyuncs.com/static/img"),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "CDN-img-cache"
  })
);
workbox.routing.registerRoute(
  new RegExp("^https://obrisk.oss-cn-hangzhou.aliyuncs.com/media/profile_pics"),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "CDN-img-cache"
  })
);

// Fallback to offline page if nothing is found in cache
var networkFirstHandler = new workbox.strategies.NetworkFirst({
  cacheName: 'default',
  plugins: [
    new workbox.expiration.Plugin({
      maxEntries: 100
    }),
    new workbox.cacheableResponse.Plugin({
      statuses: [200]
    })
  ]
});

const matcher = ({
  event
}) => event.request.mode === 'navigate';
const handler = (args) => networkFirstHandler.handle(args).then((response) => (!response) ? caches.match('/offline') : response);

workbox.routing.registerRoute(matcher, handler);
// End fallback offline



// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
  // Retrieve the textual payload from event.data (a PushMessageData object).
  // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
  // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
  const eventInfo = event.data.text();

  try {
      var data = JSON.parse(eventInfo);
      var head = data.head;
      var body = data.body;
  } catch (e) {
      var head = 'New Notification 🕺🕺';
      var body =  'Open Obrisk to view';
  }

  // Keep the service worker alive until the notification is created.
  event.waitUntil(
    self.registration.showNotification(head, {
      body: body,
      icon: 'https://obrisk.oss-cn-hangzhou.aliyuncs.com/static/img/favicon.png'
    })
  );
});