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

              if ($("#code").hasClass("d-none")) {
                  $("#code").toggleClass("d-none");
              }
              if ($("#email-request").hasClass("d-none")) {
                  $("#email-request").toggleClass("d-none");
              }

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
            $("#code-notice")
              .empty()
              .append(
                "<p class='blue-link'> Sorry the signup is closed! Please try again later!<p>"
              );
            console.log(err);
          }
        });
        return false;
      }
    }
  });

  $("input[name='code']").keyup(function(e) {
    if (e.target.value.length == 6) {
      $(".loading").toggleClass("d-none");
      if (
        isNaN($("input[name='code']").val()) ||
        $("input[name='code']").val().length != 6 ||
        isNaN($("#id_phone_number").val()) ||
        $("#id_phone_number").val().length != 11 ||
        $("#id_phone_number")
          .val()
          .charAt(0) != 1
      ) {
        event.preventDefault();
      } else {
        $.ajax({
          url: "/users/phone-verify/",
          data: {
            phone_no: $("#id_phone_number").val(),
            code: $("input[name='code']").val()
          },
          cache: false,
          type: "GET",
          success: function(data) {
            //enable send button after message is sent
            if (data.success == true) {
              // $('#send-code').removeAttr("disabled");
              if (data.url) {
                $("#results")
                  .empty()
                  .append(
                    "<p class='blue-link'>Successfully verified your number! Redirecting... <p>"
                  );
                window.location.href = data.url;
              } else {
                $("#results")
                  .empty()
                  .append(
                    "<p class='blue-link'> You have successfully verified your phone number! <p>"
                  );
                $("input[name='verified_no']").val("YES");

                //I should hide the phone number label that says don't enter country code
                $("#phone_label").hide();

                $("#code-notice").empty();

                $("#code").hide();
                $("#send-code").hide();
                $("#email-request").hide();
                $("#signup-panel-1").hide();
                $(".process-panel-wrap").removeClass("is-active");
                $(".step-title").removeClass("is-active");
              }
              $(".step-dot-2").addClass("is-active");
            } else {
              $("#results")
                .empty()
                .append(
                  "<p class='text-error '>" + data.error_message + "</p>"
                );
              $("#send-code").attr("disabled", false);
              code_counter = code_counter + 1;

              if (code_counter >= 5) {
                $("#phone-verify").attr("disabled", true);
                printError(
                  "Maximum number of code retrial has reached, you can't retry anymore!");
              }
            }
            $(".loading").toggleClass("d-none");
          },
          error: function(error) {
            printError(error);
          }
        });
        return false;
      }
    }
  });

  $("#phone-verify").click(function() {});

  //Updated form to be use steps

  $(".process-button").on("click", function() {
    var $this = $(this);
    var targetStepDot = $this.attr("data-step");
    function goToNextStep() {
      $this.addClass("is-loading");
      setTimeout(function() {
        $this.removeClass("is-loading");
        $(".process-panel-wrap").removeClass("is-active");
        $("." + targetStepDot).addClass("is-active");
      }, 500);
    }

    if (targetStepDot == "step-dot-3") {
      goToNextStep();
    }
  });


  $("#signup-finish").on("click", function() {
    var $this = $(this);
    var url = "/stories";
    $this.addClass("is-loading");
    setTimeout(function() {
      window.location = url;
    }, 800);
  });

  });

});

  $("#social-signup-submit").click(function(event) {
    if (!$("input[name='verified_no']").val()) {
      event.preventDefault();
      printError(
        "Please verify your phone number before submitting the form!"
      );
    } else {
      $("#id_phone_number").attr("disabled", false);

      if (
        $("#id_phone_number").val().toString().startsWith("+86") == false) {
            $("#id_phone_number").val("+86" + $("#id_phone_number").val());
        }

          $("input[name='city']").val(
              $("select[name='city']").val()
          );
          $("input[name='province_region']").val(
            $("select[name='province']").val()
          );

          $("#signup_form").submit();
     } 
});
