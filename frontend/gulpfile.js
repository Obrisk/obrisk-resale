var gulp = require("gulp");
var clean = require("gulp-clean");
var sass = require("gulp-sass");
var sourcemaps = require("gulp-sourcemaps");
var postcss = require("gulp-postcss");
var autoprefixer = require("autoprefixer");
var mq4HoverShim = require("mq4-hover-shim");
var rimraf = require("rimraf").sync;
var concat = require("gulp-concat");
var wait = require("gulp-wait");
var nodepath = "node_modules/";
var assetspath = "../obrisk/static/frontend/assets/";
var exec = require("child_process").exec;\
var uglify = require("gulp-uglify");


// Watch files for changes
gulp.task("watch", function() {
  gulp.watch("scss/**/*", ["compile-scss"]);
  gulp.watch("js/**/*", ["copy-js"]);
});

// Erases the destination folder
gulp.task("reset", function() {
  rimraf("bulma/*");
  rimraf("scss/*");
  rimraf("../obrisk/static/frontend/assets/css/*");
  rimraf("../obrisk/static/frontend/assets/fonts/*");
  rimraf("images/*");
});

// Erases the destination folder
gulp.task("clean", function() {
  rimraf("../obrisk/static/css");
  rimraf("../obrisk/static/js");
});

// Copy Bulma filed into Bulma development folder
gulp.task("setupBulma", function() {
  //Get Bulma from node modules
  gulp.src([nodepath + "bulma-scss/*.scss"]).pipe(gulp.dest("scss/bulma_partials"));
  gulp.src([nodepath + "bulma-scss/**/*.scss"]).pipe(gulp.dest("scss/bulma_partials"));
});


// Copy assets
gulp.task("copy", function() {
  //Copy other external css assets
  gulp
    .src([nodepath + "@mdi/font/css/materialdesignicons.min.css"])
    .pipe(gulp.dest("../obrisk/static/css/"));
  gulp
    .src([nodepath + "dripicons/webfont/webfont.css"])
    .pipe(gulp.dest("../obrisk/static/css/"));
  //Copy other external font assets
  gulp
    .src([nodepath + "@mdi/font/fonts/**/*"])
    .pipe(gulp.dest("../obrisk/static/frontend/assets/fonts/"));
  gulp
    .src([nodepath + "dripicons/webfont/fonts/**/*"])
    .pipe(gulp.dest("../obrisk/static/frontend/assets/css/fonts/"));
  gulp
    .src([nodepath + "slick-carousel/slick/fonts/**/*"])
    .pipe(gulp.dest("../obrisk/static/frontend/assets/css/fonts/"));
  gulp
    .src([nodepath + "slick-carousel/slick/ajax-loader.gif"])
    .pipe(gulp.dest("../obrisk/static/frontend/assets/css/"));
});


//Theme Scss variables
var scssOptions = {
  errLogToConsole: true,
  outputStyle: "compressed",
  includePaths: ["./scss/partials", "./scss/bulma_partials"]
};


// Compile Bulma Scss
gulp.task("compile-sass", function() {
  ];
  //Watch me get Sassy
  return gulp
    .src("./bulma/bulma.sass")
    .pipe(sourcemaps.init())
    .pipe(sass(sassOptions).on("error", sass.logError))
    .pipe(postcss(processors))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest("../obrisk/static/frontend/assets/css/"));
});


// Compile Theme Scss
gulp.task("compile-scss", function() {
  var processors = [
    mq4HoverShim.postprocessorFor({
      hoverSelectorPrefix: ".is-true-hover "
    }),
    autoprefixer({
      browsers: [
        "Chrome >= 45",
        "Firefox ESR",
        "Edge >= 12",
        "Explorer >= 10",
        "iOS >= 9",
        "Safari >= 9",
        "Android >= 4.4",
        "Opera >= 30"
      ]
    }) //,
    cssnano(),
  ];
  //Watch me get Sassy
  return gulp
    .src(["./scss/core.scss", "./scss/bulma.scss"])
    .pipe(wait(500))
    .pipe(sourcemaps.init())
    .pipe(sass(sassOptions).on("error", sass.logError))
    .pipe(postcss(processors))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest("../obrisk/static/css/"));
});


gulp.task("update-sw", function(cb) {
  exec("workbox injectManifest config.js", function(err, stdout, stderr) {
    console.log(stdout);
    console.log(stderr);
    cb(err);
  });
});


gulp.task("init", ["setupBulma"]);


gulp.task("build", [
  "clean",
  "compile-scss",
  //"update-sw"
]);

gulp.task("default", ["watch", "update-sw"]);
