//This is only for mobile web app:

const username_el = document.getElementById("id_username");
const username_err = document.getElementById('username-errors');

var verify_counter = 0;
var code_counter = 0;
var phone_no;

const confirm_btn = document.querySelector('#confirm');
const code_notice = document.getElementById("code-notice");
const send_code_btn = document.getElementById('send-code');
const results = document.getElementById('results');
const phone_number = document.getElementById('id_phone_number');
const verify_code_input = document.getElementById('verify-code');

const panel_two = document.getElementById('signup-panel-2');
const request_unverify = document.getElementById('request-unverified-phone');
const unverify_form = document.getElementById('unverify-form');
const signup_loading = document.getElementById('signup-loading-popup');


/* -------------------------------------------------------------------------- */
/*                               utils and libs                               */
/* -------------------------------------------------------------------------- */

//Print error message
function printError(msg) {
  document.getElementsByClassName('notification')[0].classList.remove('is-hidden'); 
  document.getElementById('notf-msg').innerHTML = msg;
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
        document.querySelector("#signup-panel-2").classList.remove("is-hidden");
        document.querySelector("#signup-panel-2").classList.add("is-active");
     }
});


document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.close-dj-messages').forEach(item => {
        item.addEventListener('click', e => {
            e.currentTarget.parentElement.classList.add('is-hidden');
            e.stopPropagation();
        });
    });

    var len = username_el.value.length;
    username_el.setSelectionRange(len, len);

  send_code_btn.addEventListener('click', function (event) {
    if (!phone_number.value) {
      event.preventDefault();
        code_notice.innerHTML ="<p class='error-text'>Please enter a valid phone number!<p>";
    } else {
      var num = parseInt(phone_number.value);
      var str = num.toString();

      if (isNaN(num) || str.length != 11 || str.charAt(0) != 1) {
        event.preventDefault();
          code_notice.innerHTML = "<p class='error-text'>Don't enter country code or special characters<p>";
      } else {

        $.ajax({
          url: '/users/verification-code/',
          data: {
            phone_no: num
          },
          cache: false,
          type: "GET",
          success: function(data) {
            if (data.success === true) {
              timeout = 60;
              send_code_btn.disabled = true;

              document.getElementById("code").classList.remove("is-hidden")

              if (data.message != undefined) {
                  code_notice.innerHTML = "<p class='pass-text'>" + data.message + "<p>";
                  verify_code_input.focus()
              }

              function updateSec() {
                timeout--;
                if (timeout > 0) {
                  send_code_btn.textContent = timeout + " S";

                    if (timeout === 30 && verify_code_input.value === "") {
                        request_unverify.style.cssText += ';display:block !important;';
                    }

                } else {
                    send_code_btn.textContent = "Resend Code";
                    send_code_btn.disabled = false;
                    verify_code_input.disabled = false;
                    
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
                send_code_btn.disabled = true;
                printError(
                  "Maximum number of sending SMS has reached, Try again later!"
                );
              }

              //$("#send-code").attr("disabled", false);
            } else {
              if (data.error_message != undefined) {
                code_notice.innerHTML = "<p class='error-text'>" + data.error_message + "<p>";
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
              code_notice.innerHTML = "<p class='error-text'> The signup is closed! Please try again later!<p>";
              console.log(err);
          }
        });
        return false;
      }
    }
  });

  request_unverify.addEventListener('click', e => {
      unverify_form.style.cssText += ';display:block !important;';
      document.getElementById('id_notes').focus();
      panel_two.classList.remove('blur-out');
      panel_two.classList.add('blur-in');
      e.stopPropagation();

  });

  document.getElementById('close-unverify-form').addEventListener('click', e => {
          unverify_form.style.display = 'none';
          panel_two.classList.remove('blur-in');
          panel_two.classList.add('blur-out');
          e.stopPropagation();
  });

  username_el.addEventListener('keyup', e => {
      fetch(`/users/username-exists/?username=${e.target.value}`)
      .then (resp => resp.json())
      .then (data => {
          if (data.status === '201') {
            username_err.innerHTML= "This username is already taken!";
            confirm_btn.disabled = true;
          }
          else {
            username_err.innerHTML="";
            confirm_btn.disabled = false;
          }
      })
  });

  function submitForm() {
       $.ajax({
          url: "/users/cmplt-wx-reg-149eb8766awswdff224fgo029k12ol8/",
          data: Object.fromEntries(new FormData(document.querySelector("form"))),
          cache: false,
          type: "POST",
          success: function(data) {
            if (data.success === true) {
                window.location.replace('/classifieds/');
            } else {
                  results.innerHTML="<p class='error-text'>" + data.error_message + "</p>" ;
                  signup_loading.style.display = 'none';
                  send_code_btn.disabled = false;
                  verify_code_input.disabled = false;
                  document.getElementById('verify-code').disabled = false;
                  unverify_form.style.display = 'none';
                  panel_two.classList.remove('blur-in');
                  panel_two.classList.add('blur-out');
                  code_counter = code_counter + 1;

                  if (code_counter >= 5) {
                    verify_code_input.disabled = true;
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

  function submitVerifyCode() {
      document.getElementsByClassName("loading")[0].classList.remove("is-hidden");

      if (
          isNaN(verify_code_input.value) ||
          verify_code_input.value.length !== 6 ||
          isNaN(phone_number.value)
      ) {
          event.preventDefault();
              results.innerHTML="<p class='error-text'> The code or number is not correct!<p>";
      } else {

          if (phone_number.value.toString().startsWith("+86") === false) {
              phone_number.value = "+86" + phone_number.value;
          }
          signup_loading.style.display = 'flex';
          submitForm();
          return false;
      }
  }

  verify_code_input.addEventListener('keyup', e => {
      if (verify_code_input.value.length === 6) {
        submitVerifyCode();
      }
  });

  document.getElementById('submit-code').addEventListener('click', e => {
    submitVerifyCode();
  });

  document.getElementById('cant-verify-submit').addEventListener('click', e => {

          if (
              isNaN(phone_number.value) ||
              phone_number.value.length.toString() != 11 ||
              phone_number.value.charAt(0) != 1
          ) {
                  e.preventDefault();
                  results.innerHTML="<p class='error-text'> The phone number is not correct!<p>";
                  unverify_form.style.display = 'none';
                  panel_two.classList.remove('blur-in');
                  panel_two.classList.add('blur-out');
                  e.stopPropagation();
          } else {
               document.getElementById('id_unverified_phone').value = phone_number.value;
               phone_number.value = "";
               signup_loading.style.display = 'flex';
               submitForm();
               return false;
          }

    });
//Close jQuery function
});
