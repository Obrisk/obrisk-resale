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
    "revision": "ec1178f1513f83e8f256912506a0c025"
  },
  {
    "url": "/static/css/colors.css",
    "revision": "903c85830f85e79dd3a04235dfb842dd"
  },
  {
    "url": "/static/css/contact-list.css",
    "revision": "b79ec061457ba01eccf69f09b115965f"
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
    "url": "/static/css/images/blank.gif",
    "revision": "07b31fa8a00640021b3997ebe4562b70"
  },
  {
    "url": "/static/css/listing.css",
    "revision": "82cb2d0cc455218a5e35998a5aea27e9"
  },
  {
    "url": "/static/css/login.css",
    "revision": "d4bbec33e3ea614936fb86a4267da20f"
  },
  {
    "url": "/static/css/messages.css",
    "revision": "5c816159127eac8aa6d8580828a3c74b"
  },
  {
    "url": "/static/css/nav.css",
    "revision": "3ca2770c9b22da159f5fe98062b785d3"
  },
  {
    "url": "/static/css/notifications.css",
    "revision": "c8c9b0217b4580c04d00c9a4aeaf2fe3"
  },
  {
    "url": "/static/css/obrisk.css",
    "revision": "ea19ac4b90573564bb0e6decd6393023"
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
    "revision": "e3e94d0fde9007d3b9047135edcef0c9"
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
    "url": "/static/css/slider-pro.min.css",
    "revision": "6ad9f544594d24c79e2e708252dee520"
  },
  {
    "url": "/static/css/stories.css",
    "revision": "c2cac86e85b3a8aafb3d394c93859b5b"
  },
  {
    "url": "/static/css/swiper.min.css",
    "revision": "e7827ef3b92ce9040ca473de65143402"
  },
  {
    "url": "/static/css/uploader.css",
    "revision": "90c59c696f044caff617065c1c0fa4d0"
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
    "url": "frontend/assets/css/ajax-loader.gif",
    "revision": "c5cd7f5300576ab4c88202b42f6ded62"
  },
  {
    "url": "frontend/assets/css/app.css",
    "revision": "a2a2a7117b1cdb5d1efe7b57928c0976"
  },
  {
    "url": "frontend/assets/css/bulma.css",
    "revision": "4a9a178adeac28389492e5963f30efe6"
  },
  {
    "url": "frontend/assets/css/core.css",
    "revision": "2c838031b9c782d78982b14fc271a998"
  },
  {
    "url": "frontend/assets/css/materialdesignicons.min.css",
    "revision": "169a7721873bc1ecad61797edc3b304f"
  },
  {
    "url": "frontend/assets/css/webfont.css",
    "revision": "aea41e7f54519a53a1629b2d23069e61"
  },
  {
    "url": "frontend/assets/js/app.js",
    "revision": "9bf0224de24fee8db5746617c44de6b3"
  },
  {
    "url": "frontend/assets/js/autocompletes.js",
    "revision": "a84c9e2e8b09234eebf8b94f4e7a6a88"
  },
  {
    "url": "frontend/assets/js/chat.js",
    "revision": "a3172027f3176521cfe7403431289892"
  },
  {
    "url": "frontend/assets/js/elements.js",
    "revision": "a32f46c2a4b411950b1b891c192b6c10"
  },
  {
    "url": "frontend/assets/js/events.js",
    "revision": "24e63a872b5cbf926826ce79c41336b0"
  },
  {
    "url": "frontend/assets/js/explorer.js",
    "revision": "466d466ed591b9a557fea495ef662ef9"
  },
  {
    "url": "frontend/assets/js/feed.js",
    "revision": "6dd4cb00219f26cdd8fc17e1a9aa02e4"
  },
  {
    "url": "frontend/assets/js/friends.js",
    "revision": "4db6c2e7eff4c21670dde3227df7dbb0"
  },
  {
    "url": "frontend/assets/js/global.js",
    "revision": "aacebb1f448797470ccad76067d8ac83"
  },
  {
    "url": "frontend/assets/js/go-live.js",
    "revision": "bf76b7cd1a32e52388d32c932242b435"
  },
  {
    "url": "frontend/assets/js/inbox.js",
    "revision": "04068a235862aa45574e287165d94559"
  },
  {
    "url": "frontend/assets/js/landing.js",
    "revision": "1c90809f8d2f444c6d7b47a1576b88a2"
  },
  {
    "url": "frontend/assets/js/lightbox.js",
    "revision": "ea87e91145637177d1641359bcd1307f"
  },
  {
    "url": "frontend/assets/js/main.js",
    "revision": "bfa3a9f4dcf53fe0a8c8bbaf9d26b62c"
  },
  {
    "url": "frontend/assets/js/modal-uploader.js",
    "revision": "cd66113247e284c73cb78d462f6fc040"
  },
  {
    "url": "frontend/assets/js/news.js",
    "revision": "0044306da774b6bbf76d8f369bb236ac"
  },
  {
    "url": "frontend/assets/js/popovers-pages.js",
    "revision": "84703e877b88d17bf2bb6febcba204d5"
  },
  {
    "url": "frontend/assets/js/popovers-users.js",
    "revision": "7b103ef98cf014962eb7d08ce3347b61"
  },
  {
    "url": "frontend/assets/js/profile.js",
    "revision": "22232474dae8182c745b52a7df32748d"
  },
  {
    "url": "frontend/assets/js/questions.js",
    "revision": "765dca8c12dd834efd4773c7b204f18e"
  },
  {
    "url": "frontend/assets/js/signup.js",
    "revision": "7760e1216245b3896ef0da25f0a0108b"
  },
  {
    "url": "frontend/assets/js/touch.js",
    "revision": "1140bb01d2a04b048245c5a1036be175"
  },
  {
    "url": "frontend/assets/js/tour.js",
    "revision": "18de6e2130b112c2961f2cfd603f69f6"
  },
  {
    "url": "frontend/assets/js/videos.js",
    "revision": "a1ab8ad0ce3e68f7841518cda5b562a4"
  },
  {
    "url": "frontend/assets/js/widgets.js",
    "revision": "b8e215360a354e57aa6c753016e03fe0"
  },
  {
    "url": "/static/img/ajax-loader.gif",
    "revision": "04836c514aea7d3d203112128be81fd6"
  },
  {
    "url": "/static/img/android-chrome-192x192.png",
    "revision": "5de38bb634e3365ccad6a5808cbfbe22"
  },
  {
    "url": "/static/img/android-chrome-512x512.png",
    "revision": "382e988c80d4b854aaccbb149c5f4b98"
  },
  {
    "url": "/static/img/apple-touch-icon.png",
    "revision": "df28f0ba4dd3a8bd08f39269d6e686e2"
  },
  {
    "url": "/static/img/bg.png",
    "revision": "8ddad23ce6dcc70bf111b23ae022f10c"
  },
  {
    "url": "/static/img/blank.gif",
    "revision": "07b31fa8a00640021b3997ebe4562b70"
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
    "revision": "333313efcf24c4341fe3315cb71a264d"
  },
  {
    "url": "/static/img/favicon-32x32.png",
    "revision": "e317d20287c3df252fa904b8d9e27324"
  },
  {
    "url": "/static/img/favicon.ico",
    "revision": "402f6510d7a32c2be9dd508de3aac6f1"
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
    "url": "/static/img/homepage-bg.jpg",
    "revision": "17b3eb9f6992a754f6cc5978798189a2"
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
    "url": "/static/img/loading-anti-clockwise.gif",
    "revision": "24403b4fe8914bc583ae9b0ab09bf0e2"
  },
  {
    "url": "/static/img/loading-block-puzzle.gif",
    "revision": "2b018964331551ec6c27f81efc8b160c"
  },
  {
    "url": "/static/img/loading.gif",
    "revision": "387d69b4eb5cdf1e050cc89cc20b5f5c"
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
    "url": "/static/js/classifieds.js",
    "revision": "831fdeff08cf0bbbdebc94bf9bb9759d"
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
    "url": "/static/js/listing.js",
    "revision": "548da0625fb5256127b9a7ffab8aed3e"
  },
  {
    "url": "/static/js/location.js",
    "revision": "1a27a7150aefee3a045965bfd5272631"
  },
  {
    "url": "/static/js/messager.js",
    "revision": "6b443e4c497a5383caa639a2f3e2d55c"
  },
  {
    "url": "/static/js/moment.min.js",
    "revision": "761502841c035afcf6a9bdc5d0a20d11"
  },
  {
    "url": "/static/js/multipleUploader.js",
    "revision": "b88d137e7e0bb02bb25f44ff4ed707f1"
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
    "revision": "74ea2840b2d6944215e8bdf22bf2e7ca"
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
    "revision": "cadb538595ea32a931d3a7c5730acb17"
  },
  {
    "url": "/static/js/swiper.min.js",
    "revision": "7513a78ef80742576aee1bdd39d217ed"
  },
  {
    "url": "/static/js/toast-msg.js",
    "revision": "af82356c546778cbdf17b6f9ae8b79d7"
  },
  {
    "url": "/static/js/uploader.js",
    "revision": "eda88ca267350c06bd2b0b7cf8fe91c4"
  },
  {
    "url": "/static/js/user-form.js",
    "revision": "82a759fee43d43bcfc3913e1674842f4"
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