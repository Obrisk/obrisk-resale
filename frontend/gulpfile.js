// Initialize modules
const { src, dest, watch, series, parallel } = require('gulp');
const sourcemaps = require('gulp-sourcemaps');
const sass = require('gulp-sass');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify-es').default;
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

//const replace = require('gulp-replace');
//Gulp3 variables, their calls are commented
//const clean = require("gulp-clean");
//const mq4HoverShim = require("mq4-hover-shim");
//const rimraf = require("rimraf").sync;
//const wait = require("gulp-wait");
//const nodepath = "node_modules/";
//const exec = require("child_process").exec;

// File paths
const files = { 
    scssPath: './scss/*.scss',
    jsPath: './js/*.js'
}

const destPath = {
    cssPath: '../obrisk/static/css/',
    jsPath:  '../obrisk/static/js/'
}

// Sass task: compiles the .scss files into .css
function scssTask(){    
    return src(files.scssPath)
        .pipe(sourcemaps.init()) // initialize sourcemaps first
        .pipe(sass()) // compile SCSS to CSS
        .pipe(postcss([ autoprefixer(), cssnano() ])) // PostCSS plugins
        .pipe(sourcemaps.write('../../../frontend/scss/sourcemaps/')) // write sourcemaps file in current directory
        .pipe(dest(destPath.cssPath)
    ); 
}

// JS task: concatenates and uglifies JS files to script.js
function jsTask(){
    return src([
        files.jsPath
        //,'!' + 'includes/js/jquery.min.js', // to exclude any specific files
        ])
        .pipe(uglify())
        .pipe(dest(destPath.jsPath)
    );
}

// If we want the static files to have version query 
// so that the local cache will be wiped 
function cacheBustTask(){
    var cbString = new Date().getTime();
    return src(['index.html'])
        .pipe(replace(/cb=\d+/g, 'cb=' + cbString))
        .pipe(dest('.'));
}

// Watch task: watch SCSS and JS files for changes
// If any change, run scss and js tasks simultaneously
function watchTask(){
    watch([files.scssPath, files.jsPath],
        {interval: 1000, usePolling: true}, //Makes docker work
        series(
            parallel(scssTask, jsTask)
        )
    );    
}


// Runs the scss tasks simultaneously
exports.scss = series(
    scssTask
);

// Runs the js tasks simultaneously
exports.js = series(
    jsTask 
);


// Runs the js tasks simultaneously
exports.watch = series(
    watchTask
);


// Export the default Gulp task so it can be run
// Runs the scss and js tasks simultaneously
exports.default = series(
    parallel(scssTask, jsTask), 
    watchTask
);


// Erases the dev folder
//gulp.task("reset", function() {
//  rimraf("bulma/*");
//  rimraf("scss/*");
//  rimraf("../obrisk/static/frontend/assets/css/*");
//  rimraf("../obrisk/static/frontend/assets/fonts/*");
//  rimraf("images/*");
//});
//
//// Erases the destination folder
//gulp.task("clean", function() {
//  rimraf("../obrisk/static/css");
//  rimraf("../obrisk/static/js");
//});
//
//// Copy Bulma filed into Bulma development folder
//gulp.task("setupBulma", function() {
//  //Get Bulma from node modules
//  gulp.src([nodepath + "bulma-scss/*.scss"]).pipe(gulp.dest("scss/bulma_partials"));
//  gulp.src([nodepath + "bulma-scss/**/*.scss"]).pipe(gulp.dest("scss/bulma_partials"));
//});
//
//
//// Copy assets
//gulp.task("copy", function() {
//  //Copy other external css assets
//  gulp
//    .src([nodepath + "@mdi/font/css/materialdesignicons.min.css"])
//    .pipe(gulp.dest("../obrisk/static/css/vendor/"));
//  gulp
//    .src([nodepath + "dripicons/webfont/webfont.css"])
//    .pipe(gulp.dest("../obrisk/static/css/vendor"));
//  //Copy other external font assets
//  gulp
//    .src([nodepath + "@mdi/font/fonts/**/*"])
//    .pipe(gulp.dest("../obrisk/static/frontend/assets/fonts/"));
//  gulp
//    .src([nodepath + "dripicons/webfont/fonts/**/*"])
//    .pipe(gulp.dest("../obrisk/static/fonts/"));
//  gulp
//    .src([nodepath + "slick-carousel/slick/fonts/**/*"])
//    .pipe(gulp.dest("../obrisk/static/fonts/"));
//  gulp
//    .src([nodepath + "slick-carousel/slick/ajax-loader.gif"])
//    .pipe(gulp.dest("../obrisk/static/css/vendor/"));
//});
//
//
////Theme Scss variables
//var scssOptions = {
//  errLogToConsole: true,
//  outputStyle: "compressed",
//  includePaths: ["./scss/partials", "./scss/bulma_partials"]
//};
//
//
//gulp.task("update-sw", function(cb) {
//  exec("workbox injectManifest config.js", function(err, stdout, stderr) {
//    console.log(stdout);
//    console.log(stderr);
//    cb(err);
//  });
//});
//
//
//gulp.task("init", ["setupBulma"]);
//
//
//gulp.task("build", [
//  "clean",
//  "compile-scss",
//  //"update-sw"
//]);

//gulp.task("default", ["watch", "update-sw"]);
