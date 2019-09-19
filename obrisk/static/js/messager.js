$(function () {

    function setUserOnlineOffline(username, status) {
        /* This function enables the client to switch the user connection
        status, allowing to show if an user is connected or not.
        */
        var elem = $(".online-stat");
        if (elem) {
            if (status === 'online') {
                $(".status-light").css('color', "#28a745");
                elem.text('online')
            } else {
                $(".status-light").css('color', "#ffc107");
                elem.text('offline')
            };
        };
    };

    function scrollMessages() {
        /* Set focus on the input box from the form, and rolls to show the
            the most recent message.
        */
        $("textarea[name='message']").focus();
        var d = $('.messages');
        d.scrollTop(d.prop("scrollHeight"));
    }

    function addNewMessage(message_id) {
        /* This function calls the respective AJAX view, so it will be able to
        load the received message in a proper way.
         */
        $.ajax({
            url: '/ws/messages/receive-message/',
            data: {
                'message_id': message_id
            },
            cache: false,
            success: function (data) {
                $(".send-message").before(data);
                scrollMessages();
            }
        });
    };

    $("#send").submit(function () {
        //disable send button after clicking 
        $(".send-btn").attr("disabled", true);
        $.ajax({
            url: '/ws/messages/send-message/',
            data: $("#send").serialize(),
            cache: false,
            type: 'POST',
            success: function (data) {
                //enable send button after message is sent
                $('.send-btn').removeAttr("disabled");
                $(".send-message").before(data);
                $('#send')[0].reset();
                $("textarea").val("");
                $("textarea[name='message']").focus();
                scrollMessages();
            }
        });
        return false;
    });



    //This helps the text in the textarea of the message to be send
    //when press enter and go new line with shift + enter!
    $("#sendText").keypress(function (e) {
        if (e.which == 13 && !e.shiftKey && !$('.send-btn').is('[disabled="disabled"]')) {
            $(this).closest("form").submit();
            e.preventDefault();
            return false;
        }
    });

    // WebSocket connection management block.
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/ws/messages/" + currentUser + "/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    window.onbeforeunload = function () {
        // Small function to run instruction just before closing the session.
        payload = {
            type: "recieve",
            sender: currentUser,
            set_status: "offline",
            key: "set_status"
        };
        webSocket.send(payload);
    }

    // Helpful debugging
    webSocket.socket.onopen = function () {
        // console.log("Connected to inbox stream");
        // Commenting this block until I find a better way to manage how to
        // report the user status.

        payload = {
            type: "recieve",
            sender: currentUser,
            set_status: "online",
            key: "set_status"
        };

        webSocket.send(payload);
    };

    webSocket.socket.onclose = function () {
        // console.log("Disconnected from inbox stream");
    };

    // onmessage management.
    webSocket.listen(function (event) {
        event = JSON.parse(event);
        switch (event.key) {
            case "message":
                if (event.sender === activeUser) {
                    addNewMessage(event.message_id);
                    // I hope there is a more elegant way to work this out.
                    setTimeout(function () {
                        $("#unread-count").hide()
                    }, 1);
                } else {
                    $("#new-message-" + event.sender).show();
                }
                break;

            case "set_status":
                setUserOnlineOffline(event.sender, event.set_status);
                break;

            default:
                break;
        }
    });
});