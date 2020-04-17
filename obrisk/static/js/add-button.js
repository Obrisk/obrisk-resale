$("#addNewItem").click(function(e) {
  e.preventDefault();
  if (window.location.href.includes("posts")) {
      window.location.href="/posts/write-new-post/";

  } else if (window.location.href.includes("ws/messages")) {
      window.location.href="/connections/friends/";
  }
});

