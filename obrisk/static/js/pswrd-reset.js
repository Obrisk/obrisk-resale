const csrftoken=document.querySelector("[name=csrfmiddlewaretoken]").value;$((function(){$.ajaxSetup({beforeSend:function(e,t){var r;r=t.type,/^(GET|HEAD|OPTIONS|TRACE)$/.test(r)||this.crossDomain||e.setRequestHeader("X-CSRFToken",csrftoken)}})}));var phone_no,verify_counter=0,code_counter=0;function printError(e){document.getElementsByClassName("notification")[0].classList.remove("is-hidden"),document.getElementById("notf-msg").innerHTML=e}$((function(){function e(e){if(6==document.querySelector("#code").value.length){$(".loading").hasClass("is-hidden")&&$(".loading").toggleClass("is-hidden");const e=parseInt($("#id_phone_number").val()),t=e.toString();if(!(isNaN(e)||t.length<11||t.length>14))return $.ajax({url:"/users/phone-verify/",data:{phone_no:$("#id_phone_number").val(),code:$("#code").val()},cache:!1,type:"GET",success:function(e){1==e.success?(e.url?($("#results").empty().append("<p class='error-text'>Successfully verified your number! Redirecting... <p>"),window.location.href=e.url):($("#results").empty().append("<p class='error-text'> You have successfully verified your phone number! <p>"),$("input[name='verified_no']").val("YES"),$("#signup-panel-1").hide(),$(".process-panel-wrap").removeClass("is-active"),$(".step-title").removeClass("is-active")),$(".step-dot-2").removeClass("is-hidden"),$(".step-dot-2").addClass("is-active")):($("#results").empty().append("<p class='error-text'>"+e.error_message+"</p>"),$("#send-code").attr("disabled",!1),(code_counter+=1)>=7&&($("#phone-verify").attr("disabled",!0),printError("Maximum number of code retrial, you can't retry anymore!"))),$(".loading").removeClass("is-hidden")},error:function(e){printError(e)}}),!1;event.preventDefault(),$("#results").empty().append("<p class='error-text'> Phone number is incorrect! <p>")}}document.getElementById("id_phone_number").removeAttribute("disabled"),document.querySelectorAll(".close-dj-messages").forEach(e=>{e.addEventListener("click",e=>{e.currentTarget.parentElement.classList.add("is-hidden"),e.stopPropagation()})}),$("#send-code").click((function(e){if($("#id_phone_number").val()){const n=parseInt($("#id_phone_number").val()),s=n.toString();var t,r;if(!isNaN(n)&&11==s.length&&1==s.charAt(0))return"/users/phone-password-reset/"==current_url?(t="/users/phone-password-reset/",r="POST"):(t="/users/verification-code/",r="GET"),$.ajax({url:t,data:{phone_no:n},cache:!1,type:r,success:function(e){if(1==e.success){timeout=60,$("#send-code").attr("disabled",!0),$("#phone_label").hide(),null!=e.message&&$("#code-notice").empty().append("<p class='pass-text'>"+e.message+"<p>");let t=setInterval(()=>(timeout--,void(timeout>0?$("#send-code").text(timeout+" S"):($("#send-code").text("Get Code"),$("#send-code").attr("disabled",!1)))),1e3);setTimeout(()=>{clearInterval(t)},61e3),(verify_counter+=1)>=7&&($("#send-code").attr("disabled",!0),printError("Max number of sending SMS has reached, Try again later!"))}else null!=e.error_message&&$("#code-notice").empty().append("<p class='error-text'>"+e.error_message+"<p>"),null!=e.messageId&&console.log(e.messageId),null!=e.requestId&&console.log(e.requestId),null!=e.returnedCode&&console.log(e.returnedCode),null!=e.retries&&console.log(e.retries)},error:function(e){$("#code-notice").empty().append("<p class='error-text'> Sorry, Please try again later!<p>"),console.log(e)}}),!1;e.preventDefault(),$("#code-notice").empty().append("<p class='error-text'> Don't include country code or special characters<p>")}else e.preventDefault(),$("#code-notice").empty().append("<p class='error-text'>Please enter a valid phone number!<p>")})),$("#code").keyup((function(t){e()})),$("#submit-ps-reset").click((function(t){e()}))}));