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

    $('#chooseFile').click(function() {
        $("#uploader").show();
    });
    
    $("body").on("uploadComplete", function(event) {
        //Todo check if images where uploaded or empty
        var imgs = images.split(',');
        for (var img in imgs) {
            $("#imgs-list").append("<p>" + " https://obrisk.oss-cn-hangzhou.aliyuncs.com/" + imgs[img]+ "</p>");
        }
    });
   
    $("#startImgUpload").click(function(event) {
        console.log("clicked");
        if (uploader.fileStats.totalFilesNum > 0) {
                $("body").trigger("submitClicked");
                console.log("submit trigged")
        } else {
            bootbox.alert("Please upload at least one image for your post");
        }
    });

});


// adding a crsf token
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
  $(function(){
    $(".comment-btn").click(function(event){
        event.preventDefault();
    
        $.ajax({
            method: 'POST',
            url: url,
            data : $('#commentForm').serialize(),
            processData: false,
            success: function(data){
                $('#comment-notify').html(data);
                $('#commentForm')[0].reset();
                location.reload();
            },
            error: function(err){
                console.log(err);
            }
        });
    });
});
});
