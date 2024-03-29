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


/* -------------------------------------------------------------------------- */
/*                               utils and libs                               */
/* -------------------------------------------------------------------------- */
//Print error message
const confirm_btn = document.querySelector('#confirm');
const code_notice = document.getElementById("code-notice");
const send_code_btn = document.getElementById('send-code');
const phone_number = document.getElementById('id_phone_number');
const verify_code_input = document.getElementById('verify-code');

var verify_counter = 0;
var code_counter = 0;

var phone_no;

function printError(msg) {
  document.getElementsByClassName('notification')[0].classList.remove('is-hidden'); 
  document.getElementById('notf-msg').innerHTML = msg;
}


$(function() {
  function checkPassword(str) {
    // at least one number, one lowercase and one uppercase letter
    // at least eight characters
    var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/;
    return re.test(str);
  }

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

              if ($("#agree").hasClass("is-hidden")) {
                  $("#agree").toggleClass("is-hidden");
              }

              if ($("#code-section").hasClass("is-hidden")) {
                  $("#code-section").toggleClass("is-hidden");
              }

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
                "<p class='error-text'> Sorry the signup is closed! Please try again later!<p>"
              );
            console.log(err);
          }
        });
        return false;
      }
    }
  });

  $('#code').keyup(function(e) {

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
      var pw1 = $("#id_password1").val();
      if (checkPassword(pw1)) {
        goToNextStep();
      } else {
        //weak password
      }
    } else {
      goToNextStep();
    }
  });

  $("#signup-finish").on("click", function() {
    var $this = $(this);
    var url = "/i/";
    $this.addClass("is-loading");
    setTimeout(function() {
      window.location = url;
    }, 800);
  });

  $("#phone-signup-submit").click(function(event) {
    if (!$("input[name='verified_no']").val()) {
      event.preventDefault();
      printError(
        "Please verify your phone number before submitting the form!"
      );
    } else if (
      !$("select[name='city']").val() ||
      !$("select[name='province']")
    ) {
      event.preventDefault();
      $(".process-panel-wrap").removeClass("is-active");
      $(".step-title").removeClass("is-active");
      $(".step-dot-3").addClass("is-active");
      printError("Please enter your city and province!");
    } else if (
      !$("input[name='username']").val() ||
      !$("input[name='password1']").val()
    ) {
      event.preventDefault();
      $(".process-panel-wrap").removeClass("is-active");
      $(".step-title").removeClass("is-active");
      $(".step-dot-2").addClass("is-active");
      printError(
        "Please provide your username and password!"
      );
    } else if ( $("input[name=username").val().length < 3 ||
       $("input[name=username").val().length > 16  ) {

      event.preventDefault();
      $(".process-panel-wrap").removeClass("is-active");
      $(".step-title").removeClass("is-active");
      $(".step-dot-2").addClass("is-active");
      printError(
        "Username must be 3 to 16 letters, without spaces!"
      );
    } else if ( $("input[name=password1").val().length < 8) {

      event.preventDefault();
      $(".process-panel-wrap").removeClass("is-active");
      $(".step-title").removeClass("is-active");
      $(".step-dot-2").addClass("is-active");

      printError(
        "The password is too weak!"
      );

    } else {
          $("#id_phone_number").attr("disabled", false);

          if ($("#id_phone_number").val().toString().startsWith("+86") === false)
          {
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

  //update-profile submit event is on the image-uploader.js file
  //In the near future please reorganise the files.

  $("#email-signup-submit").click(function(event) {
    if (!$("select[name='city']").val() || !$("select[name='province']")) {
      event.preventDefault();
      printError("Please enter your city and province!");
    } else if (
      !$("input[name='username']").val() ||
      !$("input[name='email']").val() ||
      !$("input[name='password1']")
    ) {
      event.preventDefault();
      printError("Please fill in all of the infomation");
    } else {
      $("#id_phone_number").attr("disabled", false);
      $("input[name='password2']").val($("input[name='password1']").val());
      $("input[name='city']").val($("select[name='city']").val());
      $("input[name='province_region']").val(
        $("select[name='province']").val()
      ); //hack for second password
      $("#signup_form").submit();
    }
  });

});

/* -------------------------------------------------------------------------- */
/*                              Password checker                              */
/* -------------------------------------------------------------------------- */
/**
 * @author Òscar Casajuana a.k.a. elboletaire <elboletaire at underave dot net>
 * @link https://github.com/elboletaire/password-strength-meter
 * @license GPL-3.0
 */
!(function(h) {
  "use strict";
  function e(i, l) {
    function c(s, e) {
      for (var t = "", a = !1, n = 0; n < e.length; n++) {
        a = !0;
        for (var r = 0; r < s && r + n + s < e.length; r++)
          a = a && e.charAt(r + n) === e.charAt(r + n + s);
        r < s && (a = !1), a ? ((n += s - 1), (a = !1)) : (t += e.charAt(n));
      }
      return t;
    }
    return (
      (l = h.extend(
        {},
        {
          shortPass: "The password is too short",
          badPass: "Weak; Try combining letters & numbers",
          goodPass: "Medium; Medium stength!",
          strongPass: "Strong password!",
          containsField: "The password contains your username",
          enterPass: "Not less than 8 letters & numbers",
          showPercent: !1,
          showText: !0,
          animate: !0,
          animateSpeed: "fast",
          field: !1,
          fieldPartialMatch: !0,
          minimumLength: 4,
          closestSelector: "div"
        },
        l
      )),
      function() {
        var s = !0,
          n = l.showText,
          r = l.showPercent,
          e = h("<div>").addClass("pass-graybar"),
          o = h("<div>").addClass("pass-colorbar"),
          t = h("<div>")
            .addClass("pass-wrapper")
            .append(e.append(o));
        return (
          i.closest(l.closestSelector).addClass("pass-strength-visible"),
          l.animate &&
            (t.css("display", "none"),
            (s = !1),
            i.closest(l.closestSelector).removeClass("pass-strength-visible")),
          l.showPercent &&
            ((r = h("<span>")
              .addClass("pass-percent")
              .text("0%")),
            t.append(r)),
          l.showText &&
            ((n = h("<span>")
              .addClass("pass-text")
              .html(l.enterPass)),
            t.append(n)),
          i.closest(l.closestSelector).append(t),
          i.keyup(function() {
            var s = l.field || "";
            s && (s = h(s).val());
            var e = (function(s, e) {
              var t = 0;
              if (s.length < l.minimumLength) return -1;
              if (l.field) {
                if (s.toLowerCase() === e.toLowerCase()) return -2;
                if (l.fieldPartialMatch && e.length) {
                  var a = new RegExp(e.toLowerCase());
                  if (s.toLowerCase().match(a)) return -2;
                }
              }
              (t += 4 * s.length),
                (t += c(1, s).length - s.length),
                (t += c(2, s).length - s.length),
                (t += c(3, s).length - s.length),
                (t += c(4, s).length - s.length),
                s.match(/(.*[0-9].*[0-9].*[0-9])/) && (t += 5);
              var n = ".*[!,@,#,$,%,^,&,*,?,_,~]";
              return (
                (n = new RegExp("(" + n + n + ")")),
                s.match(n) && (t += 5),
                s.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/) && (t += 10),
                s.match(/([a-zA-Z])/) && s.match(/([0-9])/) && (t += 15),
                s.match(/([!,@,#,$,%,^,&,*,?,_,~])/) &&
                  s.match(/([0-9])/) &&
                  (t += 15),
                s.match(/([!,@,#,$,%,^,&,*,?,_,~])/) &&
                  s.match(/([a-zA-Z])/) &&
                  (t += 15),
                (s.match(/^\w+$/) || s.match(/^\d+$/)) && (t -= 10),
                100 < t && (t = 100),
                t < 0 && (t = 0),
                t
              );
            })(i.val(), s);
            i.trigger("password.score", [e]);
            var t = e < 0 ? 0 : e;
            if (
              (o.css({
                backgroundPosition: "0px -" + t + "px",
                width: t + "%"
              }),
              l.showPercent && r.html(t + "%"),
              l.showText)
            ) {
              var a = (function(s) {
                return -1 === s
                  ? l.shortPass
                  : -2 === s
                  ? l.containsField
                  : (s = s < 0 ? 0 : s) < 34
                  ? l.badPass
                  : s < 68
                  ? l.goodPass
                  : l.strongPass;
              })(e);
              !i.val().length && e <= 0 && (a = l.enterPass),
                n.html() !==
                  h("<div>")
                    .html(a)
                    .html() && (n.html(a), i.trigger("password.text", [a, e]));
            }
          }),
          l.animate &&
            (i.focus(function() {
              s ||
                t.slideDown(l.animateSpeed, function() {
                  (s = !0),
                    i
                      .closest(l.closestSelector)
                      .addClass("pass-strength-visible");
                });
            }),
            i.blur(function() {
              !i.val().length &&
                s &&
                t.slideUp(l.animateSpeed, function() {
                  (s = !1),
                    i
                      .closest(l.closestSelector)
                      .removeClass("pass-strength-visible");
                });
            })),
          this
        );
      }.call(this)
    );
  }
  h.fn.password = function(s) {
    return this.each(function() {
      new e(h(this), s);
    });
  };
})(jQuery);

$("#id_password1").password({

  shortPass: "The password is too short",
  badPass: "Weak; Try combining letters & numbers",
  goodPass: "Medium; This is okay",
  strongPass: "Strong password!",
  containsField: "The password contains your username",
  enterPass: "Type carefully, ensure there are no mistakes!",

  showPercent: false,
  showText: true, // shows the text tips
  animate: true, // whether or not to animate the progress bar on input blur/focus
  animateSpeed: "fast", // the above animation speed
  field: "#id_username", // select the match field (selector or jQuery instance) for better password checks
  fieldPartialMatch: true, // whether to check for partials in field
  minimumLength: 8 // minimum password length (below this threshold, the score is 0)
});

strongPass1 = false;

$("#id_password1").on("password.text", (e, text, score) => {
  if (score > 68) {
    strongPass1 = true;
    $(".process-button").removeClass("is-hidden");
  } else {
    $(".process-button").addClass("is-hidden");
  }
});
