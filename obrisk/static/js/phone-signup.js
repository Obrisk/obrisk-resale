const csrftoken=document.querySelector("[name=csrfmiddlewaretoken]").value;$((function(){$.ajaxSetup({beforeSend:function(e,t){var s;s=t.type,/^(GET|HEAD|OPTIONS|TRACE)$/.test(s)||this.crossDomain||e.setRequestHeader("X-CSRFToken",csrftoken)}})}));const confirm_btn=document.querySelector("#confirm"),code_notice=document.getElementById("code-notice"),send_code_btn=document.getElementById("send-code"),phone_number=document.getElementById("id_phone_number"),verify_code_input=document.getElementById("verify-code");var phone_no,verify_counter=0,code_counter=0;function printError(e){document.getElementsByClassName("notification")[0].classList.remove("is-hidden"),document.getElementById("notf-msg").innerHTML=e}$((function(){function e(){$(".loading").hasClass("is-hidden")&&$(".loading").toggleClass("is-hidden");const e=parseInt($("#id_phone_number").val()),t=e.toString();if(!(isNaN(e)||t.length<11||t.length>14))return $.ajax({url:"/users/phone-verify/",data:{phone_no:$("#id_phone_number").val(),code:$("#code").val()},cache:!1,type:"GET",success:function(e){1==e.success?(e.url?($("#results").empty().append("<p class='error-text'>Successfully verified your number! Redirecting... <p>"),window.location.href=e.url):($("#results").empty().append("<p class='error-text'> You have successfully verified your phone number! <p>"),$("input[name='verified_no']").val("YES"),$("#signup-panel-1").hide(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active")),$(".step-dot-2").removeClass("is-hidden"),$(".step-dot-2").addClass("is-active")):($("#results").empty().append("<p class='error-text'>"+e.error_message+"</p>"),$("#send-code").attr("disabled",!1),(code_counter+=1)>=7&&($("#phone-verify").attr("disabled",!0),printError("Maximum number of code retrial, you can't retry anymore!"))),$(".loading").removeClass("is-hidden")},error:function(e){printError(e)}}),!1;event.preventDefault(),$("#results").empty().append("<p class='error-text'> Phone number is incorrect! <p>")}document.getElementById("id_phone_number").removeAttribute("disabled"),document.querySelectorAll(".close-dj-messages").forEach(e=>{e.addEventListener("click",e=>{e.currentTarget.parentElement.classList.add("is-hidden"),e.stopPropagation()})}),$("#send-code").click((function(e){if($("#id_phone_number").val()){const n=parseInt($("#id_phone_number").val()),a=n.toString();var t,s;if(!isNaN(n)&&11==a.length&&1==a.charAt(0))return"/users/phone-password-reset/"==current_url?(t="/users/phone-password-reset/",s="POST"):(t="/users/verification-code/",s="GET"),$.ajax({url:t,data:{phone_no:n},cache:!1,type:s,success:function(e){if(1==e.success){timeout=60,$("#send-code").attr("disabled",!0),$("#phone_label").hide(),$("#agree").hasClass("is-hidden")&&$("#agree").toggleClass("is-hidden"),$("#code-section").hasClass("is-hidden")&&$("#code-section").toggleClass("is-hidden"),null!=e.message&&$("#code-notice").empty().append("<p class='pass-text'>"+e.message+"<p>");let t=setInterval(()=>(timeout--,void(timeout>0?$("#send-code").text(timeout+" S"):($("#send-code").text("Get Code"),$("#send-code").attr("disabled",!1)))),1e3);setTimeout(()=>{clearInterval(t)},61e3),(verify_counter+=1)>=7&&($("#send-code").attr("disabled",!0),printError("Max number of sending SMS has reached, Try again later!"))}else null!=e.error_message&&$("#code-notice").empty().append("<p class='error-text'>"+e.error_message+"<p>"),null!=e.messageId&&console.log(e.messageId),null!=e.requestId&&console.log(e.requestId),null!=e.returnedCode&&console.log(e.returnedCode),null!=e.retries&&console.log(e.retries)},error:function(e){$("#code-notice").empty().append("<p class='error-text'> Sorry the signup is closed! Please try again later!<p>"),console.log(e)}}),!1;e.preventDefault(),$("#code-notice").empty().append("<p class='error-text'> Don't include country code or special characters<p>")}else e.preventDefault(),$("#code-notice").empty().append("<p class='error-text'>Please enter a valid phone number!<p>")})),document.getElementById("code").addEventListener("keyup",t=>{6===t.target.value.length&&e()}),document.getElementById("submit-code").addEventListener("click",t=>{e()});const t=document.getElementById("id_username"),s=document.getElementById("username-errors"),n=document.getElementById("phone-signup-submit");t.addEventListener("keyup",e=>{fetch("/users/username-exists/?username="+e.target.value).then(e=>e.json()).then(e=>{"201"===e.status?(s.innerHTML="This username is already taken!",n.disabled=!0):(s.innerHTML="",n.disabled=!1)})}),$(".process-button").on("click",(function(){var e=$(this),t=e.attr("data-step");function s(){e.addClass("is-loading"),setTimeout((function(){e.removeClass("is-loading"),$(".process-panel-wrap").removeClass("is-active"),$("."+t).addClass("is-active")}),500)}if("step-dot-3"==t){var n=$("#id_password1").val();/(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/.test(n)&&s()}else s()})),$("#signup-finish").on("click",(function(){var e=$(this);e.addClass("is-loading"),setTimeout((function(){window.location="/i/"}),800)})),$("#phone-signup-submit").click((function(e){$("input[name='verified_no']").val()?$("select[name='city']").val()&&$("select[name='province']")?$("input[name='username']").val()&&$("input[name='password1']").val()?$("input[name=username").val().length<3||$("input[name=username").val().length>16?(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-2").addClass("is-active"),printError("Username must be 3 to 16 letters, without spaces!")):$("input[name=password1").val().length<8?(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-2").addClass("is-active"),printError("The password is too weak!")):($("#id_phone_number").attr("disabled",!1),!1===$("#id_phone_number").val().toString().startsWith("+86")&&$("#id_phone_number").val("+86"+$("#id_phone_number").val()),$("input[name='city']").val($("select[name='city']").val()),$("input[name='province_region']").val($("select[name='province']").val()),$("#signup_form").submit()):(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-2").addClass("is-active"),printError("Please provide your username and password!")):(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-3").addClass("is-active"),printError("Please enter your city and province!")):(e.preventDefault(),printError("Please verify your phone number before submitting the form!"))})),$("#email-signup-submit").click((function(e){$("select[name='city']").val()&&$("select[name='province']")?$("input[name='username']").val()&&$("input[name='email']").val()&&$("input[name='password1']")?($("#id_phone_number").attr("disabled",!1),$("input[name='password2']").val($("input[name='password1']").val()),$("input[name='city']").val($("select[name='city']").val()),$("input[name='province_region']").val($("select[name='province']").val()),$("#signup_form").submit()):(e.preventDefault(),printError("Please fill in all of the infomation")):(e.preventDefault(),printError("Please enter your city and province!"))}))})),function(e){"use strict";function t(t,s){function n(e,t){for(var s="",n=!1,a=0;a<t.length;a++){n=!0;for(var r=0;r<e&&r+a+e<t.length;r++)n=n&&t.charAt(r+a)===t.charAt(r+a+e);r<e&&(n=!1),n?(a+=e-1,n=!1):s+=t.charAt(a)}return s}return s=e.extend({},{shortPass:"The password is too short",badPass:"Weak; Try combining letters & numbers",goodPass:"Medium; Medium stength!",strongPass:"Strong password!",containsField:"The password contains your username",enterPass:"Not less than 8 letters & numbers",showPercent:!1,showText:!0,animate:!0,animateSpeed:"fast",field:!1,fieldPartialMatch:!0,minimumLength:4,closestSelector:"div"},s),function(){var a=!0,r=s.showText,o=s.showPercent,i=e("<div>").addClass("pass-graybar"),l=e("<div>").addClass("pass-colorbar"),d=e("<div>").addClass("pass-wrapper").append(i.append(l));return t.closest(s.closestSelector).addClass("pass-strength-visible"),s.animate&&(d.css("display","none"),a=!1,t.closest(s.closestSelector).removeClass("pass-strength-visible")),s.showPercent&&(o=e("<span>").addClass("pass-percent").text("0%"),d.append(o)),s.showText&&(r=e("<span>").addClass("pass-text").html(s.enterPass),d.append(r)),t.closest(s.closestSelector).append(d),t.keyup((function(){var a=s.field||"";a&&(a=e(a).val());var i=function(e,t){var a=0;if(e.length<s.minimumLength)return-1;if(s.field){if(e.toLowerCase()===t.toLowerCase())return-2;if(s.fieldPartialMatch&&t.length){var r=new RegExp(t.toLowerCase());if(e.toLowerCase().match(r))return-2}}a+=4*e.length,a+=n(1,e).length-e.length,a+=n(2,e).length-e.length,a+=n(3,e).length-e.length,a+=n(4,e).length-e.length,e.match(/(.*[0-9].*[0-9].*[0-9])/)&&(a+=5);var o=".*[!,@,#,$,%,^,&,*,?,_,~]";return o=new RegExp("("+o+o+")"),e.match(o)&&(a+=5),e.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)&&(a+=10),e.match(/([a-zA-Z])/)&&e.match(/([0-9])/)&&(a+=15),e.match(/([!,@,#,$,%,^,&,*,?,_,~])/)&&e.match(/([0-9])/)&&(a+=15),e.match(/([!,@,#,$,%,^,&,*,?,_,~])/)&&e.match(/([a-zA-Z])/)&&(a+=15),(e.match(/^\w+$/)||e.match(/^\d+$/))&&(a-=10),100<a&&(a=100),a<0&&(a=0),a}(t.val(),a);t.trigger("password.score",[i]);var d=i<0?0:i;if(l.css({backgroundPosition:"0px -"+d+"px",width:d+"%"}),s.showPercent&&o.html(d+"%"),s.showText){var c=function(e){return-1===e?s.shortPass:-2===e?s.containsField:(e=e<0?0:e)<34?s.badPass:e<68?s.goodPass:s.strongPass}(i);!t.val().length&&i<=0&&(c=s.enterPass),r.html()!==e("<div>").html(c).html()&&(r.html(c),t.trigger("password.text",[c,i]))}})),s.animate&&(t.focus((function(){a||d.slideDown(s.animateSpeed,(function(){a=!0,t.closest(s.closestSelector).addClass("pass-strength-visible")}))})),t.blur((function(){!t.val().length&&a&&d.slideUp(s.animateSpeed,(function(){a=!1,t.closest(s.closestSelector).removeClass("pass-strength-visible")}))}))),this}.call(this)}e.fn.password=function(s){return this.each((function(){new t(e(this),s)}))}}(jQuery),$("#id_password1").password({shortPass:"The password is too short",badPass:"Weak; Try combining letters & numbers",goodPass:"Medium; This is okay",strongPass:"Strong password!",containsField:"The password contains your username",enterPass:"Type carefully, ensure there are no mistakes!",showPercent:!1,showText:!0,animate:!0,animateSpeed:"fast",field:"#id_username",fieldPartialMatch:!0,minimumLength:8}),strongPass1=!1,$("#id_password1").on("password.text",(e,t,s)=>{s>68?(strongPass1=!0,$(".process-button").removeClass("is-hidden")):$(".process-button").addClass("is-hidden")});