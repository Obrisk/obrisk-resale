module.exports = {
    "globDirectory": "static",
    "globPatterns": [
        "**/*.{css,html,js,png,jpg,gif,ico}"
    ],
    globIgnores: ["**/workbox*"],
    "swDest": "templates/serviceworker.js",
    "swSrc": "templates/sw-src.js",
    modifyURLPrefix: {

        'css': '/static/css',
        'fonts': '/static/fonts',
        'img': '/static/img',
        'js': '/static/js',
        'webpush': '/static/webpush'
    },
};