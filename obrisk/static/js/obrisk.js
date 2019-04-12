/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/


$('.form-group').removeClass('row');


/* Notifications JS basic client */
$(function () {
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
   });



    let emptyMessage = 'You have no unread notification';

    function checkNotifications() {
        $.ajax({
            url: 'wss://www.obrisk.com/ws/notifications/latest-notifications/',
            cache: false,
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function (data) {
                if (!data.includes(emptyMessage)) {
                    $("#notifications").addClass("btn-dark");
                }
            },
        });
    };


    checkNotifications();

    $('#notifications').popover({
        html: true,
        trigger: 'manual',
        container: "body" ,
        placement: "bottom",
    });

    $("#notifications").click(function () {
        if ($(".popover").is(":visible")) {
            $("#notifications").popover('hide');
            checkNotifications();
        }
        else {
            $("#notifications").popover('dispose');
            $.ajax({
                url: 'wss://www.obrisk.com/ws/notifications/latest-notifications/',
                cache: false,
                beforeSend: function(xhr, settings) {
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function (data) {
                    $("#notifications").popover({
                        html: true,
                        trigger: 'focus',
                        container: "body" ,
                        placement: "bottom",
                        content: data,
                    });
                    $("#notifications").popover('show');
                    $("#notifications").removeClass("btn-dark")
                },
            });
        }
        return false;
    });

     
    
    // Code block to manage WebSocket connections
    // Try to correctly decide between ws:// and wss://
    let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    let ws_path = "wss://www.obrisk.com/ws/notifications/";
    console.log( window.location.host);
    let webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // When debugging websockets uncomment these lines.
    // webSocket.socket.onopen = function () {
    //     console.log("Connected to " + ws_path);
    // };

    // webSocket.socket.onclose = function () {
    //     console.log("Disconnected from " + ws_path);
    // };

    // Listen the WebSocket bridge created throug django-channels library.
//     webSocket.listen(function(event) {
//         switch (event.key) {
//             case "notification":
//                 $("#notifications").addClass("btn-dark");
//                 break;

//             case "social_update":
//                 $("#notifications").addClass("btn-dark");
//                 update_social_activity(event.id_value);
//                 break;

//             case "additional_stories":
//                 if (event.actor_name !== currentUser) {
//                     $(".stream-update").show();
//                 }
//                 break;

//             default:
//                 // console.log('error: ', event);
//                 break;
//         };
//     });
});
