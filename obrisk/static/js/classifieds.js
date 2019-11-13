

$( function(){
    $("body").on("uploadComplete", function(event) {
        if (!images) {
            event.preventDefault();
            bootbox.alert("Please upload at least one image for your post!");
        } else {
            $("input[name='status']").val("A");
            $("#id_images").val(images);
            $("#id_img_error").val(img_error);
            
            $.ajax({
              url: "/classifieds/write-new-classified/",
              data: $("form").serialize(),
              type: "POST",
              cache: false,
              success: function(data) {
                if (data.readyState == 4 && (data.status == 302 || data.status == 301))  {
                   //This doesn't redirect smoothly 
                    window.location.href = "/classifieds";
                } else {
                    //At this point check if the images variable exists and 
                    //update the thumbnail holder to show the previous uploaded images.
                    //Scroll the page to the top or to the place with errors.
                    $('#classified-form-div').html(data);
                }

              },
              error: function(data) {
                bootbox.alert(data.responseText);
              }
          });
        }
      });
});