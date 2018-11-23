$(function () {
    $(".publish").click(function () {
        $("input[name='status']").val("P");
        $("#posts-form").submit();
    });

    $(".update").click(function () {
        $("input[name='status']").val("P");
        //$("input[name='edited']").prop("checked");
        $("input[name='edited']").val("True");
        $("#posts-form").submit();
    });

    $(".draft").click(function () {
        $("input[name='status']").val("D");
        $("#posts-form").submit();
    });
});
