$(document).ready(function() {
  $(".notifications").click(function(e) {
    var target = e.target;
    if ($(target).is(".recent-notifications #close")) {
      $(".recent-notifications").removeClass("is-active");
    } else if ($(target).is("#mark")) {
    } else if ($(target).is("#view")) {
    } else {
      $(".recent-notifications").html("");
      $.ajax({
        url: "/ws/notifications/latest-notifications/",
        success: function(data) {
          $(".recent-notifications").html(data);
        }
      });
    }

    return false;
  });

  $(".acc").click(function(e) {
    var target = e.target;
    if ($(target).is("#close")) {
      $(".is-account-dropdown").removeClass("is-active");
    }
  });
});
