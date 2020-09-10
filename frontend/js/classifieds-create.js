/* -------------------------------------------------------------------------- */
/*                                    utils                                   */
/* -------------------------------------------------------------------------- */

function printError(msg, target) {
  template = `
        <div class="notification is-danger" role="alert">
            <button type="button" class="delete close-dj-messages"></button>
          ${msg}
        </div>
        `;
  $(`${target}`).prepend(template);
}


$(function() {

  const new_classified = JSON.parse(localStorage.getItem('new-classified'));

  if (new_classified) {
      document.getElementById('id_title').value = new_classified.title;
      document.getElementById('id_details').value = new_classified.details;
      document.getElementById('id_price').value = new_classified.price;
  }

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
            window.location.replace("/classifieds/");
        } else {
          //At this point check if the images variable exists and
          //update the thumbnail holder to show the uploaded images.
          //Scroll the page to the top or to the place with errors.
          console.log(data);
          printError(data.error_message, "#classified-form");
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
    const phn = document.getElementById("id_phone_number");
    //Help the user to add the country code on phone number
    if ((typeof phn !== 'undefined') && phn != '') {
        if (phn.value.startsWith('+86') == false) {
            if (phn.value.length == 11 ) {
                phn.value ="+86" + phn.value;
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
  
  if ( user === '' ) {
      document.getElementsByClassName('login-to-post')[0].addEventListener('click', function () {
          let draft_post = Object.fromEntries(new FormData(document.querySelector("form")));
          localStorage.setItem('new-classified', JSON.stringify(draft_post));
      });
  }

  document.getElementById('cancel-classified').addEventListener('click', function () {
      localStorage.removeItem('new-classified');
  });
});
