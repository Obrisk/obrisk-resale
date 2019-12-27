$(function() {
  function getCookie(name) {
    // Function to get any cookie available in the session.
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
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

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  function offset(el) {
    var rect = el.getBoundingClientRect(),
      scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
      scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    return { top: rect.top + scrollTop, left: rect.left + scrollLeft };
  }

  // This sets up every ajax call with proper headers.
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $("input, textarea").val("");

  //Submit stories
  $(".submit-button").click(function(e) {
    e.preventDefault();
    //check if text only
    if (uploader.fileStats.totalFilesNum > 0) {
      $("body").trigger("submitClicked");
    } else if (
      $("#publish")
        .val()
        .substring(0, 20).length != 0
    ) {
      $("body").trigger("uploadComplete");
    } else {
      bootbox.alert("Please, Upload an image or write something!");
    }
  });

  //Liker
  $(".infinite-container").on("click", ".like-wrapper", function() {
    // Ajax call on action on like button.
    var li = $(this).closest(".card");
    var stories = $(li).attr("stories-id");

    if (user != "") {
      $.ajax({
        url: "/stories/like/",
        data: {
          stories: stories
        },
        type: "GET",
        cache: false,
        success: function(data) {
          li.find(".likes-count .count").text(data.likes);
        }
      });
    } else {
      window.location.href = "/accounts-authorization/login/";
    }

    return false;
  });

  //Cose comments
  $(".infinite-container").on("click", ".close-comments", function() {
    // Ajax call to request a given Stories object detail and thread, and to
    // show it in a modal.
    var post = $(this).closest(".card");
    var stories = $(post).attr("stories-id");
    post.find(".content-wrap").toggleClass("is-hidden");
    post.find(".comments-wrap").toggleClass("is-hidden");
  });

  //Show comments
  $(".infinite-container").on("click", ".is-comment", function() {
    // Ajax call to request a given Stories object detail and thread, and to
    var post = $(this).closest(".card");
    var stories = $(post).attr("stories-id");
    post.find(".content-wrap").toggleClass("is-hidden");
    post.find(".comments-wrap").toggleClass("is-hidden");
    window.scrollTo({
      top: offset(post[0]).top,
      behavior: "smooth"
    });
    $(".emojionearea-editor").keyup(function() {
      var counter = $(this).closest(".textarea-parent");
      counter.find(".counter .count").text(400 - $(this).val().length);
      $(this).height("auto");
      $(this).height($(this).prop("scrollHeight"));
    });
    $("input, textarea").val("");
    $(".emojionearea-editor").html("");
    $.ajax({
      url: "/stories/get-thread/",
      data: {
        stories: stories
      },
      type: "GET",
      cache: false,

      success: function(data) {
        if (data.thread) {
          if (data.thread.trim() != "")
            post.find(".comments-body").html(data.thread);
        }
        post.find("input[name=parent]").val(data.uuid);
      }
    });
    $(".comment-textarea").addClass("focused");
  });

  //Comment on a story
  $("a#post-comment-button").click(function() {
    // Ajax call to register a reply to any given Stories object.
    post = $(this).closest(".card");

    if (user != "") {
      $.ajax({
        url: "/stories/post-comment/",
        data: post.find(".replyStoriesForm").serialize(),
        type: "POST",
        cache: false,
        success: function() {
          post.find(".comment-textarea").val("");
          post
            .find(".comments-count .count")
            .html(parseInt(post.find(".comments-count .count").html(), 10) + 1);
          post.find(".content-wrap").toggleClass("is-hidden");
          post.find(".comments-wrap").toggleClass("is-hidden");
          var stories = $(post).attr("stories-id");
          $("input, textarea").val("");
          setTimeout(function() {
            $.ajax({
              url: "/stories/get-thread/",
              data: {
                stories: stories
              },
              cache: false,

              success: function(data) {
                if (data.thread.trim() != "")
                  post.find(".comments-body").html(data.thread);
                post.find("input[name=parent]").val(data.uuid);
              }
            });
            post.find(".content-wrap").toggleClass("is-hidden");
            post.find(".comments-wrap").toggleClass("is-hidden");
          }, 200);
        },
        error: function(data) {
          bootbox.alert(data.responseText);
        }
      });
    } else {
      window.location.href = "/accounts-authorization/login/";
    }
  });

  //Character count
  $("textarea").keyup(function() {
    var counter = $(this).closest(".textarea-parent");
    counter.find(".counter .count").text(400 - $(this).val().length);
    $(this).height("auto");
    $(this).height($(this).prop("scrollHeight"));
  });

  //Open publish mode
  $("#publish").on("click", function() {
    $(".app-overlay").addClass("is-active");
    $(".close-wrap").removeClass("d-none");
    $(".is-new-content").addClass("is-highlighted");
    $(".all-stories ").addClass("block-scroll");
  });

  //Enable and disable publish button based on the textarea value length (1)
  $("#publish").on("input", function() {
    var valueLength = $(this).val().length;

    if (valueLength >= 1 || $(".filelist").children().length > 0) {
      $("#publish-button").removeClass("is-disabled");
    } else {
      $("#publish-button").addClass("is-disabled");
    }
  });

  //Close compose box
  $(".close-publish").on("click", function() {
    $("body").trigger("resetUpload");
    //Clear text input
    $("input, textarea").val("");
    $(".app-overlay").removeClass("is-active");
    $(".is-new-content").removeClass("is-highlighted");
    $(".close-wrap").addClass("d-none");
    $(".all-stories ").removeClass("block-scroll");
  });

  //Show comments
  $(".infinite-container").on("click", ".is-comment", function() {
    // Ajax call to request a given Stories object detail and thread, and to
    // show it in a modal.
    var post = $(this).closest(".card");
    var stories = $(post).attr("stories-id");
    post.find(".content-wrap").addClass("is-hidden");
    post.find(".comments-wrap").removeClass("is-hidden");
    post.find("textarea").focus();

    $.ajax({
      url: "/stories/get-thread/",
      data: {
        stories: stories
      },
      cache: false,

      success: function(data) {
        if (data.thread.trim() != "")
          post.find(".comments-body").html(data.thread);
        post.find("input[name=parent]").val(data.uuid);
      }
    });
  });

  //
  $("body").on("uploadComplete", function(event) {
    $("#id_images").val(images);
    $("#id_video").val(storyVideo);
    $("#id_img_error").val(img_error);
    $.ajax({
      url: "/stories/post-stories/",
      data: $("#postStoriesForm").serialize(),
      type: "POST",
      cache: false,
      success: function(data) {
        //window.location.reload();
        $('[name="post"]').val("");
        $(".app-overlay").removeClass("is-active");
        $(".is-new-content").removeClass("is-highlighted");
        $(".close-wrap").addClass("d-none");
        feather.replace();
        $("#postStoriesForm")[0].reset();
        $("input, textarea").val("");
        $(".stream");
        $(".stream").prepend(data);
        lazyload();
      },
      error: function(data) {
        bootbox.alert(data.responseText);
      }
    });
  });

  $(".select-status button").click(function(e) {
    $("#selected-status #viewer-icon").html(
      $(this)
        .find("svg")
        .html()
    );
    $("#selected-status span").text(
      $(this)
        .find("h3")
        .text()
    );
    $("#viewers").val($(this).data("status"));
  });
  $(".dropdown-trigger").click(function(e) {
    e.preventDefault();
    $(".dropdown-trigger").toggleClass("is-active");
  });
  $("img").on("click", function() {
    $.ajax({
      type: "get",
      url:
        "/stories/story-images/?story_id=" +
        $(this)
          .closest("[stories-id]")
          .data("id"),
      success: function(response) {
        $.fancybox.open(response, {
          type: "image",
          loop: true
        });
      }
    });
  });
});
