//(function () {
//var sidebar = document.getElementById('sidebar');
//var sidebarOverlay = document.getElementsByClassName('sidebar-overlay')[0];
//var container = document.getElementsByClassName('container')[0];
////var sidebarBtnOpen = document.getElementById('sidebarBtnOpen');
//var sidebarBtnClose = document.getElementById('sidebarBtnClose');

//var openSidebar = function () {
//sidebarOverlay.style.left = '0';
//sidebar.style.left = '0';
//sidebarOverlay.style.top = '0';
//sidebar.style.display = 'block';
//$(".classifieds").toggleClass("open-sidebar");
//}

//var closeSidebar = function (e) {
//e.cancelBubble = true;
//sidebarOverlay.style.left = '-100%';
//sidebar.style.left = '-100%';
//$(".classifieds").toggleClass("open-sidebar");
//}

//sidebarOverlay.addEventListener('click', closeSidebar);
//sidebarBtnOpen.addEventListener('click', openSidebar);
//sidebarBtnClose.addEventListener('click', closeSidebar);
//})()

/* -------------------------------------------------------------------------- */
/*                              Share classifieds                             */
/* -------------------------------------------------------------------------- */

function share(title, text, url) {
  url = window.location.host + url;
  console.log(url);
  if (window.navigator.share) {
    window.navigator
      .share({
        title: title,
        text: text,
        url: url
      })
      .then(function() {
        return console.log("Successful share");
      })
      ["catch"](function(error) {
        return console.log("Error sharing", error);
      });
  } else {
    window.navigator.clipboard.writeText(url);
    // alert("copied to clipboard");
  }
}
jQuery(".share").click(function(e) {
  e.preventDefault();
});

/* -------------------------------------------------------------------------- */
/*                           Classified create ajax                           */
/* -------------------------------------------------------------------------- */

$(".close-publish").click(function(e) {
  e.preventDefault();
  $("input, textarea").val("");
  $(".app-overlay").removeClass("is-active");
  $(".is-new-content").removeClass("is-highlighted");
  $(".is-new-content").addClass("d-none");
  $(".close-wrap").addClass("d-none");
  $(".all-stories ").removeClass("block-scroll");
});

$("#addNewItem").click(function(e) {
  e.preventDefault();
  $(".app-overlay").addClass("is-active");
  $(".close-wrap").removeClass("d-none");
  $(".is-new-content").removeClass("d-none");
  $(".is-new-content").addClass("is-highlighted");
  $(".all-stories ").addClass("block-scroll");
});
