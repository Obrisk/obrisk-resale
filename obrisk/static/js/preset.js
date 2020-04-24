$(function() {
  function getCookie(name) {
    // Function to get any cookie available in the session.
    var cookieValue = null;
    if (document.cookie) {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie("csrftoken");

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
