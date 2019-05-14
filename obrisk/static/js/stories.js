$(function () {
    function getCookie(name) {
        // Function to get any cookie available in the session.
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
  
    // This sets up every ajax call with proper headers.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function hide_stream_update() {
        $(".stream-update").hide();
    };


    // Focus on the modal input by default.
    $('#storiesFormModal').on('shown.bs.modal', function () {
        $('#storiesInput').trigger('focus')
    });

    $('#storiesThreadModal').on('shown.bs.modal', function () {
        $('#replyInput').trigger('focus')
    });

    // Counts textarea characters to provide data to user.
    $("#storiesInput").keyup(function () {
        var charCount = $(this).val().length;
        $("#storiesCounter").text(280 - charCount);
    });

    $("#replyInput").keyup(function () {
        var charCount = $(this).val().length;
        $("#replyCounter").text(280 - charCount);
    });

    $("input, textarea").attr("autocomplete", "off");

    $("#postStories").click(function () {
        // Ajax call after pushing button, to register a Stories object.
        $.ajax({
            url: '/stories/post-stories/',
            data: $("#postStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $("ul.stream").prepend(data);
                $("#storiesInput").val("");
                $("#storiesFormModal").modal("hide");
                hide_stream_update();
            },
            error : function(data){
                alert(data.responseText);
            },
        });
    });

    $("#replyStories").click(function () {
        // Ajax call to register a reply to any given Stories object.
        $.ajax({
            url: '/stories/post-comment/',
            data: $("#replyStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $("#replyInput").val("");
                $("#storiesThreadModal").modal("hide");
                location.reload();
            },
            error: function(data){
                alert(data.responseText);
            },
        });
    });

    $("ul.stream").on("click", ".like", function () {
        // Ajax call on action on like button.
        var li = $(this).closest("li");
        var stories = $(li).attr("stories-id");
       
        $.ajax({
            url: '/stories/like/',
            data: { 'stories': stories },
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like .like-count", li).text(data.likes);
                if ($(".like .heart", li).hasClass("fa fa-heart")) {
                    $(".like .heart", li).removeClass("fa fa-heart");
                    $(".like .heart", li).addClass("fa fa-heart-o");
                } else {
                    $(".like .heart", li).removeClass("fa fa-heart-o");
                    $(".like .heart", li).addClass("fa fa-heart");
                }
            }
        });
        return false;
    });

    $("ul.stream").on("click", ".comment", function () {
        // Ajax call to request a given Stories object detail and thread, and to
        // show it in a modal.
        var post = $(this).closest(".card");
        var stories = $(post).closest("li").attr("stories-id");
        $("#storiesThreadModal").modal("show");
        $.ajax({
            url: '/stories/get-thread/',
            data: {'stories': stories},
            cache: false,
            beforeSend: function () {
                $("#threadContent").html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
            },
            success: function (data) {
                $("input[name=parent]").val(data.uuid)
                $("#storiesContent").html(data.stories);
                $("#threadContent").html(data.thread);
            }
        });
        return false;
    });
});


/* Example query for the GraphQL endpoint.

    query{
        stories(uuidId: "--insert here the required uuid_id value for the lookup"){
          uuidId
          content
          timestamp
          countThread
          countLikers
          user {
            name
            picture
          }
          liked {
            name
          }
          thread{
            content
          }
        }
        paginatedStories(page: 1){
          page
          pages
          hasNext
          hasPrev
          objects {
            uuidId
            content
            timestamp
            countThread
            countLikers
            user {
              name
              picture
            }
            liked {
              name
            }
            thread{
              content
            }
          }
        }
      }
 */
