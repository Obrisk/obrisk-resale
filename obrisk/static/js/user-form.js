$(document).ready(function() {
  // adding a crsf token
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
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

$(function() {
  function checkPassword(str) {
    // at least one number, one lowercase and one uppercase letter
    // at least six characters
    var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/;
    return re.test(str);
  }

  $("#send-code").click(function(event) {
    if (!$("#id_phone_number").val()) {
      event.preventDefault();
      bootbox.alert(
        "It looks like you didn't enter your phone number. Please enter a valid phone number!"
      );
    } else {
      var num = parseInt($("#id_phone_number").val());
      var str = num.toString();

      if (isNaN(num) || str.length != 11 || str.charAt(0) != 1) {
        event.preventDefault();
        bootbox.alert(
          "The phone number you entered is not correct. Please don't include the country code or spaces or any character!"
        );
      } else {
        //If button is disabled and the verification code is not sent, user can't do anything.
        var url, req;

        if (current_url == "/accounts-authorization/signup/") {
          url = "/users/verification-code/";
          req = "GET";
        } else if (current_url == "/users/phone-password-reset/") {
          url = "/users/phone-password-reset/";
          req = "POST";
        } else {
          bootbox.alert(
            "We are sorry, we can't handle users registration at the moment. Please try again later"
          );
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
              $("#code").toggleClass("d-none");
              $("#email-request").toggleClass("d-none");
              $("#code-notice")
                .empty()
                .append("<p class='blue-link'>" + data.message + "<p>");

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

              if (verify_counter >= 5) {
                $("#send-code").attr("disabled", true);
                bootbox.alert(
                  "Maximum number of sending code trials has reached, we can't send anymore!"
                );
              }

              //$("#send-code").attr("disabled", false);
            } else {
              $("#code-notice")
                .empty()
                .append("<p class='blue-link'>" + data.error_message + "</p>");
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
            $("#code-notice").empty()
                .append("<p class='blue-link'> Sorry the signup is closed! Please try again later!<p>");
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
                    "<p class='blue-link'> You have successfully verified your phone number! Please wait to be redirected <p>"
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
                bootbox.alert(
                  "Maximum number of code retrial has reached, you can't retry anymore!"
                );
              }
            }
            $(".loading").toggleClass("d-none");
          },
          error: function(error) {
            bootbox.alert(error);
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
      var pw2 = $("#id_password2").val();
      if (pw1 != "" && pw2 != "" && pw1 == pw2) {
        if (checkPassword(pw2)) {
          goToNextStep();
        } else {
          //weak password
          bootbox.alert("Pass");
        }
      } else {
        //wrong password
        bootbox.alert("Your Passwords do not match");
      }
    } else {
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

  $("#phone-signup-submit").click(function(event) {
    if (!$("input[name='verified_no']").val()) {
      event.preventDefault();
      bootbox.alert(
        "Please verify your phone number by requesting the verification code, before signing up!"
      );
    } else if (
      !$("select[name='city']").val() ||
      !$("select[name='province']")
    ) {
      event.preventDefault();
      $(".process-panel-wrap").removeClass("is-active");
      $(".step-title").removeClass("is-active");
      $(".step-dot-3").addClass("is-active");
      bootbox.alert("Please enter your city and province!");
    } else if (
      !$("input[name='username']").val() ||
      !$("input[name='password1']") ||
      !$("input[name='password2']")
    ) {
      event.preventDefault();
      $(".process-panel-wrap").removeClass("is-active");
      $(".step-title").removeClass("is-active");
      $(".step-dot-2").addClass("is-active");
      bootbox.alert(
        "Please fill in all of the info. Also verify your phone number!"
      );
    } else if (
      $("input[name='password1']").val() != $("input[name='password2']").val()
    ) {
      event.preventDefault();
      $(".process-panel-wrap").removeClass("is-active");
      $(".step-title").removeClass("is-active");
      $(".step-dot-2").addClass("is-active");
      bootbox.alert("Your password's inputs don't match!");
    } else {
      $("#id_phone_number").attr("disabled", false);

      if (
        $("#id_phone_number")
          .val()
          .toString()
          .startsWith("+86") == false
      ) {
        $("#id_phone_number").val("+86" + $("#id_phone_number").val());
      }
      $("input[name='city']").val($("select[name='city']").val());
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
      bootbox.alert("Please enter your city and province!");
    } else if (
      !$("input[name='username']").val() ||
      !$("input[name='email']").val() ||
      !$("input[name='password1']") ||
      !$("input[name='password2']")
    ) {
      event.preventDefault();
      bootbox.alert("Please fill in all of the infomation");
    } else if (
      $("input[name='password1']").val() != $("input[name='password2']").val()
    ) {
      event.preventDefault();
      bootbox.alert("Your password's inputs don't match!");
    } else {
      $("#id_phone_number").attr("disabled", false);
      $("input[name='city']").val($("select[name='city']").val());
      $("input[name='province_region']").val(
        $("select[name='province']").val()
      );
      $("#signup_form").submit();
    }
  });
});

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
          badPass: "Weak; try combining letters & numbers",
          goodPass: "Medium; try using special characters",
          strongPass: "Strong password",
          containsField: "The password contains your username",
          enterPass: "Type your password",
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

$("#id_password1,#id_password2").password({
  shortPass: "The password is too short",
  badPass: "Weak; try combining letters & numbers",
  goodPass: "Medium; try using special characters",
  strongPass: "Strong password",
  containsField: "The password contains your username",
  enterPass: "Type your password",
  showPercent: false,
  showText: true, // shows the text tips
  animate: true, // whether or not to animate the progress bar on input blur/focus
  animateSpeed: "fast", // the above animation speed
  field: "#id_username", // select the match field (selector or jQuery instance) for better password checks
  fieldPartialMatch: true, // whether to check for partials in field
  minimumLength: 8 // minimum password length (below this threshold, the score is 0)
});

strongPass1 = false;
strongPass2 = false;

$("#id_password1").on("password.text", (e, text, score) => {
  if (score > 68) {
    strongPass1 = true;
    $(document).trigger("strongPass");
  } else strongPass1 = false;
});

$("#id_password2").on("password.text", (e, text, score) => {
  if (score > 68) {
    strongPass2 = true;
    $(document).trigger("strongPass");
  } else strongPass2 = false;
});

$(document).ready(function() {
  $(document).on("strongPass", function() {
    if (strongPass1 && strongPass2) {
      $(".process-button").removeClass("is-hidden");
    } else $(".process-button").addClass("is-hidden");
  });
});
