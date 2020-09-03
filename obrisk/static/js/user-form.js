function printError(e){template=`\n        <div class="notification is-danger" role="alert">\n            <button type="button" class="delete close-dj-messages"></button>\n          ${e}\n        </div>\n        `,$("#signup-panel-2").prepend(template)}var phone_no,verify_counter=0,code_counter=0;$((function(){$("#send-code").click((function(e){if($("#id_phone_number").val()){const a=parseInt($("#id_phone_number").val()),n=a.toString();var s,t;if(!isNaN(a)&&11==n.length&&1==n.charAt(0))return"/users/phone-password-reset/"==current_url?(s="/users/phone-password-reset/",t="POST"):(s="/users/verification-code/",t="GET"),$.ajax({url:s,data:{phone_no:a},cache:!1,type:t,success:function(e){if(1==e.success){timeout=60,$("#send-code").attr("disabled",!0),$("#phone_label").hide(),$("#agree").hasClass("is-hidden")&&$("#agree").toggleClass("is-hidden"),$("#code-section").hasClass("is-hidden")&&$("#code-section").toggleClass("is-hidden"),null!=e.message&&$("#code-notice").empty().append("<p class='pass-text'>"+e.message+"<p>");let s=setInterval(()=>(timeout--,void(timeout>0?$("#send-code").text(timeout+" S"):($("#send-code").text("Get Code"),$("#send-code").attr("disabled",!1)))),1e3);setTimeout(()=>{clearInterval(s)},61e3),(verify_counter+=1)>=7&&($("#send-code").attr("disabled",!0),printError("Maximum number of sending SMS has reached, Try again later!"))}else null!=e.error_message&&$("#code-notice").empty().append("<p class='error-text'>"+e.error_message+"<p>"),null!=e.messageId&&console.log(e.messageId),null!=e.requestId&&console.log(e.requestId),null!=e.returnedCode&&console.log(e.returnedCode),null!=e.retries&&console.log(e.retries)},error:function(e){$("#code-notice").empty().append("<p class='error-text'> Sorry the signup is closed! Please try again later!<p>"),console.log(e)}}),!1;e.preventDefault(),$("#code-notice").empty().append("<p class='error-text'> Don't include country code or special characters<p>")}else e.preventDefault(),$("#code-notice").empty().append("<p class='error-text'>Please enter a valid phone number!<p>")})),$("#code").keyup((function(e){if(6==document.querySelector("#code").value.length){$(".loading").hasClass("is-hidden")&&$(".loading").toggleClass("is-hidden");const e=parseInt($("#id_phone_number").val()),s=e.toString();if(!(isNaN(e)||s.length<11||s.length>14))return $.ajax({url:"/users/phone-verify/",data:{phone_no:$("#id_phone_number").val(),code:$("#code").val()},cache:!1,type:"GET",success:function(e){1==e.success?(e.url?($("#results").empty().append("<p class='error-text'>Successfully verified your number! Redirecting... <p>"),window.location.href=e.url):($("#results").empty().append("<p class='error-text'> You have successfully verified your phone number! <p>"),$("input[name='verified_no']").val("YES"),$("#signup-panel-1").hide(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active")),$(".step-dot-2").removeClass("is-hidden"),$(".step-dot-2").addClass("is-active")):($("#results").empty().append("<p class='error-text'>"+e.error_message+"</p>"),$("#send-code").attr("disabled",!1),(code_counter+=1)>=5&&($("#phone-verify").attr("disabled",!0),printError("Maximum number of code retrial has reached, you can't retry anymore!"))),$(".loading").removeClass("is-hidden")},error:function(e){printError(e)}}),!1;event.preventDefault(),$("#results").empty().append("<p class='error-text'> Phone number is incorrect! <p>")}})),$("#phone-verify").click((function(){})),$(".process-button").on("click",(function(){var e=$(this),s=e.attr("data-step");function t(){e.addClass("is-loading"),setTimeout((function(){e.removeClass("is-loading"),$(".process-panel-wrap").removeClass("is-active"),$("."+s).addClass("is-active")}),500)}if("step-dot-3"==s){var a=$("#id_password1").val();/(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/.test(a)&&t()}else t()})),$("#signup-finish").on("click",(function(){var e=$(this);e.addClass("is-loading"),setTimeout((function(){window.location="/classifieds"}),800)})),$("#phone-signup-submit").click((function(e){$("input[name='verified_no']").val()?$("select[name='city']").val()&&$("select[name='province']")?$("input[name='username']").val()&&$("input[name='password1']").val()?$("input[name=username").val().length<3||$("input[name=username").val().length>16?(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-2").addClass("is-active"),printError("Must be 3 to 16 letters, without spaces!")):$("input[name=password1").val().length<8?(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-2").addClass("is-active"),printError("The password is too weak!")):($("#id_phone_number").attr("disabled",!1),0==$("#id_phone_number").val().toString().startsWith("+86")&&$("#id_phone_number").val("+86"+$("#id_phone_number").val()),$("input[name='city']").val($("select[name='city']").val()),$("input[name='province_region']").val($("select[name='province']").val()),$("#signup_form").submit()):(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-2").addClass("is-active"),printError("Please provide your username and password!")):(e.preventDefault(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active"),$(".step-dot-3").addClass("is-active"),printError("Please enter your city and province!")):(e.preventDefault(),printError("Please verify your phone number before submitting the form!"))})),$("#email-signup-submit").click((function(e){$("select[name='city']").val()&&$("select[name='province']")?$("input[name='username']").val()&&$("input[name='email']").val()&&$("input[name='password1']")?($("#id_phone_number").attr("disabled",!1),$("input[name='password2']").val($("input[name='password1']").val()),$("input[name='city']").val($("select[name='city']").val()),$("input[name='province_region']").val($("select[name='province']").val()),$("#signup_form").submit()):(e.preventDefault(),printError("Please fill in all of the infomation")):(e.preventDefault(),printError("Please enter your city and province!"))}))})),function(e){"use strict";function s(s,t){function a(e,s){for(var t="",a=!1,n=0;n<s.length;n++){a=!0;for(var r=0;r<e&&r+n+e<s.length;r++)a=a&&s.charAt(r+n)===s.charAt(r+n+e);r<e&&(a=!1),a?(n+=e-1,a=!1):t+=s.charAt(n)}return t}return t=e.extend({},{shortPass:"The password is too short",badPass:"Weak; Try combining letters & numbers",goodPass:"Medium; Medium stength!",strongPass:"Strong password!",containsField:"The password contains your username",enterPass:"Not less than 8 letters & numbers",showPercent:!1,showText:!0,animate:!0,animateSpeed:"fast",field:!1,fieldPartialMatch:!0,minimumLength:4,closestSelector:"div"},t),function(){var n=!0,r=t.showText,o=t.showPercent,i=e("<div>").addClass("pass-graybar"),l=e("<div>").addClass("pass-colorbar"),c=e("<div>").addClass("pass-wrapper").append(i.append(l));return s.closest(t.closestSelector).addClass("pass-strength-visible"),t.animate&&(c.css("display","none"),n=!1,s.closest(t.closestSelector).removeClass("pass-strength-visible")),t.showPercent&&(o=e("<span>").addClass("pass-percent").text("0%"),c.append(o)),t.showText&&(r=e("<span>").addClass("pass-text").html(t.enterPass),c.append(r)),s.closest(t.closestSelector).append(c),s.keyup((function(){var n=t.field||"";n&&(n=e(n).val());var i=function(e,s){var n=0;if(e.length<t.minimumLength)return-1;if(t.field){if(e.toLowerCase()===s.toLowerCase())return-2;if(t.fieldPartialMatch&&s.length){var r=new RegExp(s.toLowerCase());if(e.toLowerCase().match(r))return-2}}n+=4*e.length,n+=a(1,e).length-e.length,n+=a(2,e).length-e.length,n+=a(3,e).length-e.length,n+=a(4,e).length-e.length,e.match(/(.*[0-9].*[0-9].*[0-9])/)&&(n+=5);var o=".*[!,@,#,$,%,^,&,*,?,_,~]";return o=new RegExp("("+o+o+")"),e.match(o)&&(n+=5),e.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)&&(n+=10),e.match(/([a-zA-Z])/)&&e.match(/([0-9])/)&&(n+=15),e.match(/([!,@,#,$,%,^,&,*,?,_,~])/)&&e.match(/([0-9])/)&&(n+=15),e.match(/([!,@,#,$,%,^,&,*,?,_,~])/)&&e.match(/([a-zA-Z])/)&&(n+=15),(e.match(/^\w+$/)||e.match(/^\d+$/))&&(n-=10),100<n&&(n=100),n<0&&(n=0),n}(s.val(),n);s.trigger("password.score",[i]);var c=i<0?0:i;if(l.css({backgroundPosition:"0px -"+c+"px",width:c+"%"}),t.showPercent&&o.html(c+"%"),t.showText){var d=function(e){return-1===e?t.shortPass:-2===e?t.containsField:(e=e<0?0:e)<34?t.badPass:e<68?t.goodPass:t.strongPass}(i);!s.val().length&&i<=0&&(d=t.enterPass),r.html()!==e("<div>").html(d).html()&&(r.html(d),s.trigger("password.text",[d,i]))}})),t.animate&&(s.focus((function(){n||c.slideDown(t.animateSpeed,(function(){n=!0,s.closest(t.closestSelector).addClass("pass-strength-visible")}))})),s.blur((function(){!s.val().length&&n&&c.slideUp(t.animateSpeed,(function(){n=!1,s.closest(t.closestSelector).removeClass("pass-strength-visible")}))}))),this}.call(this)}e.fn.password=function(t){return this.each((function(){new s(e(this),t)}))}}(jQuery),$("#id_password1").password({shortPass:"The password is too short",badPass:"Weak; Try combining letters & numbers",goodPass:"Medium; This is okay",strongPass:"Strong password!",containsField:"The password contains your username",enterPass:"Type carefully, ensure there are no mistakes!",showPercent:!1,showText:!0,animate:!0,animateSpeed:"fast",field:"#id_username",fieldPartialMatch:!0,minimumLength:8}),strongPass1=!1,$("#id_password1").on("password.text",(e,s,t)=>{t>68?(strongPass1=!0,$(".process-button").removeClass("is-hidden")):$(".process-button").addClass("is-hidden")});