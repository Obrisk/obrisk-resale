function callpay(){if(isNaN(price)||"0.00"===price)return document.getElementById("payError").innerHTML="Only priced items can accept payments",void setTimeout(()=>{document.getElementById("payError").innerHTML=""},7e3);const e=encodeURIComponent(slug);window.location.href=orderUrl+e}function onSale(e){const t=document.getElementById("meta-info");if(e.checked){const e=`\n              <div class="action-wrapper" id=actions">\n                  <a class="button action-button chat-button" href="${editItem}"\n                      title="Edit this classified">\n                      ✎Edit\n                  </a>\n                  <a class="button action-button pay-button" href="#"\n                      title="Share this classified" id="share">\n                      📤Share\n                  </a>\n              </div>`;t.nextElementSibling.remove(),t.insertAdjacentHTML("afterend",e)}else{const e='\n              <div class="notification is-warning" id="unavailable">\n                This item is no longer available\n              </div>';t.nextElementSibling.remove(),t.insertAdjacentHTML("afterend",e)}}const ui={showMask(){if(document.querySelector(".m-share-mask"))return;const e=document.createElement("div");e.className="m-share-mask",e.addEventListener("click",()=>{this.hideRightTips(),this.hideMask()}),document.body.appendChild(e),window.setTimeout(()=>{e.style.opacity=.7},0)},hideMask(){const e=document.querySelectorAll(".m-share-mask");for(let t=0;t<e.length;t++){const n=e[t];(()=>n.remove())()}},showRightTopTips(){this.showMask();const e=document.createElement("div");e.className="m-share-tips",e.innerHTML='\n      <div class="m-share-tips-w">\n        <div class="m-share-tips-p">Please tap the 3 dots“<i class="m-share-iconfont m-share-iconfont-dots"></i>”</div>\n        <div class="m-share-tips-p">On the upper right corner</div>\n      </div>\n      <div class="m-share-tips-arrow"></div>\n    ',document.body.appendChild(e),window.setTimeout(()=>{this.hideMask(),this.hideRightTips()},4400)},hideRightTips(){const e=document.querySelectorAll(".m-share-tips");for(let t=0;t<e.length;t++){e[t].remove()}}};document.addEventListener("DOMContentLoaded",(function(){wx.ready((function(){try{wx.onMenuShareAppMessage({title:title,desc:str_price+" "+descr,link:location.href,imgUrl:thumbnail,trigger:function(e){console.log(JSON.stringify(e))},success:function(e){console.log(JSON.stringify(e))},fail:function(e){console.log(JSON.stringify(e))}}),wx.onMenuShareTimeline({title:title,desc:str_price+" "+descr,link:location.href,imgUrl:thumbnail,trigger:function(e){console.log(JSON.stringify(e))},success:function(e){console.log(JSON.stringify(e))},fail:function(e){console.log(JSON.stringify(e))}})}catch(e){console.log(e)}})),wx.error((function(e){console.log(e)}));const e=document.getElementById("chat-button-id");null!==e&&e.addEventListener("click",()=>{"undefined"!=typeof currentUser?window.location.href=chatUrl:wechat_browser?window.location.href=wechatAuth:window.location.href=loginUrl});const t=document.getElementById("share");null!==t&&t.addEventListener("click",()=>{wechat_browser?ui.showRightTopTips():navigator.share({title:title,text:str_price+" "+descr,url:location.href})});const n=document.getElementById("tags");null!==n&&n.addEventListener("click",()=>{sessionStorage.restoreScroll="false"})})),"undefined"!=typeof toggler&&(window.onbeforeunload=function(){let e="E";toggler.checked!==switch_value&&(e=!0===toggler.checked?"A":"E",fetch(removeUrl,{method:"POST",body:JSON.stringify({sg:slug,st:e}),headers:{"X-Requested-With":"XMLHttpRequest","Content-Type":"application/json"},credentials:"same-origin",redirect:"follow"}).then(e=>{}).catch(e=>{console.error("failure to toggle item availability",e)}))});