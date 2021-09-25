/* -------------------------------------------------------------------------- */
/*                                    utils                                   */
/* -------------------------------------------------------------------------- */
const adminUrl = '/classifieds/wsguatpotlfwccdi/admin-write-new-classified/';

//Print error message
function printError(msg) {
  document.getElementsByClassName('notification')[0].classList.remove('is-hidden'); 
  document.getElementById('notf-msg').innerHTML = msg;
  window.scroll({
      top: 0, 
      left: 0, 
      behavior: 'smooth'
  });
}


document.addEventListener('DOMContentLoaded', function() {

  if (getCookie("classified")) {
     //cookie.replace(/["']/g, '')
     const classifiedArray = getCookie("classified")

     document.getElementById('id_title').value = classifiedArray[0]
     document.getElementById('id_details').value = classifiedArray[1]
     document.getElementById('id_price').value = classifiedArray[2]
  }

  document.querySelectorAll('.close-dj-messages').forEach(item => {
        item.addEventListener('click', e => {
            e.currentTarget.parentElement.classList.add('is-hidden');
            e.stopPropagation();
        });
  });

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
      url: adminUrl,
      data: $("form").serialize(),
      type: "POST",
      cache: false,
      success: function(data) {
        if (data.status == "200") {
            window.location.replace(adminUrl);
        } else {
          //At this point check if the images variable exists and
          //update the thumbnail holder to show the uploaded images.
          console.log(data);
          printError(data.error_message);
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      },
      error: function(data) {
          if (typeof data.error_message !== 'undefined') {
             printError(data.error_message);
          }else {
             printError(
                 "Sorry we can't process your request, please try again later"
             );
          }
      }
    });
  });

  document.querySelector("#addBtn").addEventListener('click', function() {
    $("#uploader").show();
  });

  document.querySelector("#chooseFile").addEventListener('click', function() {
    if (currentUser == undefined) {
      let draft_post = Object.fromEntries(new FormData(document.querySelector("form")));
      localStorage.setItem('new-classified', JSON.stringify(draft_post));
      window.location.replace('/auth/login/?next=/classifieds/write-new-classified/');
    }
  });


  document.getElementById("create-btn").addEventListener('click', function(event) {

      if (document.getElementById('id_title').value.length < 2 ) {
              printError(
                "Please provide the title"
              );
        } else {
              $("body").trigger("uploadComplete");

              try {
                const phn = document.getElementById("id_phone_number");
                if (phn !== null) {
                   if (phn.value !== '') {
                        if (phn.value.startsWith('+86') == false) {
                            if (phn.value.length === 11 ) {
                                phn.value ="+86" + phn.value;
                            } else {
                                  printError(
                                    "The phone number is incorrect, Please verify"
                                  );
                            }
                        }
                    }
                 } 
              } catch (error) {
                console.error(error);
              }

              localStorage.removeItem('new-classified');
              $("body").trigger("submitClicked");
        }
  });
});
