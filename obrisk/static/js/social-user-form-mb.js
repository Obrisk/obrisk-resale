//This is only for mobile web app:
//

var username_el = document.getElementById("id_username");
var username_err = document.getElementById('username-errors');

var verify_counter = 0;
var code_counter = 0;
var phone_no;

var confirm_btn = document.querySelector('#confirm');
var code_notice = document.getElementById("code-notice");
var send_code_btn = document.getElementById('send-code');
var results = document.getElementById('results');
var phone_number = document.getElementById('id_phone_number');
var verify_code_input = document.getElementById('verify-code');


document.addEventListener('DOMContentLoaded', function () {
    var len = username_el.value.length;
    username_el.setSelectionRange(len, len);
});


/* -------------------------------------------------------------------------- */
/*                               utils and libs                               */
/* -------------------------------------------------------------------------- */

//Print error message
function printError(msg) {
  template = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          ${msg}
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        `;
  $(".form-panel-top").prepend(template);
}


confirm_btn.addEventListener('click', function (event) {

    if (!document.getElementById('city').value ||
        !document.getElementById('province').value) {
          event.preventDefault();
          printError("Please enter your city and province!");

    } else if (username_el.value.length < 3 ||
      username_el.value.length > 16 || /\s/.test(username_el.value)) {
          event.preventDefault();
            username_err.innerHTML = "Must be 3 to 16 letters, without spaces!";
    } else {
        document.querySelector("#signup-panel-1").style.display = 'none';
        document.querySelector(".process-panel-wrap").classList.remove("is-active");
        document.querySelector("#signup-panel-2").classList.add("is-active");
     }
});



$(function() {
  send_code_btn.addEventListener('click', function (event) {
    if (!phone_number.value) {
      event.preventDefault();
        code_notice.innerHTML ="<p class='blue-link'>Empty input. Please enter a valid phone number!<p>";
    } else {
      var num = parseInt(phone_number.value);
      var str = num.toString();

      if (isNaN(num) || str.length != 11 || str.charAt(0) != 1) {
        event.preventDefault();
          code_notice.innerHTML = "<p class='blue-link'>Invalid number. Don't include country code/spaces/special characters<p>";
      } else {

        $.ajax({
          url: '/users/verification-code/',
          data: {
            phone_no: num
          },
          cache: false,
          type: "GET",
          success: function(data) {
            if (data.success == true) {
              timeout = 60;
              send_code_btn.setAttribute("disabled", true);
              $("#phone_label").hide();

              document.getElementById("code").classList.remove("d-none")
              //document.getElementById("cant-verify").classList.remove("d-none")

              if (data.message != undefined) {
                  code_notice.innerHTML = "<p class='blue-link'>" + data.message + "<p>";
                  verify_code_input.focus()
              }

              function updateSec() {
                timeout--;
                if (timeout > 0) {
                  send_code_btn.textContent = timeout + " S";
                } else {
                  send_code_btn.textContent = "Resend Code";
                  send_code_btn.setAttribute("disabled", false);
                }
              }
              // repeat with the interval of 1 seconds
              let timerId = setInterval(() => updateSec(), 1000);

              // after 60 seconds stop
              setTimeout(() => {
                clearInterval(timerId);
              }, 61000);

              verify_counter = verify_counter + 1;

              if (verify_counter >= 7) {
                send_code_btn.setAttribute("disabled", true);
                printError(
                  "Maximum number of sending SMS has reached, Try again later!"
                );
              }

              //$("#send-code").attr("disabled", false);
            } else {
              if (data.error_message != undefined) {
                code_notice.innerHTML = "<p class='blue-link'>" + data.error_message + "<p>";
              }
              if (data.messageId != undefined) {
                console.log(data.messageId);
              }
              if (data.requestId != undefined) {
                console.log(data.requestId);
              }
              if (data.returnedCode != undefined) {
                console.log(data.returnedCode);
              }
              if (data.retries != undefined) {
                console.log(data.retries);
              }
            }
          },
          error: function(err) {
              code_notice.innerHTML = "<p class='blue-link'> Sorry the signup is closed! Please try again later!<p>";
              console.log(err);
          }
        });
        return false;
      }
    }
  });


  username_el.addEventListener('keyup', e => {
      fetch(`/users/username-exists/?username=${e.target.value}`)
      .then (resp => resp.json())
      .then (data => {
          if (data.status == '201') {
            username_err.innerHTML= "This username is already taken!";
          }
          else {
            username_err.innerHTML="";
          }
      })
  });


  verify_code_input.addEventListener('keyup', e => {

    if (e.target.value.length == 6) {
      $(".loading").toggleClass("d-none");
      
      if (
          isNaN(verify_code_input.value) ||
          verify_code_input.value.length != 6 ||
          isNaN(phone_number.value) ||
          phone_number.value.length.toString() != 11 ||
          phone_number.value.charAt(0) != 1
      ) {
          event.preventDefault();
              results.innerHTML="<p class='blue-link'> The code is not correct!<p>";
      } else {

           $.ajax({
              url: "/users/cmplt-wx-reg-149eb8766awswdff224fgo029k12ol8/",
              data: Object.fromEntries(new FormData(document.querySelector("form"))),
              cache: false,
              type: "POST",
              success: function(data) {
                if (data.success == true) {
                    window.location.replace('/stories/');
                } else {
                      results.innerHTML="<p class='text-error '>" + data.error_message + "</p>" ;
                      send_code_btn.setAttribute("disabled", false);
                      code_counter = code_counter + 1;

                      if (code_counter >= 5) {
                        verify_code_input.setAttribute("disabled", true);
                        printError(
                          "Max number of code retrial has reached, Try again later!");
                      }
                   }
              },
              error: function(error) {
                printError(error);
              }
            });
          return false;
        }
      }
  //Close verify_code_input keyup listener function
  });
//Close jQuery function
});
