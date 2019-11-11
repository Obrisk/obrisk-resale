

$( function(){
    $("body").on("uploadComplete", function(event) {
        $("#id_images").val(images);
        $("#id_img_error").val(img_error);
        $.ajax({
          url: "/classifieds/write-new-classified/",
          data: $("form").serialize(),
          type: "POST",
          cache: false,
          success: function(data) {
            window.location.href("/classifieds");

          },
          error: function(data) {
            bootbox.alert(data.responseText);
          }
        });
      });
});