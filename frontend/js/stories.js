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
       // $('.loading').classList.remove('is-hidden')
        //$.when(
         // $.get('?page=' + page, function (data) {
          //  if (data == '') {
           //     empty_page = true;
            //    $('.loading').classList.add('is-hidden')
             //   $('.stream').append('<div class="m-auto"> End of Stories</div>')
           // } else {
            //    $('.loading').classList.add('is-hidden');
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
    if (this.value == "") { 
      document.getElementById('replyStories').disabled = true;
    } else {
      document.getElementById('replyStories').disabled = false;
    }
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

           document.querySelector("body").dispatchEvent(
               new CustomEvent('submitClicked', {
                  bubbles: true
               })
           );

       } else if (document.getElementById("publish").value.substring(0, 20).length != 0) {

           document.querySelector("body").dispatchEvent(
               new CustomEvent('uploadComplete', {
                  bubbles: true
              })
           );

       } else {
          error = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
              Please, Upload an image or write something!
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>`;
          document.getElementsByClassName("compose")[0].insertAdjacentHTML('beforeend', error);
      }
  });

  //Liker
  document.getElementsByClassName("like-wrapper").addEventListener('click', function () {
    // Ajax call on action on like button.
    const li = document.querySelector(this).closest(".card");
    const stories = document.querySelector(li).getAttribute("stories-id");
    if (user != "") {

      fetch(`/stories/like/?stories=${stories}`)
      .then (resp => resp.json())
      .then (data => {
          li.querySelectorAll(".like-button").classList.add("is-active");
          li.querySelectorAll(".like-button .mdi").classList.toggle("is-active");
          li.querySelectorAll(".likes-count .count").textContent(data.likes);
      });

    } else {
      window.location.href = "/auth/login/";
    }

    return false;
  });

  //Close comments
  document.getElementsByClassName("close-comments").addEventListener('click', function () {
    // Ajax call to request a given Stories object detail and thread, and to
    // show it in a modal.
    const post = document.querySelector(this).closest(".card");

    const stories = document.querySelector(post).getAttribute("stories-id");
    post.querySelectorAll(".post-media").classList.remove("smaller");
    post.querySelectorAll(".comments-wrap").classList.toggle("is-hidden");
  });

  //Show comments
  document.querySelector(".is-comment").addEventListener("click", function () {
    // Ajax call to request a given Stories object detail and thread
    var post = this.closest(".card");
    var stories = post.getAttribute("stories-id");
    post.querySelector(".comments-wrap").classList.toggle("is-hidden");
    window.scrollTo({
      top: offset(post[0]).top,
      behavior: "smooth",
    });

    document.querySelector(".emojionearea-editor").addEventListener("keyup", function () {
      var counter = this.closest(".textarea-parent");
      counter.querySelector(".counter .count").textContent(400 - this.value.length);
      this.style.height = "auto";
      //this.height(this.prop("scrollHeight"));
      this.style.height=this.scrollHeight;
    });

    document.querySelector("input, textarea").value="";
    document.querySelector(".emojionearea-editor").innerHTML= "";

      fetch(`/stories/get-thread/?stories=${stories}`)
      .then (resp => resp.json())
      .then (data => {
            if (data.thread) {
              if (data.thread.trim() != "") {
                post.querySelectorAll(".comments-body").innerHTML=data.thread;
              }
            }
            post.querySelector("input[name=parent]").value=data.uuid;
      });

    document.querySelector(".comment-textarea").classList.add("focused");
  });

  //Comment on a story
  document.querySelector('a#post-comment-button').addEventListener("click", function () {
    // Ajax call to register a reply to any given Stories object.
    post = this.closest(".card");

    if (user != "") {

        //'csrfmiddlewaretoken': document.querySelector(
                   //'#csrf-helper input[name="csrfmiddlewaretoken"]'
              // ).getAttribute('value')

    fetch('/stories/post-comment/', {
        method: 'POST',
        body: post.querySelectorAll(".replyStoriesForm").serialize(),
        credentials: 'same-origin'
    }).then(function(response) {
        // with the response, parse to text, then pass it along
        response.text().then(function(data) {
          post.querySelectorAll(".comment-textarea").value("");
          post
            .querySelectorAll(".comments-count .count")
            .html(parseInt(post.querySelectorAll(".comments-count .count").html(), 10) + 1);
          var comment_count = Number(
            post.querySelectorAll(".comments-heading small").textContent()
          );
          post.querySelectorAll(".comments-heading small").textContent(comment_count + 1);

          var stories = $(post).attr("stories-id");
          $("input, textarea").value("");
          setTimeout(function () {
            $.ajax({
              url: "/stories/get-thread/",
              data: {
                stories: stories,
              },
              cache: false,

              success: function (data) {
                if (data.thread.trim() != "")
                  post.querySelectorAll(".comments-body").html(data.thread);
                post.querySelectorAll("input[name=parent]").value(data.uuid);
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
          post.querySelectorAll(".card-footer .media-content").append(error);
        },
      });
    } else {
      window.location.href = "/auth/login/";
    }
  });
        });
    });



      $.ajax({
        success: function () {

  //Character count
  $("textarea").keyup(function () {
    var counter = this.closest(".textarea-parent");
    counter.querySelectorAll(".counter .count").textContent(400 - this.value.length);
    this.height("auto");
    this.height(this.prop("scrollHeight"));
  });

  //Open publish mode
  $("#publish").on("click", function () {
    $(".app-overlay").classList.add("is-active");
    $(".close-wrap").classList.remove("is-hidden");
    $(".is-new-content").classList.add("is-highlighted");
    $(".all-stories ").classList.add("block-scroll");
  });

  //Enable and disable publish button based on the textarea value length (1)
  $("#publish").on("input", function () {
    var valueLength = this.value.length;

    if (valueLength >= 1 || $(".filelist").children().length > 0) {
      $("#publish-button").classList.remove("is-disabled");
    } else {
      $("#publish-button").classList.add("is-disabled");
    }
  });

  //Close compose box
  $(".close-publish").on("click", function () {
    $("body").trigger("resetUpload");
    //Clear text input
    $("input, textarea").value("");
    $(".app-overlay").classList.remove("is-active");
    $(".is-new-content").classList.remove("is-highlighted");
    $(".close-wrap").classList.add("is-hidden");
    $(".all-stories ").classList.remove("block-scroll");
    $("#addVideo").show();
    $("#addBtn").show();
  });

  //Show comments
  $(document.body).on("click", ".is-comment", function () {
    // Ajax call to request a given Stories object detail and thread, and to
    // show it in a modal.
    var post = this.closest(".card");
    var stories = $(post).attr("stories-id");
    post.querySelectorAll(".post-media").classList.add("smaller");
    post.querySelectorAll(".comments-wrap").classList.remove("is-hidden");
    post.querySelectorAll("textarea").focus();

    $.ajax({
      url: "/stories/get-thread/",
      data: {
        stories: stories,
      },
      cache: false,

      success: function (data) {
        if (data.thread.trim() != "")
          post.querySelectorAll(".comments-body").html(data.thread);
        post.querySelectorAll("input[name=parent]").value(data.uuid);
      },
    });
  });

  $("body").on("uploadComplete", function (event) {
    $("#id_images").value(images);
    $("#id_video").value(videos);
    $("#id_img_error").value(img_error);

    $.ajax({
      url: "/stories/post-stories/",
      data: $("#postStoriesForm").serialize(),
      type: "POST",
      cache: false,
      success: function (data) {
        $('[name="post"]').value("");
        $(".app-overlay").classList.remove("is-active");
        $(".is-new-content").classList.remove("is-highlighted");
        $(".close-wrap").classList.add("is-hidden");
        feather.replace();
        $("#postStoriesForm")[0].reset();
        $("input, textarea").value("");
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
    $("#selected-status #viewer-icon").html(this.querySelectorAll("svg").html());
    $("#selected-status span").textContent(this.querySelectorAll("h3").textContent());
    $("#viewers").value(this.data("status"));
  });
  $(".dropdown-trigger").click(function (e) {
    e.preventDefault();
    $(".dropdown-trigger").classList.toggle("is-active");
  });

  $(document.body).on("click", ".stry-image", function () {
    $.ajax({
      type: "get",
      url:
        "/stories/story-images/?story_id=" +
        this.closest("[stories-id]").data("id"),
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
  location.href = this.attr("href");
});
