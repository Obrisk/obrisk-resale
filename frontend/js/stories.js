document.addEventListener('DOMContentLoaded', function () {

   //window.HELP_IMPROVE_VIDEOJS = false;

  //Hide create card on stories details, to focus on shared content
  if (document.getElementById('compose-card').classList.contains('is-hidden') &&
    window.location.href.endsWith('/stories/')) {
    document.getElementById('compose-card').classList.toggle('is-hidden');
  }

  function prepareTruncatedText(e) {
      if ('querySelector' in document && 
        'addEventListener' in window) {

        var fullTextWrapper = e.parentElement.querySelector('.fulltext');
        var toggleButtonText = e.parentElement.querySelector('.text');
        var shortText = e.parentElement.querySelector('#short-content');

        // change attributes and text if full text is shown/hidden
        if (!fullTextWrapper.hasAttribute('hidden')) {
            if (toggleButtonText.innerText == 'Less') {
                toggleButtonText.innerText = 'More';
            }
            fullTextWrapper.setAttribute('hidden', true);
            shortText.hidden = false;
        } else {
            if (toggleButtonText.innerText == 'More') {
                toggleButtonText.innerText = 'Less';
            }
            fullTextWrapper.removeAttribute('hidden');
            shortText.hidden = true;
        }
    }
  }

  //var page = 1;
  //var empty_page = false;
  //var block_request = false;
  //var is_tag_page = "{{tag}}";
  //if (is_tag_page == "None") {
   // $(window).scroll(function () {
    //  if (empty_page == false && block_request == false) {
     //   block_request = true;
      //  page += 1;
       // $('.loading').removeClass('is-hidden')
        //$.when(
         // $.get('?page=' + page, function (data) {
          //  if (data == '') {
           //     empty_page = true;
            //    $('.loading').addClass('is-hidden')
             //   $('.stream').append('<div class="m-auto"> End of Stories</div>')
           // } else {
            //    $('.loading').addClass('is-hidden');
             //   block_request = false;
              //  $('.stream').append(data);

               // loadvideo();
            //}

       //   })
      ////////  ).done(
    ////////      lazyload()
     ////////   )
   ////////   }
 ////////   });
 //////// }

  //$(' .post-text').linkify({ target: "_blank" });

  document.getElementById('replyStories').disabled = true;
  document.getElementById('replyInput').addEventListener('keyup', function () {
      document.getElementById('replyStories').disabled = this.value == "" ? true : false);
  });

  var infinite = new Waypoint.Infinite({
    element: document.querySelectorAll(".infinite-container")[0],
    onBeforePageLoad: function () {
      document.querySelector(".load").style.cssText += ';display:block !important;';
    },
    onAfterPageLoad: function () {
        document.querySelector(".load").style.display = 'hidden';
    },
  });

  function offset(el) {
    var rect = el.getBoundingClientRect(),
      scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
      scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    return { top: rect.top + scrollTop, left: rect.left + scrollLeft };
  }

  documentElement.querySelector("input, textarea").value = "";

  //Submit stories
  document.getElementsByClassName("submit-button")[0].addEventListener('click', function (e) {
        e.preventDefault();
        //check if text only
        if (uploader.fileStats.totalFilesNum > 0) {

            // Create a new event, allow bubbling
            const submitEv = new CustomEvent('submitClicked', {
              bubbles: true
            });

           //inside the document dispatches/triggers the event to fire
           //I can select the form instead of the body
           document.querySelector("body").dispatchEvent(submitEv); 

    } else if (document.getElementById("publish").value.substring(0, 20).length != 0) {

            // Create a new event, allow bubbling
            const uploadComp = new CustomEvent('uploadComplete', {
              bubbles: true
            });
           //inside the document dispatches/triggers the event to fire
           document.querySelector("body").dispatchEvent(uploadComp); 

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
  $(document.body).on("click", ".like-wrapper", function () {
    // Ajax call on action on like button.
    var li = $(this).closest(".card");
    var stories = $(li).attr("stories-id");
    if (user != "") {
      $.ajax({
        url: "/stories/like/",
        data: {
          stories: stories,
        },
        type: "GET",
        cache: false,
        success: function (data) {
          li.find(".like-button").addClass("is-active");
          li.find(".like-button .mdi").toggleClass("is-active");
          li.find(".likes-count .count").text(data.likes);
        },
      });
    } else {
      window.location.href = "/auth/login/";
    }

    return false;
  });

  //Cose comments
  $(document.body).on("click", ".close-comments", function () {
    // Ajax call to request a given Stories object detail and thread, and to
    // show it in a modal.
    var post = $(this).closest(".card");

    var stories = $(post).attr("stories-id");
    post.find(".post-media").removeClass("smaller");
    post.find(".comments-wrap").toggleClass("is-hidden");
  });

  //Show comments
  $(document.body).on("click", ".is-comment", function () {
    // Ajax call to request a given Stories object detail and thread, and to
    var post = $(this).closest(".card");
    var stories = $(post).attr("stories-id");
    post.find(".comments-wrap").toggleClass("is-hidden");
    window.scrollTo({
      top: offset(post[0]).top,
      behavior: "smooth",
    });
    $(".emojionearea-editor").keyup(function () {
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
        stories: stories,
      },
      type: "GET",
      cache: false,

      success: function (data) {
        if (data.thread) {
          if (data.thread.trim() != "") {
            post.find(".comments-body").html(data.thread);
          }
        }
        post.find("input[name=parent]").val(data.uuid);
      },
    });
    $(".comment-textarea").addClass("focused");
  });

  //Comment on a story
  $(document.body).on("click", "a#post-comment-button", function () {
    // Ajax call to register a reply to any given Stories object.
    post = $(this).closest(".card");

    if (user != "") {
      $.ajax({
        url: "/stories/post-comment/",
        data: post.find(".replyStoriesForm").serialize(),
        type: "POST",
        cache: false,
        success: function () {
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
          setTimeout(function () {
            $.ajax({
              url: "/stories/get-thread/",
              data: {
                stories: stories,
              },
              cache: false,

              success: function (data) {
                if (data.thread.trim() != "")
                  post.find(".comments-body").html(data.thread);
                post.find("input[name=parent]").val(data.uuid);
              },
            });
          }, 200);
        },
        error: function (data) {
          error = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          Sorry we can't handle new comments, please try again later.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `;
          post.find(".card-footer .media-content").append(error);
        },
      });
    } else {
      window.location.href = "/auth/login/";
    }
  });

  //Character count
  $("textarea").keyup(function () {
    var counter = $(this).closest(".textarea-parent");
    counter.find(".counter .count").text(400 - $(this).val().length);
    $(this).height("auto");
    $(this).height($(this).prop("scrollHeight"));
  });

  //Open publish mode
  $("#publish").on("click", function () {
    $(".app-overlay").addClass("is-active");
    $(".close-wrap").removeClass("is-hidden");
    $(".is-new-content").addClass("is-highlighted");
    $(".all-stories ").addClass("block-scroll");
  });

  //Enable and disable publish button based on the textarea value length (1)
  $("#publish").on("input", function () {
    var valueLength = $(this).val().length;

    if (valueLength >= 1 || $(".filelist").children().length > 0) {
      $("#publish-button").removeClass("is-disabled");
    } else {
      $("#publish-button").addClass("is-disabled");
    }
  });

  //Close compose box
  $(".close-publish").on("click", function () {
    $("body").trigger("resetUpload");
    //Clear text input
    $("input, textarea").val("");
    $(".app-overlay").removeClass("is-active");
    $(".is-new-content").removeClass("is-highlighted");
    $(".close-wrap").addClass("is-hidden");
    $(".all-stories ").removeClass("block-scroll");
    $("#addVideo").show();
    $("#addBtn").show();
  });

  //Show comments
  $(document.body).on("click", ".is-comment", function () {
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
        stories: stories,
      },
      cache: false,

      success: function (data) {
        if (data.thread.trim() != "")
          post.find(".comments-body").html(data.thread);
        post.find("input[name=parent]").val(data.uuid);
      },
    });
  });

  $("body").on("uploadComplete", function (event) {
    $("#id_images").val(images);
    $("#id_video").val(videos);
    $("#id_img_error").val(img_error);

    $.ajax({
      url: "/stories/post-stories/",
      data: $("#postStoriesForm").serialize(),
      type: "POST",
      cache: false,
      success: function (data) {
        $('[name="post"]').val("");
        $(".app-overlay").removeClass("is-active");
        $(".is-new-content").removeClass("is-highlighted");
        $(".close-wrap").addClass("is-hidden");
        feather.replace();
        $("#postStoriesForm")[0].reset();
        $("input, textarea").val("");
        $(".stream").prepend(data);
        lazyload();
        $("body").trigger("resetUpload");
      },
      error: function (data) {
        error = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          Sorry we can't handle new posts, please try again later.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `;
        $(".compose").prepend(error);
      },
    });
  });

  $(".select-status button").click(function (e) {
    $("#selected-status #viewer-icon").html($(this).find("svg").html());
    $("#selected-status span").text($(this).find("h3").text());
    $("#viewers").val($(this).data("status"));
  });
  $(".dropdown-trigger").click(function (e) {
    e.preventDefault();
    $(".dropdown-trigger").toggleClass("is-active");
  });

  $(document.body).on("click", ".stry-image", function () {
    $.ajax({
      type: "get",
      url:
        "/stories/story-images/?story_id=" +
        $(this).closest("[stories-id]").data("id"),
      success: function (response) {
        $.fancybox.open(response, {
          type: "image",
          loop: true,
        });
      },
    });
  });
});

var shareMe = function shareMe(username, text, url) {
  navigator.share({
    title: `${username} shared a story on Obrisk`,
    text: `Shared: ${text}`,
    url: location.origin + "/stories/" + url,
  });
};

$(document.body).on("click", ".delete-story", function () {
  location.href = $(this).attr("href");
});
