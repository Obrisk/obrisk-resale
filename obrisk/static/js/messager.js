var url;function scrollMessages(){document.querySelector("textarea[name='message']").focus(),document.querySelector("#conversation").scrollTop=9999}function addListenerMulti(e,t,s){t.split(" ").forEach(t=>e.addEventListener(t,s,!1))}function getFormatedTime(){const e=new Date;return[{month:"short"},{day:"numeric"}].map((function(t){return new Intl.DateTimeFormat("en",t).format(e)})).join(" ")+` ${e.getHours()}:${e.getMinutes()}`}document.addEventListener("DOMContentLoaded",(function(){scrollMessages();document.querySelector(".message-scroll");document.querySelector("textarea").addEventListener("keydown",autosize),addListenerMulti(document.querySelector("textarea[name='message']"),"input selectionchange",(function(e){""===document.querySelector(".textarea").value?document.getElementById("addBtn").classList.remove("is-hidden"):document.getElementById("addBtn").classList.add("is-hidden")})),document.querySelector("textarea[name='message']").addEventListener("focus",(function(e){document.getElementById("addBtn").classList.remove("is-hidden"),document.getElementById("conversation").scrollTop=9999})),document.getElementById("send").addEventListener("submit",(function(e){if(e.preventDefault(),""!==document.querySelector(".textarea").value){const e=getFormatedTime(),t=`<div class="chat-message is-sent">\n            <img src="${currentUserThumbnail}"\n            class="rounded-circle profile-avatar img-fluid" alt="pic">\n            <div class="message-block">\n                <span>${e}</span>\n                <div class="message-text">${document.getElementById("sendText").value}</div>\n            </div>\n        </div>`;document.getElementById("conversation").insertAdjacentHTML("beforeend",t),fetch("/ws/messages/send-message/",{method:"POST",body:new FormData(document.getElementById("send")),credentials:"same-origin",headers:{"X-Requested-With":"XMLHttpRequest"}}).then(e=>e.text()).then(e=>{document.getElementById("send").reset(),document.querySelector("textarea").value="",document.getElementById("addBtn").classList.remove("is-hidden"),document.querySelector("textarea[name='message']").focus(),document.getElementById("conversation").scrollTop=9999})}return!1})),document.getElementById("send-text").addEventListener("click",(function(e){e.preventDefault(),document.getElementById("send").dispatchEvent(new Event("submit",{bubbles:!0}))})),document.getElementById("sendText").addEventListener("keyup",(function(e){13!=(event.which||event.keyCode||event.charCode)||e.shiftKey||(document.getElementById("send").dispatchEvent(new Event("submit",{bubbles:!0})),setTimeout((function(e){document.getElementById("conversation").scrollTop=9999}),0))}));const e=("https:"==window.location.protocol?"wss":"ws")+"://"+window.location.host+"/ws/messages/"+currentUser+"/",t=new channels.WebSocketBridge;t.connect(e),window.onbeforeunload=function(){payload={type:"recieve",sender:currentUser,set_status:"offline",key:"set_status"},t.send(payload)},t.socket.onopen=function(){payload={type:"recieve",sender:currentUser,set_status:"online",key:"set_status"},t.send(payload)},t.listen((function(e){switch(void 0===e.key&&(e=JSON.parse(e)),e.key){case"message":""!=activeUser&&null!=activeUser&&(e.sender===activeUser?(t=e.message_id,fetch("/ws/messages/receive-message/",{method:"GET",body:{message_id:t},credentials:"same-origin",headers:{"X-Requested-With":"XMLHttpRequest"}}).then(e=>e.text()).then(e=>{document.getElementById("conversation").insertAdjacentHTML("beforeend",e),setTimeout((function(){document.getElementById("conversation").scrollTop=9999}),200)}),scrollMessages(),setTimeout((function(){document.getElementById("unread-count").classList.add("is-hidden")}),1)):document.getElementById("new-message-"+e.sender).classList.remove("is-hidden"));break;case"set_status":!function(e,t){const s=document.querySelector(".online-stat");s&&("online"===t&&e===activeUser?(document.querySelector(".status-light").style.color="#28a745",s.textContent="online"):(document.querySelector(".status-light").style.color="#ffc107",s.textContent="offline"))}(e.sender,e.set_status)}var t})),(ossUpload=new OssUpload).init()}));var images,img_error,client,imgClient,uploader={fileList:[],fileStats:{totalFilesNum:0,totalFilesSize:0,uploadFinishedFilesNum:0,curFileSize:0}},Buffer=OSS.Buffer,STS=OSS.STS,FileMaxSize=2e7,ossUpload="",obrisk_oss_url="https://obrisk.oss-cn-hangzhou.aliyuncs.com/";let retryCount=0;const retryCountMax=5;OssUpload.prototype={constructor:OssUpload,bindEvent:function(){const e=this;document.querySelector("#chooseFile, #addBtn").addEventListener("click",(function(){document.getElementById("image-file").click()})),document.querySelector('input[type="file"]').addEventListener("change",(function(t){if(t.target.files&&t.target.files[0]){const e=new FileReader;e.onload=function(){const t=getFormatedTime(),s=`<div class="chat-message is-sent">\n                          <img src="${currentUserThumbnail}"\n                            alt="pic" class="rounded-circle profile-avatar img-fluid">\n                            <div class="message-block">\n                              <span> ${t} </span>\n                              <a data-fslightbox="gallery" href="${e.result}">\n                                <img class="chat-img" src="${e.result}">\n                              </a>\n                            </div>\n                        </div>`;document.getElementById("conversation").insertAdjacentHTML("beforeend",s),document.getElementById("conversation").scrollTop=9999},e.readAsDataURL(t.target.files[0])}const s=t.target.files,n=uploader.fileList.length;let o=null;if(0==s.length)alert("No image selected , Please select one or more images");else{for(let e=0;e<s.length;e++)o=s[e],o.size<=FileMaxSize?(uploader.fileList[n+e]=o,o.id=uploader.fileList[n+e].id="image"+(n+e+1),uploader.fileStats.totalFilesSize+=o.size):alert(o.name+" is larger than 20MB, please select images small than 20MB");document.getElementById("addBtn").classList.add("is-hidden")}if(uploader.fileStats.totalFilesNum=uploader.fileList.length,0==uploader.fileStats.totalFilesNum)event.preventDefault(),alert("Please select images to upload!");else{const t=uploader.fileStats.totalFilesNum;for(let s=0;s<t;s++){const t=genKey();o=uploader.fileList[s],e.uploadFile(o,t)}uploader={fileList:[],fileStats:{totalFilesNum:0,totalFilesSize:0,uploadFinishedFilesNum:0,curFileSize:0}}}}))},uploadFile:function(e,t){applyTokenDo().then(s=>{if(void 0!==(client=s.direct?new OSS({region:s.region,accessKeyId:s.accessId,accessKeySecret:s.stsTokenKey,bucket:s.bucket}):new OSS({region:s.region,accessKeyId:s.accessKeyId,accessKeySecret:s.accessKeySecret,stsToken:s.SecurityToken,bucket:s.bucket}))){const s=async()=>{try{return await client.multipartUpload(t,e,{partSize:204800,timeout:12e4}).then((function(t){submitOSSImage(t,s,e)})).catch(e=>{console.error(e),console.log("err.name : "+e.name),console.log("err.message : "+e.message),console.log("err.request : "+e.requestId),-1!==e.name.toLowerCase().indexOf("connectiontimeout")?retryCount<5?(retryCount++,console.error("retryCount : "+retryCount),s()):(img_error=e.name+", Message: "+e.message+", RequestID: "+e.requestId,images||(images="undef,classifieds/error-img.jpg",alert("An error occured, Pls try again or add our wechatID: Obrisk"))):(img_error=e.name+", Message: "+e.message+", RequestID: "+e.requestId,images||(images="classifieds/error-img.jpg",alert("Oops! an error occured, Pls try again or add our wechatID: Obrisk")))})}catch(e){alert("Oops! an error occured, Pls try again or add our wechatID: Obrisk"),console.log(e)}};return s()}alert("Oops!, it looks like there is a network problem,             Please try again later or contact us at support@obrisk.com")}).catch(e=>{alert("Oops! an error has occured, pls try again or add our wechatID: Obrisk"),console.log(e)})}};var applyTokenDo=function(){return new Promise((e,t)=>{fetch(oss_url,{headers:{"X-Requested-With":"XMLHttpRequest"}}).then(t=>{if(!t.ok)throw new Error("Network response was not ok");e(t.json())}).catch(e=>{t(e)})})};function submitOSSImage(e,t,s){fetch(obrisk_oss_url+e.name+"?x-oss-process=image/average-hue",{headers:{"X-Requested-With":"XMLHttpRequest"}}).then(t=>{if(!t.ok)throw new Error("Network response was not ok");uploader.fileStats.uploadFinishedFilesNum++,uploader.fileStats.curFileSize+=s.size,document.getElementById("image").value=e.name,fetch("/ws/messages/send-message/",{method:"POST",body:new FormData(document.getElementById("upload")),credentials:"same-origin",headers:{"X-Requested-With":"XMLHttpRequest"}}).then(e=>e.text()).then(e=>{document.getElementById("image").value=""}).catch(e=>{alert("Image upload failed, please re-submit")})}).catch(n=>{console.log(n),retryCount<5?(retryCount++,console.error("retryCount : "+retryCount),t()):(uploader.fileStats.uploadFinishedFilesNum++,uploader.fileStats.curFileSize+=s.size,img_error=e.name+", Message: Corrupted image, RequestID: "+e.name,images||(images="undef,classifieds/error-img.jpg",alert("Oops! an error occured, please try again later")))})}function OssUpload(){const e=this;e.init=function(){e.initPage(),e.bindEvent()},e.initPage=function(){}}function genKey(){return"media/images/messages/"+usernameSlug+"/"+activeUserSlug+"/"+"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,(function(e){const t=16*Math.random()|0;return("x"==e?t:3&t|8).toString(16)}))}