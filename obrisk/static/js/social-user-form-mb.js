//This is only for mobile web app:
//

var username_el = document.getElementById("id_username");
var username_err = document.getElementById('username-errors');

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
  $(".form-panel").prepend(template);
}

var verify_counter = 0;
var code_counter = 0;

var phone_no;

var confirm_btn = document.querySelector('#confirm');

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
  $("#send-code").click(function(event) {
    if (!$("#id_phone_number").val()) {
      event.preventDefault();
      $("#code-notice")
        .empty()
        .append(
          "<p class='blue-link'>Empty input. Please enter a valid phone number!<p>"
        );
    } else {
      var num = parseInt($("#id_phone_number").val());
      var str = num.toString();

      if (isNaN(num) || str.length != 11 || str.charAt(0) != 1) {
        event.preventDefault();
        $("#code-notice")
          .empty()
          .append(
            "<p class='blue-link'>Invalid number. Don't include country code/spaces/special characters<p>");
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
              $("#send-code").attr("disabled", true);
              $("#phone_label").hide();

              document.getElementById("code").classList.remove("d-none")
              //document.getElementById("cant-verify").classList.remove("d-none")

              if (data.message != undefined) {
                $("#code-notice")
                  .empty()
                  .append("<p class='blue-link'>" + data.message + "<p>");
                  document.getElementById("code-input").focus()
              }

              function updateSec() {
                timeout--;
                if (timeout > 0) {
                  $("#send-code").text(timeout + " S");
                } else {
                  $("#send-code").text("Get Code");
                  $("#send-code").attr("disabled", false);
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
                $("#send-code").attr("disabled", true);
                printError(
                  "Maximum number of sending SMS has reached, Try again later!"
                );
              }

              //$("#send-code").attr("disabled", false);
            } else {
              if (data.error_message != undefined) {
                $("#code-notice")
                  .empty()
                  .append("<p class='blue-link'>" + data.error_message + "<p>");
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
            $("#code-notice").empty().append(
                "<p class='blue-link'> Sorry the signup is closed! Please try again later!<p>"
              );
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


  document.getElementById('code-input').addEventListener('keyup', e => {

    if (e.target.value.length == 6) {
      $(".loading").toggleClass("d-none");
      
      if (
          isNaN($("input[name='verify_code']").val()) ||
          $("input[name='verify_code']").val().length != 6 ||
          isNaN($("#id_phone_number").val()) ||
          $("#id_phone_number").val().length != 11 ||
          $("#id_phone_number").val().charAt(0) != 1
      ) {
          event.preventDefault();
          document.getElementById(
              "results").innerHTML="<p class='blue-link'> The code is not correct!<p>";
      } else {
          let main_phone_no = document.getElementById("id_phone_number").value.toString();

          if ( main_phone_no.startsWith("+86") == false) {
              document.getElementById("id_phone_number").value = "+86" + main_phone_no;
          }

       $.ajax({
          url: "/users/cmplt-wx-reg-149eb8766awswdff224fgo029k12ol8/",
          data: Object.fromEntries(new FormData(document.querySelector("form"))),
          cache: false,
          type: "POST",
          success: function(data) {
            if (data.success == true) {
                window.location.replace('/stories/');
            } else {
                  $("#results").empty().append(
                      "<p class='text-error '>" + data.error_message + "</p>"
                    );
                  $("#send-code").attr("disabled", false);
                  code_counter = code_counter + 1;

                  if (code_counter >= 5) {
                    $("#id_verify_code").attr("disabled", true);
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
  });
});
