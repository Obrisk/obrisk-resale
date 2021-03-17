const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

$(function() {
  function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  // This sets up every ajax call with proper headers.
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

});

var verify_counter = 0;
var code_counter = 0;

var phone_no;

function printError(msg) {
  document.getElementsByClassName('notification')[0].classList.remove('is-hidden'); 
  document.getElementById('notf-msg').innerHTML = msg;
}

$(function() {
  document.getElementById("id_phone_number").removeAttribute("disabled");

  document.querySelectorAll('.close-dj-messages').forEach(item => {
    item.addEventListener('click', e => {
        e.currentTarget.parentElement.classList.add('is-hidden');
        e.stopPropagation();
    });
  });

  $("#send-code").click(function(event) {
    if (!$("#id_phone_number").val()) {
      event.preventDefault();
      $("#code-notice")
        .empty()
        .append(
          "<p class='error-text'>Please enter a valid phone number!<p>"
        );
    } else {
      const num = parseInt($("#id_phone_number").val());
      const nm_str = num.toString();

      if (isNaN(num) || nm_str.length != 11 || nm_str.charAt(0) != 1) {
        event.preventDefault();
        $("#code-notice")
          .empty()
          .append(
            "<p class='error-text'> Don't include country code or special characters<p>");
      } else {
        //If button is disabled and the verification code is not sent, user can't do anything.
        var url, req;

        if (current_url == "/users/phone-password-reset/") {
              url = "/users/phone-password-reset/";
              req = "POST";
        } else {
              url = "/users/verification-code/";
              req = "GET";
        }

        $.ajax({
          url: url,
          data: {
            phone_no: num
          },
          cache: false,
          type: req,
          success: function(data) {
            if (data.success == true) {
              timeout = 60;
              $("#send-code").attr("disabled", true);
              $("#phone_label").hide();


              if (data.message != undefined) {
                $("#code-notice")
                  .empty()
                  .append("<p class='pass-text'>" + data.message + "<p>");
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
                  "Max number of sending SMS has reached, Try again later!"
                );
              }

            } else {
              if (data.error_message != undefined) {
                $("#code-notice")
                  .empty()
                  .append("<p class='error-text'>" + data.error_message + "<p>");
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
            $("#code-notice")
              .empty()
              .append(
                "<p class='error-text'> Sorry, Please try again later!<p>"
              );
            console.log(err);
          }
        });
        return false;
      }
    }
  });


  function submitPsReset(e) {
    if (document.querySelector('#code').value.length == 6) {

       if ($(".loading").hasClass("is-hidden")) {
          $(".loading").toggleClass("is-hidden");
       }
       const int_num = parseInt($("#id_phone_number").val())
       const str_num = int_num.toString();

    if (isNaN(int_num) || str_num.length < 11 || str_num.length > 14) {
          event.preventDefault();
          $("#results").empty().append(
            "<p class='error-text'> Phone number is incorrect! <p>"
          );

      } else {
        $.ajax({
          url: "/users/phone-verify/",
          data: {
            phone_no: $("#id_phone_number").val(),
            code: $('#code').val()
          },
          cache: false,
          type: "GET",
          success: function(data) {
            //enable send button after message is sent
            if (data.success == true) {
              if (data.url) {
                    $("#results")
                      .empty()
                      .append(
                        "<p class='error-text'>Successfully verified your number! Redirecting... <p>"
                      );
                    window.location.href = data.url;
              } else {
                    $("#results")
                      .empty()
                      .append(
                        "<p class='error-text'> You have successfully verified your phone number! <p>"
                      );
                    $("input[name='verified_no']").val("YES");

                    $("#signup-panel-1").hide();
                    $(".process-panel-wrap").removeClass("is-active");
                    $(".step-title").removeClass("is-active");
              }

              $(".step-dot-2").removeClass("is-hidden");
              $(".step-dot-2").addClass("is-active");
            } else {
              $("#results")
                .empty()
                .append(
                  "<p class='error-text'>" + data.error_message + "</p>"
                );
              $("#send-code").attr("disabled", false);
              code_counter = code_counter + 1;

              if (code_counter >= 7) {
                $("#phone-verify").attr("disabled", true);
                printError(
                  "Maximum number of code retrial, you can't retry anymore!"
                );
              }
            }

          $(".loading").removeClass("is-hidden");

          },
          error: function(error) {
            printError(error);
          }
        });
        return false;
      }
    }
  }

  $('#code').keyup(function(e) {
    submitPsReset(e)
  });

  $("#submit-ps-reset").click(function(event) {
     submitPsReset(event)
  });

});
