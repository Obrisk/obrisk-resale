const username_el=document.getElementById("id_username"),username_err=document.getElementById("username-errors");var phone_no,verify_counter=0,code_counter=0;const confirm_btn=document.querySelector("#confirm"),code_notice=document.getElementById("code-notice"),send_code_btn=document.getElementById("send-code"),results=document.getElementById("results"),phone_number=document.getElementById("id_phone_number"),verify_code_input=document.getElementById("verify-code"),panel_two=document.getElementById("signup-panel-2"),request_unverify=document.getElementById("request-unverified-phone"),unverify_form=document.getElementById("unverify-form"),signup_loading=document.getElementById("signup-loading-popup");function printError(e){document.getElementsByClassName("notification")[0].classList.remove("is-hidden"),document.getElementById("notf-msg").innerHTML=e}confirm_btn.addEventListener("click",(function(e){document.getElementById("city").value&&document.getElementById("province").value?username_el.value.length<3||username_el.value.length>16||/\s/.test(username_el.value)?(e.preventDefault(),username_err.innerHTML="Must be 3 to 16 letters, without spaces!"):(document.querySelector("#signup-panel-1").style.display="none",document.querySelector(".process-panel-wrap").classList.remove("is-active"),document.querySelector("#signup-panel-2").classList.remove("is-hidden"),document.querySelector("#signup-panel-2").classList.add("is-active")):(e.preventDefault(),printError("Please enter your city and province!"))})),document.addEventListener("DOMContentLoaded",(function(){document.querySelectorAll(".close-dj-messages").forEach(e=>{e.addEventListener("click",e=>{e.currentTarget.parentElement.classList.add("is-hidden"),e.stopPropagation()})});var e=username_el.value.length;function n(){return fetch("/users/cmplt-wx-reg-149eb8766awswdff224fgo029k12ol8/",{method:"POST",body:document.querySelector("form").serialize(),credentials:"same-origin",headers:{"X-Requested-With":"XMLHttpRequest"},redirect:"follow"}).then(e=>e.json()).then(e=>{!0===e.success?window.location.replace(e.nxt):(results.innerHTML="<p class='error-text'>"+e.error_message+"</p>",signup_loading.style.display="none",send_code_btn.disabled=!1,verify_code_input.disabled=!1,document.getElementById("verify-code").disabled=!1,unverify_form.style.display="none",panel_two.classList.remove("blur-in"),panel_two.classList.add("blur-out"),(code_counter+=1)>=5&&(verify_code_input.disabled=!0,printError("Max number of code retrial has reached, Try again later!")))}),!1}function t(){if(document.getElementsByClassName("loading")[0].classList.remove("is-hidden"),!isNaN(verify_code_input.value)&&6===verify_code_input.value.length&&!isNaN(phone_number.value))return!1===phone_number.value.toString().startsWith("+86")&&(phone_number.value="+86"+phone_number.value),signup_loading.style.display="flex",n(),!1;event.preventDefault(),results.innerHTML="<p class='error-text'> The code or number is not correct!<p>"}username_el.setSelectionRange(e,e),send_code_btn.addEventListener("click",(function(e){if(phone_number.value){var n=parseInt(phone_number.value),t=n.toString();if(!isNaN(n)&&11==t.length&&1==t.charAt(0))return $.ajax({url:"/users/verification-code/",data:{phone_no:n},cache:!1,type:"GET",success:function(e){if(!0===e.success){timeout=60,send_code_btn.disabled=!0,document.getElementById("code").classList.remove("is-hidden"),null!=e.message&&(code_notice.innerHTML="<p class='pass-text'>"+e.message+"<p>",verify_code_input.focus());let n=setInterval(()=>(timeout--,void(timeout>0?(send_code_btn.textContent=timeout+" S",30===timeout&&""===verify_code_input.value&&(request_unverify.style.cssText+=";display:block !important;")):(send_code_btn.textContent="Resend Code",send_code_btn.disabled=!1,verify_code_input.disabled=!1))),1e3);setTimeout(()=>{clearInterval(n)},61e3),(verify_counter+=1)>=7&&(send_code_btn.disabled=!0,printError("Maximum number of sending SMS has reached, Try again later!"))}else null!=e.error_message&&(code_notice.innerHTML="<p class='error-text'>"+e.error_message+"<p>"),null!=e.messageId&&console.log(e.messageId),null!=e.requestId&&console.log(e.requestId),null!=e.returnedCode&&console.log(e.returnedCode),null!=e.retries&&console.log(e.retries)},error:function(e){code_notice.innerHTML="<p class='error-text'> The signup is closed! Please try again later!<p>",console.log(e)}}),!1;e.preventDefault(),code_notice.innerHTML="<p class='error-text'>Don't enter country code or special characters<p>"}else e.preventDefault(),code_notice.innerHTML="<p class='error-text'>Please enter a valid phone number!<p>"})),request_unverify.addEventListener("click",e=>{unverify_form.style.cssText+=";display:block !important;",document.getElementById("id_notes").focus(),panel_two.classList.remove("blur-out"),panel_two.classList.add("blur-in"),e.stopPropagation()}),document.getElementById("close-unverify-form").addEventListener("click",e=>{unverify_form.style.display="none",panel_two.classList.remove("blur-in"),panel_two.classList.add("blur-out"),e.stopPropagation()}),username_el.addEventListener("keyup",e=>{fetch("/users/username-exists/?username="+e.target.value).then(e=>e.json()).then(e=>{"201"===e.status?(username_err.innerHTML="This username is already taken!",confirm_btn.disabled=!0):(username_err.innerHTML="",confirm_btn.disabled=!1)})}),verify_code_input.addEventListener("keyup",e=>{6===verify_code_input.value.length&&t()}),document.getElementById("submit-code").addEventListener("click",e=>{t()}),document.getElementById("cant-verify-submit").addEventListener("click",e=>{if(!isNaN(phone_number.value)&&11==phone_number.value.length.toString()&&1==phone_number.value.charAt(0))return document.getElementById("id_unverified_phone").value=phone_number.value,phone_number.value="",signup_loading.style.display="flex",n(),!1;e.preventDefault(),results.innerHTML="<p class='error-text'> The phone number is not correct!<p>",unverify_form.style.display="none",panel_two.classList.remove("blur-in"),panel_two.classList.add("blur-out"),e.stopPropagation()})}));