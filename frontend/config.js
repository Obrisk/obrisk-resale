module.exports = {
    "globDirectory": "../obrisk/static",
    "globPatterns": [
        "**/*.{css,html,js,png,jpg,gif,ico}"
    ],
    globIgnores: ["**/workbox*", "**assets/img/**", "**assets/images/**"],
    "swDest": "../obrisk/templates/serviceworker.js",
    "swSrc": "../obrisk/templates/sw-src.js",
    modifyURLPrefix: {

        'css': '/static/css',
        'fonts': '/static/fonts',
        'img': '/static/img',
        'js': '/static/js',
        'assets': '/static/frontend/assets',
        'webpush': '/static/webpush'
    },
};