$(document).ready(function () {
    $(".notifications").click(function () {

        $(".recent-notifications").html('');
        $.ajax({
            url: '/ws/notifications/latest-notifications/',
            success: function (data) {
                $(".recent-notifications").html(data);
            },
        });

        return false;
    });

});