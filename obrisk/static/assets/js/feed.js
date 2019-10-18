/*! feed.js | Friendkit | © Css Ninja. 2018-2019 */

/* ==========================================================================
Feed page js file
========================================================================== */

$(document).ready(function () {

    "use strict";
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

})