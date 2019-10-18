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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $("input, textarea").val('');

    $(".infinite-container").on("click", ".like-wrapper", function () {
        // Ajax call on action on like button.
        var li = $(this).closest(".card");
        var stories = $(li).attr("stories-id");

        $.ajax({
            url: '/stories/like/',
            data: {
                'stories': stories
            },
            type: 'GET',
            cache: false,
            success: function (data) {
                li.find(".likes-count .count").text(data.likes);

            }
        });
        return false;
    });

    //Cose comments
    $(".infinite-container").on("click", ".close-comments", function () {
        // Ajax call to request a given Stories object detail and thread, and to
        // show it in a modal.
        var post = $(this).closest(".card");
        var stories = $(post).attr("stories-id");
        post.find('.content-wrap').toggleClass('is-hidden');
        post.find('.comments-wrap').toggleClass('is-hidden')
    });


    //Show comments
    $(".infinite-container").on("click", ".is-comment", function () {
        // Ajax call to request a given Stories object detail and thread, and to
        // show it in a modal.
        var post = $(this).closest(".card");
        var stories = $(post).attr("stories-id");
        post.find('.content-wrap').toggleClass('is-hidden');
        post.find('.comments-wrap').toggleClass('is-hidden');
        $("textarea").keyup(function () {
            var counter = $(this).closest(".textarea-parent");
            counter.find(".counter .count").text(400 - $(this).val().length);
            $(this).height('auto');
            $(this).height($(this).prop('scrollHeight'));
        });
        $("input, textarea").val('');
        $('.emojionearea-editor').html("");
        $.ajax({
            url: '/stories/get-thread/',
            data: {
                'stories': stories
            },
            cache: false,

            success: function (data) {
                if (data.thread.trim() != "")
                    post.find(".comments-body").html(data.thread);
                post.find("input[name=parent]").val(data.uuid)
            }
        });
        $('.comment-textarea').addClass("focused");
    });

    //Comment on a story
    $("a#post-comment-button").click(function () {
        // Ajax call to register a reply to any given Stories object.
        post = $(this).closest('.card');
        $.ajax({
            url: '/stories/post-comment/',
            data: post.find(".replyStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function () {
                post.find(".comment-textarea").val("");
                post.find('.comments-count .count').html(parseInt(post.find('.comments-count .count').html(), 10) + 1);
                post.find('.content-wrap').toggleClass('is-hidden');
                post.find('.comments-wrap').toggleClass('is-hidden');
                var stories = $(post).attr("stories-id");
                $("input, textarea").val('');
                setTimeout(function () {
                    $.ajax({
                        url: '/stories/get-thread/',
                        data: {
                            'stories': stories
                        },
                        cache: false,

                        success: function (data) {
                            if (data.thread.trim() != "")
                                post.find(".comments-body").html(data.thread);
                            post.find("input[name=parent]").val(data.uuid)
                        }
                    });
                    post.find('.content-wrap').toggleClass('is-hidden');
                    post.find('.comments-wrap').toggleClass('is-hidden');

                }, 200);
            },
            error: function (data) {
                bootbox.alert(data.responseText);
            },
        });

    });

    //Character count 
    $("textarea").keyup(function () {
        var counter = $(this).closest(".textarea-parent");
        counter.find(".counter .count").text(400 - $(this).val().length);
        $(this).height('auto');
        $(this).height($(this).prop('scrollHeight'));
    });

    //Open publish mode
    $('#publish').on('click', function () {
        $('.app-overlay').addClass('is-active');
        $('.close-wrap').removeClass('d-none');
        $('.is-new-content').addClass('is-highlighted');

    });
    //Enable and disable publish button based on the textarea value length (1)
    $('#publish').on('input', function () {
        var valueLength = $(this).val().length;

        if (valueLength >= 1) {
            $('#publish-button').removeClass('is-disabled');
        } else {
            $('#publish-button').addClass('is-disabled');
        }
    })
    $("#publish-button").click(function () {
        // Ajax call after pushing button, to register a Stories object.
        $.ajax({
            url: '/stories/post-stories/',
            data: $("#postStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".infinite-container").prepend(data);
                $('[name="post"]').val("");
                $('.app-overlay').removeClass('is-active');
                $('.is-new-content').removeClass('is-highlighted');
                $('.close-wrap').addClass('d-none');
                feather.replace();
            },
            error: function (data) {
                bootbox.alert(data.responseText);
            },
        });
    });
    //Close compose box
    $('.close-publish').on('click', function () {
        $('.app-overlay').removeClass('is-active');
        $('.is-new-content').removeClass('is-highlighted');
        $('.close-wrap').addClass('d-none');
    });
    //Comment on a story
    $(".comment-button").click(function () {
        // Ajax call to register a reply to any given Stories object.
        $.ajax({
            url: '/stories/post-comment/',
            data: $("#replyStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function () {
                $(".comment-textarea").val("");
                $('.is-comment-count').html(parseInt($('.is-comment-count').html(), 10) + 1);
            },
            error: function (data) {
                bootbox.alert(data.responseText);
            },
        });
    });
    //Show comments
    $(".infinite-container").on("click", ".is-comment", function () {
        // Ajax call to request a given Stories object detail and thread, and to
        // show it in a modal.
        var post = $(this).closest(".card");
        var stories = $(post).attr("stories-id");
        post.find('.content-wrap').toggleClass('is-hidden');
        post.find('.comments-wrap').toggleClass('is-hidden')

        $.ajax({
            url: '/stories/get-thread/',
            data: {
                'stories': stories
            },
            cache: false,

            success: function (data) {
                if (data.thread.trim() != "")
                    post.find(".comments-body").html(data.thread);
                post.find("input[name=parent]").val(data.uuid)
            }
        });
    });
});