var xDown=null,yDown=null;function callpay(){if(isNaN(price)||"0.00"===price)return document.getElementById("payError").innerHTML="Only priced items can accept payments",void setTimeout(()=>{document.getElementById("payError").innerHTML=""},7e3);const e=encodeURIComponent(slug);window.location.href=orderUrl+e}function handleTouchMove(e){if(xDown&&yDown){var n=e.touches[0].clientX,t=e.touches[0].clientY,o=xDown-n,i=yDown-t;Math.abs(o)>Math.abs(i)&&new Promise(e=>setTimeout(e,700)).then(()=>{const e=Math.min(document.querySelector(".is-active.is-visible .classified-image").offsetHeight,.7*visualViewport.height);document.getElementById("image-overlay").style.top=e-34+"px",document.getElementById("image-section").style.maxHeight=e+"px"}),xDown=null,yDown=null}}function handleTouchStart(e){const n=e.touches[0];xDown=n.clientX,yDown=n.clientY}document.addEventListener("DOMContentLoaded",(function(){wx.ready((function(){try{wx.onMenuShareAppMessage({title:title,desc:str_price+descr,link:location.href,imgUrl:thumbnail,trigger:function(e){console.log(JSON.stringify(e))},success:function(e){console.log(JSON.stringify(e))},fail:function(e){console.log(JSON.stringify(e))}}),wx.onMenuShareTimeline({title:title,desc:str_price+descr,link:location.href,imgUrl:thumbnail,trigger:function(e){console.log(JSON.stringify(e))},success:function(e){console.log(JSON.stringify(e))},fail:function(e){console.log(JSON.stringify(e))}})}catch(e){console.log(e)}})),wx.error((function(e){console.log(e)}))}));