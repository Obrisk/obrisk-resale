$(function() {
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
      error = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          Please, Upload an image or write something!
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `;
      $(".compose").prepend(error);
    }
  });

  //Liker
  $(document.body).on("click", ".like-wrapper", function() {
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
          li.find(".like-button").toggleClass("is-active");
        }
      });
    } else {
      window.location.href = "/auth/login/";
    }

    return false;
  });

  //Cose comments
  $(document.body).on("click", ".close-comments", function() {
    // Ajax call to request a given Stories object detail and thread, and to
    // show it in a modal.
    var post = $(this).closest(".card");

    var stories = $(post).attr("stories-id");
    post.find(".post-media").removeClass("smaller");
    post.find(".comments-wrap").toggleClass("is-hidden");
  });

  //Show comments
  $(document.body).on("click", ".is-comment", function() {
    // Ajax call to request a given Stories object detail and thread, and to
    var post = $(this).closest(".card");
    var stories = $(post).attr("stories-id");
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
          if (data.thread.trim() != "") {
            post.find(".comments-body").html(data.thread);
          }
        }
        post.find("input[name=parent]").val(data.uuid);
      }
    });
    $(".comment-textarea").addClass("focused");
  });

  //Comment on a story
  $(document.body).on("click", "a#post-comment-button", function() {
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
          var comment_count = Number(
            post.find(".comments-heading small").text()
          );
          post.find(".comments-heading small").text(comment_count + 1);

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
          }, 200);
        },
        error: function(data) {
          error = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          Sorry we can't handle new comments, please try again later.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `;
          post.find(".card-footer .media-content").append(error);
        }
      });
    } else {
      window.location.href = "/auth/login/";
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
    $("#addVideo").show();
    $("#addBtn").show();
  });

  //Show comments
  $(document.body).on("click", ".is-comment", function() {
    // Ajax call to request a given Stories object detail and thread, and to
    // show it in a modal.
    var post = $(this).closest(".card");
    var stories = $(post).attr("stories-id");
    post.find(".post-media").addClass("smaller");
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
    $("#id_video").val(videos);
    $("#id_img_error").val(img_error);
    $.ajax({
      url: "/stories/post-stories/",
      data: $("#postStoriesForm").serialize(),
      type: "POST",
      cache: false,
      success: function(data) {
        $('[name="post"]').val("");
        $(".app-overlay").removeClass("is-active");
        $(".is-new-content").removeClass("is-highlighted");
        $(".close-wrap").addClass("d-none");
        feather.replace();
        $("#postStoriesForm")[0].reset();
        $("input, textarea").val("");
        $(".stream").prepend(data);
        lazyload();
        $("body").trigger("resetUpload");
      },
      error: function(data) {
        error = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          Sorry we can't handle new posts, please try again later.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `;
        $(".compose").prepend(error);
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
  $(document.body).on("click", "img", function() {
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
var shareMe = function shareMe(username, text, url) {
  navigator.share({
    title: `${username} shared a story on Obrisk`,
    text: `Shared: ${text}`,
    url: location.origin + "/stories/" + url
  });
};
$(document.body).on("click", ".delete-story", function() {
  location.href = $(this).attr("href");
});
