$( function(){
    $("body").on("uploadComplete", function(event) {
       //Todo check if images where uploaded or empty
            $("input[name='status']").val("A");
            console.log(images);
            $("#id_images").val(images);
            $("#id_img_error").val(img_error);
            
            $.ajax({
              url: "/classifieds/write-new-classified/",
              data: $("form").serialize(),
              type: "POST",
              cache: false,
              success: function(data) {
                if (data.status == '200')  {
                   //This doesn't redirect smoothly 
                    window.location.replace("/classifieds");
                } else {
                    //At this point check if the images variable exists and 
                    //update the thumbnail holder to show the previous uploaded images.
                    //Scroll the page to the top or to the place with errors.
                    $('#data-errors').html(data.error_message);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }

              },
              error: function(data) {
                bootbox.alert(data.responseText);
              }
          });
        
      });
});