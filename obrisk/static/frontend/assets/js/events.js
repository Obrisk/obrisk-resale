/*! events.js | Friendkit | © Css Ninja. 2018-2019 */

/* ==========================================================================
Events page js file
========================================================================== */

$(document).ready(function () {

    "use strict";

    if ($('#events-page').length) {

        //Scroll to desired event
        $(".scroll-link").on('click', function (e) {
            e.preventDefault();
            $(this).siblings('.scroll-link').removeClass('is-active');
            $(this).addClass('is-active');
            var id = $(this).attr('data-event-id');
            var parentId = $('#event-list');
            $('html, body').animate({
                scrollTop: ($('#' + id).offset().top - 58)
            }, 500);
        });
    }

})