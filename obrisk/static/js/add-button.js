$("#addNewItem").click(function(e) {
  e.preventDefault();
  if (window.location.href.includes("stories")) {
    $(".app-overlay").addClass("is-active");
    $(".close-wrap").removeClass("d-none");
    $(".is-new-content").addClass("is-highlighted");
    $(".all-stories ").addClass("block-scroll");

  } else if (window.location.href.includes("posts")) {
      window.location.href="/posts/write-new-post/";

  } else if (window.location.href.includes("ws/messages")) {
      window.location.href="/connections/friends/";

  } else if (window.location.href.includes("classifieds") &&
      (!window.location.href.endsWith("classifieds/"))) {
      window.location.href="/classifieds/write-new-classified/";
  }
});

