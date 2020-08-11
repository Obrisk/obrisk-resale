/* -------------------------------------------------------------------------- */
/*                                    utils                                   */
/* -------------------------------------------------------------------------- */

function printError(msg, target) {
  template = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          ${msg}
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `;
  $(`${target}`).prepend(template);
}


$(function() {

  $("body").on("uploadComplete", function(event) {
    //Todo check if images where uploaded or empty
    $("input[name='status']").val("A");
    $("#id_images").val(images);
    $("#id_img_error").val(img_error);

    $.ajax({
      url: "/classifieds/write-new-classified/",
      data: $("form").serialize(),
      type: "POST",
      cache: false,
      success: function(data) {
        if (data.status == "200") {
          //This doesn't redirect smoothly
          window.location.replace("/classifieds/");
        } else {
          //At this point check if the images variable exists and
          //update the thumbnail holder to show the uploaded images.
          //Scroll the page to the top or to the place with errors.
          console.log(data);
          $(".alert-error").removeClass("d-none");
          $("#data-errors").html(data.error_message);
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      },
      error: function(data) {
          if (typeof data.error_message !== 'undefined') {
             printError(data.error_message, "#classified-form");
          }else {
             printError("Sorry we can't process your request, please try again later",
                "#classified-form");
          }
      }
    });
  });

  $("#addBtn").click(function() {
    $("#uploader").show();
  });

  $(".submit-button").click(function(event) {

    //Help the user to add the country code on phone number
    if (typeof $("#id_phone_number").val() !== 'undefined') {
        if ($("#id_phone_number").val().startsWith('+86') == false) {
            if ($("#id_phone_number").val().length == 11 ) {
                $("#id_phone_number").val("+86" + $("#id_phone_number").val());
            } else {
              printError(
                "Your phone number is incorrect, Please verify",
                "#classified-form"
              );
            }
        }
    }

    if (uploader.fileStats.totalFilesNum > 0) {
      if (images != "" && $("#id_images").val() == images) {
        $("body").trigger("uploadComplete");
      } else {
        $("body").trigger("submitClicked");
      }
    } else {
      printError(
        "Please provide all the details and upload at least 1 image",
        "#classified-form"
      );
    }
  });
});

