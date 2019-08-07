
$(document).ready(function () {
	//Hide the verification code form
	$("#code").hide();
	$("#email-request").hide();

	if (!errors) {
		$("#name_and_psword").hide();
	}

});

// adding a crsf tokken
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function (xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});


var verify_counter = 0;
var code_counter = 0;

var phone_no;

$(function () {
	$("#send-code").click(function (event) {
		if (!$("#id_phone_number").val()) {
			event.preventDefault();
			bootbox.alert("It looks like you didn't enter your phone number. Please enter a valid phone number!");
		} 
		else {
			
			var num = parseInt($("#id_phone_number").val());
			var str = num.toString() ;

		
			if (isNaN(num) || (str.length != 11) || (str.charAt(0) != 1)) {
				event.preventDefault();
				bootbox.alert("The phone number you entered is not correct. Please don't include the country code or spaces or any character!");
			} else {
				//If button is disabled and the verification code is not sent, user can't do anything.
				var url, req;
				
				if (current_url == '/users/signup/') {
					url = '/users/verification-code/';
					req = 'GET';
				}else if (current_url == '/users/phone-password-reset/') {
					url = '/users/phone-password-reset/';
					req = 'POST';
				}else {
					bootbox.alert("We are so sorry, we can't handle users registration right now!");
				}

				$.ajax({
					url: url,
					data: {
						phone_no: num
					},
					cache: false,
					type: req,
					success: function (data) {
						if (data.success == true)
						{
							timeout = 60;
							$("#send-code").attr("disabled", true);
							$("#phone_label").hide();
							$("#code").show();
							$("#email-request").show();
							$("#code-notice").empty().append("<p>" + data.message + "<p>");

							function updateSec() {
								timeout--;
								if (timeout > 0) {
									$("#send-code").text(timeout + " S")
								} else {
									$("#send-code").text("Get Code")
									$("#send-code").attr("disabled", false);
								}
							}
							// repeat with the interval of 1 seconds
							let timerId = setInterval(() => updateSec(), 1000);

							// after 60 seconds stop
							setTimeout(() => { clearInterval(timerId); }, 61000);


							verify_counter = verify_counter + 1;

							if(verify_counter >= 5){
								$("#send-code").attr("disabled", true);
								bootbox.alert("Maximum number of sending code trials has reached, we can't send anymore!");

							}

							//$("#send-code").attr("disabled", false);
						} else {
							$("#code-notice").empty().append("<p>" + data.error_message + "</p>");
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
					error: function (err) {
						console.log(err);
					}
				});
				return false;
			}
		}

	});

	$("#phone-verify").click(function () {

		if ((isNaN($("input[name='code']").val())) || ($("input[name='code']").val().length != 6) ||
			(isNaN($("#id_phone_number").val())) || ($("#id_phone_number").val().length != 11) ||
			($("#id_phone_number").val().charAt(0) != 1)) {
			event.preventDefault();
			bootbox.alert("The code you entered is wrong!");
		} else {
			$.ajax({
				url: '/users/phone-verify/',
				data: {
					phone_no: $('#id_phone_number').val(),
					code: $("input[name='code']").val()
				},
				cache: false,
				type: 'GET',
				success: function (data) {
					//enable send button after message is sent
					if (data.success == true)
					{
						// $('#send-code').removeAttr("disabled");
						if (data.url) {
							$("#results").empty().append("<p> You have successfully verified your phone number! Please wait to be redirected <p>");
							window.location.href = data.url;
						}
						else {
							$("#results").empty().append("<p> You have successfully verified your phone number! <p>");
							$("input[name='verified_no']").val("YES");

							//I should hide the phone number label that says don't enter country code
							$("#id_phone_number").val("+86" + $("#id_phone_number").val());

							$("#phone_label").hide();

							$("#code-notice").empty();

							$("#code").hide();
							$("#send-code").hide();
							$("#email-request").hide();
							$("#id_phone_number").attr("disabled", true);
							$("#name_and_psword").show();
						}

					} else {
						$("#results").empty().append("<p class='text-error'>" + data.error_message + "</p>");
						$("#send-code").attr("disabled", false);
						code_counter = code_counter + 1;

						if (code_counter >= 5) {
							$("#phone-verify").attr("disabled", true);
							bootbox.alert("Maximum number of code retrial has reached, you can't retry anymore!");
						}	
					}
				},
				error: function (error) {
					bootbox.alert(error)
				}
			});
			return false;
		}
	});


	$("#phone-signup-submit").click(function (event) {
		if (!$("input[name='verified_no']").val()) {
			event.preventDefault();
			bootbox.alert("Please verify your phone number by requesting the verification code, before signing up!");
		}
		else if (!$("select[name='city']").val() || !$("select[name='province']")) {
			event.preventDefault();
			bootbox.alert("Please enter your address!");
		}
		else if (!$("input[name='username']").val() || !$("input[name='password1']") || !$("input[name='password2']")) {
			event.preventDefault();
			bootbox.alert("Please fill in all of the info. Also verify your phone number!");
		}
		else if ($("input[name='password1']").val() != $("input[name='password2']").val()) {
			event.preventDefault();
			bootbox.alert("Your password's inputs don't match!");
		} else {
			$("#id_phone_number").attr("disabled", false);
			$("input[name='city']").val($("select[name='city']").val());
			$("input[name='province_region']").val($("select[name='province']").val());
			$("#signup_form").submit();
		}
	});

	//update-profile submit event is on the image-uploader.js file
	//In the near future please reorganise the files.

	$("#email-signup-submit").click(function (event) {

		if (!$("select[name='city']").val() || !$("select[name='province']")) {
			event.preventDefault();
			bootbox.alert("Please enter your address!");
		}
		else if (!$("input[name='username']").val() || !$("input[name='email']").val() || !$("input[name='password1']") || !$("input[name='password2']")) {
			event.preventDefault();
			bootbox.alert("Please fill in all of the infomation");
		}
		else if ($("input[name='password1']").val() != $("input[name='password2']").val()) {
			event.preventDefault();
			bootbox.alert("Your password's inputs don't match!");
		} else {
			$("#id_phone_number").attr("disabled", false);
			$("input[name='city']").val($("select[name='city']").val());
			$("input[name='province_region']").val($("select[name='province']").val());
			$("#signup_form").submit();
		}
	});


});

