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
    "revision": "a06cbd408b88eb787c36513382e8f32e"
  },
  {
    "url": "/static/css/classified-details.css",
    "revision": "b81c72755bf18f81fbb2c15448c288ec"
  },
  {
    "url": "/static/css/classifieds-list.css",
    "revision": "cec2e8e8ab59042b170e2e5cf9040bf9"
  },
  {
    "url": "/static/css/classifieds.css",
    "revision": "2e8cf3ed2c0064953906d30556233e41"
  },
  {
    "url": "/static/css/colors.css",
    "revision": "903c85830f85e79dd3a04235dfb842dd"
  },
  {
    "url": "/static/css/contact-list.css",
    "revision": "5516ef49ae01091702f03333e03505fd"
  },
  {
    "url": "/static/css/creative.css",
    "revision": "5ff2ab95f490c7dfdb553abef081a1fd"
  },
  {
    "url": "/static/css/default-skin.min.css",
    "revision": "96370330bb378f42b33670a7df03b9d5"
  },
  {
    "url": "/static/css/fancybox.min.css",
    "revision": "a2d42584292f64c5827e8b67b1b38726"
  },
  {
    "url": "/static/css/listing.css",
    "revision": "82cb2d0cc455218a5e35998a5aea27e9"
  },
  {
    "url": "/static/css/login.css",
    "revision": "8e8e8318dae724d73bf9eb5e34cd7073"
  },
  {
    "url": "/static/css/messages.css",
    "revision": "5c816159127eac8aa6d8580828a3c74b"
  },
  {
    "url": "/static/css/nav.css",
    "revision": "f6015156064b3bbd74b03319f24dcaca"
  },
  {
    "url": "/static/css/notifications.css",
    "revision": "c8c9b0217b4580c04d00c9a4aeaf2fe3"
  },
  {
    "url": "/static/css/obrisk.css",
    "revision": "c4a43ff5b4b6852f828d2d420f767cf4"
  },
  {
    "url": "/static/css/photoswipe.min.css",
    "revision": "7a55d43eef1b6fe6def95b70be9d742a"
  },
  {
    "url": "/static/css/post-create.css",
    "revision": "17c3998c7a6c057cdc072f89909f25d0"
  },
  {
    "url": "/static/css/post-details.css",
    "revision": "ee735434ea6da68dcbee355ec46709d2"
  },
  {
    "url": "/static/css/post-list.css",
    "revision": "1c1393b0bc27e639b852ddbc6d126c15"
  },
  {
    "url": "/static/css/post-update.css",
    "revision": "157e23707df89649711ee7f70c470827"
  },
  {
    "url": "/static/css/qa.css",
    "revision": "ddd3af46392bc5e6c808ab15ff48ee28"
  },
  {
    "url": "/static/css/share.css",
    "revision": "9d28b13eb46f364461626ac4daaee9d7"
  },
  {
    "url": "/static/css/slider-pro.min.css",
    "revision": "6ad9f544594d24c79e2e708252dee520"
  },
  {
    "url": "/static/css/stories.css",
    "revision": "6489e063bebc7741eabac34490cfb9f7"
  },
  {
    "url": "/static/css/swiper.min.css",
    "revision": "e7827ef3b92ce9040ca473de65143402"
  },
  {
    "url": "/static/css/uploader.css",
    "revision": "6dad78f4bf12863167d281dccaef1300"
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
    "revision": "1793c36a63916087ca206be8e7622dee"
  },
  {
    "url": "/static/css/util.css",
    "revision": "9cabf2d2ce5a30ae04a9a78140e4b73e"
  },
  {
    "url": "/static/css/wnoty.css",
    "revision": "040f1b3aad51c03add68ec5abdd182e0"
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
    "url": "/static/frontend/assets/css/app.css",
    "revision": "741f71fc4a9d5780c8feef9dfe9390f5"
  },
  {
    "url": "/static/frontend/assets/css/bulma.css",
    "revision": "4a9a178adeac28389492e5963f30efe6"
  },
  {
    "url": "/static/frontend/assets/css/materialdesignicons.min.css",
    "revision": "6c19656af1c9b61a27ddbef91b7495f4"
  },
  {
    "url": "/static/frontend/assets/css/webfont.css",
    "revision": "535b5c2f1492d1d10fc85e9fdc2411c8"
  },
  {
    "url": "/static/frontend/assets/js/app.js",
    "revision": "cdd7cda4f14ab735f2d1fb8895dc9911"
  },
  {
    "url": "/static/frontend/assets/js/chat.js",
    "revision": "a3172027f3176521cfe7403431289892"
  },
  {
    "url": "/static/frontend/assets/js/explorer.js",
    "revision": "466d466ed591b9a557fea495ef662ef9"
  },
  {
    "url": "/static/frontend/assets/js/feed.js",
    "revision": "6dd4cb00219f26cdd8fc17e1a9aa02e4"
  },
  {
    "url": "/static/frontend/assets/js/friends.js",
    "revision": "4db6c2e7eff4c21670dde3227df7dbb0"
  },
  {
    "url": "/static/frontend/assets/js/global.js",
    "revision": "aacebb1f448797470ccad76067d8ac83"
  },
  {
    "url": "/static/frontend/assets/js/main.js",
    "revision": "bfa3a9f4dcf53fe0a8c8bbaf9d26b62c"
  },
  {
    "url": "/static/img/android-chrome-192x192.png",
    "revision": "83763c96d4a2dfbaa0bc84739a464659"
  },
  {
    "url": "/static/img/android-chrome-512x512.png",
    "revision": "61678795edacc3db463077102233608e"
  },
  {
    "url": "/static/img/apple-touch-icon.png",
    "revision": "f784ffd3e5494fcd8c7047a35e3638d5"
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
    "revision": "791bf66fe880c78d3af46782af534b2f"
  },
  {
    "url": "/static/img/favicon-32x32.png",
    "revision": "9862950cc40e5ce4becd79238cceafcc"
  },
  {
    "url": "/static/img/favicon.png",
    "revision": "90a5ca3cac34705dd661fd7b748e7878"
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
    "url": "/static/img/icons.png",
    "revision": "c9ceb83c0a247ae47f54c3e1d3cb4bac"
  },
  {
    "url": "/static/img/image.png",
    "revision": "6b00566e6a7a54df0b83fe8a1d8b9427"
  },
  {
    "url": "/static/img/logo_blue.png",
    "revision": "6509a793972d3e1addc199bab412f058"
  },
  {
    "url": "/static/img/logo_light_blue.png",
    "revision": "b0fbd8e5dcd5a2c390a49b0072984f9f"
  },
  {
    "url": "/static/img/mstile-144x144.png",
    "revision": "2d4e642f0d7326b53f4f878cf098852d"
  },
  {
    "url": "/static/img/mstile-150x150.png",
    "revision": "e19502cab20336b9188fdf9b87a6e0f5"
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
    "revision": "a44a9f2a323fc44105c960ad4032a59f"
  },
  {
    "url": "/static/img/splashscreens/ipadpro1_splash.png",
    "revision": "642c441ec8313a3547ef98462c15138a"
  },
  {
    "url": "/static/img/splashscreens/ipadpro2_splash.png",
    "revision": "2dce0f0e649fc0f447886e78cf123e8b"
  },
  {
    "url": "/static/img/splashscreens/ipadpro3_splash.png",
    "revision": "4d2f8df0042c6ac20ba59c9118551a65"
  },
  {
    "url": "/static/img/splashscreens/iphone5_splash.png",
    "revision": "d0ac57dcc13ce9cd08718452ac6d63a5"
  },
  {
    "url": "/static/img/splashscreens/iphone6_splash.png",
    "revision": "1b08ee90693fc08f2fcd739649fb1570"
  },
  {
    "url": "/static/img/splashscreens/iphoneplus_splash.png",
    "revision": "1b6c2a1d1a5b7202fc28965c61726e11"
  },
  {
    "url": "/static/img/splashscreens/iphonex_splash.png",
    "revision": "2f9f59a6b1a8b21e2d916d6f04154799"
  },
  {
    "url": "/static/img/splashscreens/iphonexr_splash.png",
    "revision": "3cb448df5e5a3802551d66e5c925eceb"
  },
  {
    "url": "/static/img/splashscreens/iphonexsmax_splash.png",
    "revision": "566144ae53db57307db0826fc19043c6"
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
    "url": "/static/js/classifieds.js",
    "revision": "403cb439d098716f592053d9e7482f49"
  },
  {
    "url": "/static/js/fancybox.min.js",
    "revision": "003e7d1be42767dacd59bd516082e9e1"
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
    "url": "/static/js/jquery.sliderPro.min.js",
    "revision": "65a3bab710e0c266d08584b0c8987c34"
  },
  {
    "url": "/static/js/jquery.waypoints.min.js",
    "revision": "cebc34dedef229a98275955df75e20e5"
  },
  {
    "url": "/static/js/lazyload.js",
    "revision": "24d9fcc8fa17bbd4fae97f9a8360dbab"
  },
  {
    "url": "/static/js/listing.js",
    "revision": "9ef56367aefea3ae6b79bef9d2fcbf05"
  },
  {
    "url": "/static/js/location.js",
    "revision": "1a27a7150aefee3a045965bfd5272631"
  },
  {
    "url": "/static/js/messager.js",
    "revision": "1ff3dfbab752def3d16fff5479f878f8"
  },
  {
    "url": "/static/js/moment.min.js",
    "revision": "761502841c035afcf6a9bdc5d0a20d11"
  },
  {
    "url": "/static/js/multipleUploader.js",
    "revision": "881aba930504dad61530144a4daee0d2"
  },
  {
    "url": "/static/js/nav.js",
    "revision": "6d50249b1413a573c4d592437f092d05"
  },
  {
    "url": "/static/js/notif-sw.js",
    "revision": "38d1cb8689e33c694cc8ff6139b1790f"
  },
  {
    "url": "/static/js/obrisk.js",
    "revision": "5252e8a20acd6d12aee616761a55808d"
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
    "url": "/static/js/post-uploader.js",
    "revision": "7e3b824340d53b5acabd6cb31b7cbdf5"
  },
  {
    "url": "/static/js/posts.js",
    "revision": "60c600c6e470d68e52231a60008175eb"
  },
  {
    "url": "/static/js/profile-uploader.js",
    "revision": "e756797bfe972cf90e7a2d3d348785f4"
  },
  {
    "url": "/static/js/qa.js",
    "revision": "de517f44c5974b93e7b984f0570dbf15"
  },
  {
    "url": "/static/js/share.js",
    "revision": "98959a4677a4341fb8dcfbd24b47f925"
  },
  {
    "url": "/static/js/stories.js",
    "revision": "09f9e9035a19b456df543063bb3bfa3d"
  },
  {
    "url": "/static/js/swiper.min.js",
    "revision": "7513a78ef80742576aee1bdd39d217ed"
  },
  {
    "url": "/static/js/uploader.js",
    "revision": "b2e2b9d6d520af3a9ef978e417467639"
  },
  {
    "url": "/static/js/user-form.js",
    "revision": "87e102e37b64e6c0f631e4851c0cb7a5"
  },
  {
    "url": "/static/js/websocketbridge.js",
    "revision": "cdf4bd9dbfc48c91b2869b8f15fcb25c"
  },
  {
    "url": "/static/js/wnoty.js",
    "revision": "3c5e81bd9ffc8a2d83556293d6cdc2db"
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