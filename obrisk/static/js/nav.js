    $(document).ready(function () {
        $("#notifications").click(function () {
            console.log('clicked');
            $("#recent-notifications").html('');
            $.ajax({
                url: '/ws/notifications/latest-notifications/',
                success: function (data) {
                    $("#recent-notifications").html(data);
                },
            });

            return false;
        });
    });