$(function () {
    $(".create").click(function () {
        $("input[name='status']").val("A");
        $("#classified-form").submit();
    });

    $(".update").click(function () {
        $("input[name='status']").val("A");
        //$("input[name='edited']").prop("checked");
        $("input[name='edited']").val("True");
        $("#classified-form").submit();
    });

    $(".draft").click(function () {
        $("input[name='status']").val("D");
        $("#classified-form").submit();
    });
});
