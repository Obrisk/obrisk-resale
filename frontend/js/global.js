let iPhone = /iPhone/.test(navigator.userAgent) && !window.MSStream;
let aspect = window.screen.width / window.screen.height;
if (
  iPhone && (aspect.toFixed(3) === "0.462" ||
    aspect.toFixed(3) === "0.576" ||
    aspect.toFixed(3) === "0.591")
) {
  document.getElementById("navbarBottom").classList.add("iphone-nav-bt");
}


document.addEventListener("DOMContentLoaded", function() {
    const drop_trigger = document.querySelector('.drop-trigger');
    const nav_drop = drop_trigger.querySelector('.nav-drop');

    document.getElementById("addNewItem").addEventListener('click', function(e) {
      e.preventDefault();
      if (window.location.href.includes("stories")) {
        document.querySelector(".app-overlay").classList.add("is-active");
        document.querySelector(".close-wrap").classList.remove("is-hidden");
        document.querySelector(".is-new-content").classList.add("is-highlighted");
        document.querySelector(".all-stories ").classList.add("block-scroll");

      } else if (window.location.href.includes("posts")) {
          window.location.href="/posts/write-new-post/";

      } else if (window.location.href.includes("ws/messages")) {
          window.location.href="/connections/friends/";

      } else if (window.location.href.includes("classifieds") &&
          (!window.location.href.endsWith("classifieds/"))) {
          window.location.href="/classifieds/write-new-classified/";
      }
    });

    drop_trigger.addEventListener('click', function (e) {
        if (drop_trigger.classList.contains('is-account')) {
            nav_drop.classList.add('is-active');
            drop_trigger.classList.add('is-opened');
        }
    });

    document.getElementById('close').addEventListener('click', function (e) {
            nav_drop.classList.remove('is-active');
            drop_trigger.classList.remove('is-opened');
            e.stopPropagation();
    });
});


//Hide Top nav bar on scroll
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbarBottom").style.bottom = "-80px";
    document.getElementById("navbarTop").style.top = "0";
  } else {
    document.getElementById("navbarBottom").style.bottom = "0";
    if (!document.querySelector(".is-account-dropdown").contains("is-active")) {
      document.getElementById("navbarTop").style.top = "0";
    }
  }
  prevScrollpos = currentScrollPos;
};
