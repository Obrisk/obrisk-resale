$(function () {
    $(".publish").click(function () {
        $("input[name='status']").val("P");
        $("#classified-form").submit();
    });

    $(".update").click(function () {
        $("input[name='status']").val("P");
        //$("input[name='edited']").prop("checked");
        $("input[name='edited']").val("True");
        $("#classified-form").submit();
    });

    $(".draft").click(function () {
        $("input[name='status']").val("D");
        $("#classified-form").submit();
    });
});
