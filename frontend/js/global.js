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
    document.getElementById("addNewItem").addEventListener('click', function(e) {
      e.preventDefault();

      if (window.location.href.includes("classifieds")) {
          window.location.href="/classifieds/write-new-classified/";
      } else if (window.location.href.includes("ws/messages")) {
          window.location.href="/connections/friends/";
      }
    });

});


//Hide Top nav bar on scroll
//var prevScrollpos = window.pageYOffset;
//window.onscroll = function() {
//  var currentScrollPos = window.pageYOffset;
//  if (prevScrollpos > currentScrollPos) {
//    document.getElementById("navbarBottom").style.bottom = "-80px";
//    document.getElementById("navbarTop").style.top = "0";
//  } else {
//    document.getElementById("navbarBottom").style.bottom = "0";
//    if (!document.querySelector(".is-account-dropdown").contains("is-active")) {
//      document.getElementById("navbarTop").style.top = "0";
//    }
//  }
//  prevScrollpos = currentScrollPos;
//};
