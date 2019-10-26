//To be able to skip and use the new service worker no matter what
importScripts("/static/js/workbox-v4.3.1/workbox-sw.js");
workbox.setConfig({
  modulePathPrefix: "/static/js/workbox-v4.3.1"
});
//Show debug logs in console
workbox.setConfig({
  debug: false
});

workbox.core.skipWaiting();

workbox.precaching.precacheAndRoute([
  {
    "url": "/static/assets/css/ajax-loader.gif",
    "revision": "c5cd7f5300576ab4c88202b42f6ded62"
  },
  {
    "url": "/static/assets/css/app.css",
    "revision": "cdb7eab95e30b95d29bcc178bd96b3fb"
  },
  {
    "url": "/static/assets/css/bulma.css",
    "revision": "3d7dbc3e093f3e73074f21ae30f0a771"
  },
  {
    "url": "/static/assets/css/core.css",
    "revision": "c13c2c7ba1c5b008fbca80e550963dbf"
  },
  {
    "url": "/static/assets/css/materialdesignicons.min.css",
    "revision": "6c19656af1c9b61a27ddbef91b7495f4"
  },
  {
    "url": "/static/assets/css/webfont.css",
    "revision": "535b5c2f1492d1d10fc85e9fdc2411c8"
  },
  {
    "url": "/static/assets/js/app.js",
    "revision": "f8118613e701fe8aa40dc43334a2d5b3"
  },
  {
    "url": "/static/assets/js/autocompletes.js",
    "revision": "a84c9e2e8b09234eebf8b94f4e7a6a88"
  },
  {
    "url": "/static/assets/js/chat.js",
    "revision": "a3172027f3176521cfe7403431289892"
  },
  {
    "url": "/static/assets/js/elements.js",
    "revision": "a32f46c2a4b411950b1b891c192b6c10"
  },
  {
    "url": "/static/assets/js/events.js",
    "revision": "24e63a872b5cbf926826ce79c41336b0"
  },
  {
    "url": "/static/assets/js/explorer.js",
    "revision": "466d466ed591b9a557fea495ef662ef9"
  },
  {
    "url": "/static/assets/js/feed.js",
    "revision": "6dd4cb00219f26cdd8fc17e1a9aa02e4"
  },
  {
    "url": "/static/assets/js/friends.js",
    "revision": "4db6c2e7eff4c21670dde3227df7dbb0"
  },
  {
    "url": "/static/assets/js/global.js",
    "revision": "eb083b6aa4b56e4cdead8d078e34a579"
  },
  {
    "url": "/static/assets/js/go-live.js",
    "revision": "bf76b7cd1a32e52388d32c932242b435"
  },
  {
    "url": "/static/assets/js/inbox.js",
    "revision": "04068a235862aa45574e287165d94559"
  },
  {
    "url": "/static/assets/js/landing.js",
    "revision": "1c90809f8d2f444c6d7b47a1576b88a2"
  },
  {
    "url": "/static/assets/js/lightbox.js",
    "revision": "5344d8c46b063ed71fe25c1044e50cd1"
  },
  {
    "url": "/static/assets/js/main.js",
    "revision": "cb0774ba0079311c467ad1da25793cba"
  },
  {
    "url": "/static/assets/js/modal-uploader.js",
    "revision": "cd66113247e284c73cb78d462f6fc040"
  },
  {
    "url": "/static/assets/js/news.js",
    "revision": "0044306da774b6bbf76d8f369bb236ac"
  },
  {
    "url": "/static/assets/js/popovers-pages.js",
    "revision": "84703e877b88d17bf2bb6febcba204d5"
  },
  {
    "url": "/static/assets/js/popovers-users.js",
    "revision": "7b103ef98cf014962eb7d08ce3347b61"
  },
  {
    "url": "/static/assets/js/profile.js",
    "revision": "22232474dae8182c745b52a7df32748d"
  },
  {
    "url": "/static/assets/js/questions.js",
    "revision": "765dca8c12dd834efd4773c7b204f18e"
  },
  {
    "url": "/static/assets/js/signup.js",
    "revision": "7760e1216245b3896ef0da25f0a0108b"
  },
  {
    "url": "/static/assets/js/touch.js",
    "revision": "1140bb01d2a04b048245c5a1036be175"
  },
  {
    "url": "/static/assets/js/tour.js",
    "revision": "18de6e2130b112c2961f2cfd603f69f6"
  },
  {
    "url": "/static/assets/js/videos.js",
    "revision": "a1ab8ad0ce3e68f7841518cda5b562a4"
  },
  {
    "url": "/static/assets/js/widgets.js",
    "revision": "b8e215360a354e57aa6c753016e03fe0"
  },
  {
    "url": "/static/css/account.css",
    "revision": "289df53074c930a43556f71537a9e23e"
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
    "revision": "dd18d06f83c5bbd0b180801e007aa76e"
  },
  {
    "url": "/static/css/classified-details.css",
    "revision": "5560e0789d8e2823cd66da29393faee9"
  },
  {
    "url": "/static/css/classifieds-list.css",
    "revision": "e472cf4ef2fcb4d20aec21a151630806"
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
    "revision": "d8ea8e39df4cb9f2829795c8085b1e50"
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
    "revision": "ba3cd62796c6ef299573e487809989ca"
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
    "revision": "8c407ddd228da19e56736ab716eeb8b0"
  },
  {
    "url": "/static/css/notifications.css",
    "revision": "08f6483366fa709c97a8aaa571858d62"
  },
  {
    "url": "/static/css/obrisk.css",
    "revision": "4430da15e6f00e327cd9605a85efa6f9"
  },
  {
    "url": "/static/css/photoswipe.min.css",
    "revision": "f196c59501ba1283d3d863bf7b733635"
  },
  {
    "url": "/static/css/post-create.css",
    "revision": "8f35a0037000978eff167c0f9b0bb836"
  },
  {
    "url": "/static/css/post-details.css",
    "revision": "ec1f65bffb1c2b52a5eca725ab934123"
  },
  {
    "url": "/static/css/post-list.css",
    "revision": "960ea00e06bf3189421a6243d2dbb045"
  },
  {
    "url": "/static/css/post-update.css",
    "revision": "8f35a0037000978eff167c0f9b0bb836"
  },
  {
    "url": "/static/css/preloader.gif",
    "revision": "4cc848b538580780aa52b50a7a18e1fa"
  },
  {
    "url": "/static/css/qa.css",
    "revision": "a99ce06bc73af4a7a4665ee8acfcc75b"
  },
  {
    "url": "/static/css/stories.css",
    "revision": "db5470b7fd44a000fc736db5e7c1189f"
  },
  {
    "url": "/static/css/swiper.min.css",
    "revision": "e15e63828bf778572d6535e497a718a2"
  },
  {
    "url": "/static/css/uploader.css",
    "revision": "1d458c31550be3ca07bae49ade351ddd"
  },
  {
    "url": "/static/css/user_form.css",
    "revision": "5a20c5887cf8043d5099017e97e54b90"
  },
  {
    "url": "/static/css/user_list.css",
    "revision": "a7964db0a6c7c440706cb810ab16cde5"
  },
  {
    "url": "/static/css/user_profile.css",
    "revision": "5b7038b0ee03761a3bfb3bf819e5f578"
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
    "url": "/static/img/full-logo-v2.png",
    "revision": "1a20ee79061b3417a3cdc9e862902090"
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
    "revision": "205caeb2754ac7de94d1ea88b367badf"
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
    "revision": "ea4417a595c5f82501191869ba42aa02"
  },
  {
    "url": "/static/js/fancybox.min.js",
    "revision": "d6d71ddf529188fb35a2bc65efdca539"
  },
  {
    "url": "/static/js/html5shiv.min.js",
    "revision": "40bd440d29b3a9371b0c63fec41ee64f"
  },
  {
    "url": "/static/js/imageClient.js",
    "revision": "201ffb200c62b0f13b58ff362f8790c0"
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
    "revision": "3b3b9381b5994b37d536e1d1bc721360"
  },
  {
    "url": "/static/js/location.js",
    "revision": "45be2f2d5b1e9015c4b8f0761aa52d65"
  },
  {
    "url": "/static/js/messager.js",
    "revision": "878fc34bd3786d661780252aaaf5836f"
  },
  {
    "url": "/static/js/moment.min.js",
    "revision": "761502841c035afcf6a9bdc5d0a20d11"
  },
  {
    "url": "/static/js/nav.js",
    "revision": "03c72346e3d52329015f10fcfcc87894"
  },
  {
    "url": "/static/js/notif-sw.js",
    "revision": "74eb00aa496ead50011a95306103430c"
  },
  {
    "url": "/static/js/obrisk.js",
    "revision": "5d76c1e7414b3b19aef70c720a765c58"
  },
  {
    "url": "/static/js/photoswipe-ui-default.min.js",
    "revision": "9517baca43cd4e9cb23ff337fbc1baa1"
  },
  {
    "url": "/static/js/photoswipe.min.js",
    "revision": "f5cd6479c4e4682545a9603e6b50c741"
  },
  {
    "url": "/static/js/popper.min.js",
    "revision": "354e13e7651ee5d25b68e43282911d33"
  },
  {
    "url": "/static/js/post-uploader.js",
    "revision": "0c76b0bd3813a9bc7ce5ffa038558fd6"
  },
  {
    "url": "/static/js/posts.js",
    "revision": "3e629bf0360dced14124c2baf030516d"
  },
  {
    "url": "/static/js/profile-uploader.js",
    "revision": "24ff27e6dc4c145baa420dbfd83e67f2"
  },
  {
    "url": "/static/js/qa.js",
    "revision": "b1a4f5f99b3024b3bfff64965b2319bf"
  },
  {
    "url": "/static/js/stories.js",
    "revision": "95c40e769b3f60f434da75fa9426942a"
  },
  {
    "url": "/static/js/swiper.min.js",
    "revision": "d1dc6e2f65902bdfeaf88c9ef20254e0"
  },
  {
    "url": "/static/js/toast-msg.js",
    "revision": "36d40daeb71af271364fb3a27987e7aa"
  },
  {
    "url": "/static/js/upload.js",
    "revision": "870030b9f70424b4e6d23995f6eea9d9"
  },
  {
    "url": "/static/js/uploader.js",
    "revision": "01f65ab229686eed300ee89b3c5c4afd"
  },
  {
    "url": "/static/js/user-form.js",
    "revision": "872dcd7dc266c7323fb814ef1e3bcbe6"
  },
  {
    "url": "/static/js/websocketbridge.js",
    "revision": "cdf4bd9dbfc48c91b2869b8f15fcb25c"
  },
  {
    "url": "/static/webpush/webpush.js",
    "revision": "0b019a8f720c305a6ce0de13762865db"
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
    var body = 'Open Obrisk to view';
  }

  // Keep the service worker alive until the notification is created.
  event.waitUntil(
    self.registration.showNotification(head, {
      body: body,
      icon: 'https://obrisk.oss-cn-hangzhou.aliyuncs.com/static/img/favicon.png'
    })
  );
});