function wxpayFail(e=!1){document.getElementsByClassName("notification")[0].classList.remove("is-hidden"),document.getElementById("notf-msg").innerHTML=!0===e?"Payment done✌️. We'll get in touch soon to confirm the logistics😊":"Sorry payments feature is now unavailable, contact the seller directly🙇",setTimeout(()=>{window.location.href=slugURL},9e3)}document.addEventListener("DOMContentLoaded",(function(){wx.ready((function(){if(dataError.length>1)wxpayFail(),console.log(dataError);else try{wx.chooseWXPay({timestamp:timestamp,nonceStr:nonceStr,package:packge,signType:signType,paySign:paySign,trigger:function(e){console.log(JSON.stringify(e))},success:function(e){let o=null,n=null;getCookie("classified-order-is-offline")||(o=getCookie("classified-order-phone"),n=getCookie("classified-order-address")),fetch(paySuccessURL,{method:"POST",body:JSON.stringify({addr:n,phone:o,sg:slug}),headers:{"X-Requested-With":"XMLHttpRequest","Content-Type":"application/json"},credentials:"same-origin",redirect:"follow"}).then(e=>e.json()).then(e=>{!0===e.success?window.location.replace("https://obrisk.com/classifieds/orders/wsguatpotlfwccdi/"+e.order_slug):wxpayFail(pay_complete=!0)})},fail:function(e){wxpayFail(),console.log(JSON.stringify(e))},cancel:function(e){window.location.replace(slugURL)}})}catch{wxpayFail(),console.log("failure to init payments, exception happened")}})),wx.error((function(e){wxpayFail(),console.log(e)}))}));