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


$(document).ready(function() {
  $(".notifications").click(function(e) {
    var target = e.target;
    if ($(target).is(".recent-notifications #close")) {
      $(".recent-notifications").removeClass("is-active");
    } else if ($(target).is("#mark")) {
        //console.log ()
    } else if ($(target).is("#view")) {
        //console.log ()
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
