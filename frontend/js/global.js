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
    var drop_trigger = document.querySelector('.drop-trigger');
    var nav_drop = document.querySelector('.nav-drop');

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
            console.log('here');
            nav_drop.classList.add('is-active');
            drop_trigger.classList.add('is-opened');
        }
    });

    document.getElementById('close').addEventListener('click', function (e) {
            nav_drop.classList.remove('is-active');
            drop_trigger.classList.remove('is-opened');
            e.stopPropagation();
    });

    if (currentUser !== undefined) {
        let notf = document.querySelector(".notifications");
        notf.addEventListener('click', function(e) {
            if (notif.is(".recent-notifications #close")) {
              document.querySelector(".recent-notifications").classList.remove("is-active");
            } else {
              document.querySelector(".recent-notifications").innerHTML("");

             // use fetch on the /posts route, then pass the response along
                fetch("/ws/notifications/latest-notifications/")
                .then(function(response) {
                    // with the response, parse to text, then pass it along
                    response.text().then(function(data) {
                      document.querySelector(".recent-notifications").innerHTML(data);
                    });
                });
            }
            return false;
      });
    }
});
