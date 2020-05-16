$(function() {
  function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  // This sets up every ajax call with proper headers.
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

});

document.querySelector("#addNewItem").click(function(e) {
  e.preventDefault();
  if (window.location.href.includes("stories")) {
    document.querySelector(".app-overlay").classList.add("is-active");
    document.querySelector(".close-wrap").classList.remove("d-none");
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


document.addEventListener("DOMContentLoaded", function() {
    $(".notifications").click(function(e) {
    var target = e.target;
    if (document.querySelector(target).is(".recent-notifications #close")) {
      document.querySelector(".recent-notifications").classList.remove("is-active");
    } else {
      document.querySelector(".recent-notifications").innerHTML("");

	 // use fetch on the /posts route, then pass the response along
	    fetch("/ws/notifications/latest-notifications/").then(function(response) {
		// with the response, parse to text, then pass it along
		response.text().then(function(data) {
		  
		  document.querySelector(".recent-notifications").innerHTML(data);
		});
	    });
    }

    return false;
  });

  document.querySelector(".acc").click(function(e) {
    var target = e.target;
    if (document.querySelector(target).is("#close")) {
      document.querySelector(".is-account-dropdown").classList.remove("is-active");
    }
  });
});
