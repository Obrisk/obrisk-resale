var current_conv,last_stamp,last_msg=document.getElementById("last-msg").value,current_lst_stamp=document.getElementById("last-timestamp").value;const bottomNav=document.getElementById("navbarBottom");function scrollMessages(){$("textarea[name='message']").focus(),$("#conversation").scrollTop(99999999999)}$((function(){const e=document.querySelector(".message-scroll"),s=document.querySelector("textarea");s.addEventListener("keydown",(function(){setTimeout((function(){const t=Math.min(100,s.scrollHeight);e.style.cssText="height:"+t+"px",s.style.cssText="height:"+t+"px"}),0)}));const t=function(e){const s=e+"=",t=document.cookie.split(";");for(var a=0;a<t.length;a++){for(var i=t[a];" "===i.charAt(0);)i=i.substring(1,i.length);if(0===i.indexOf(s))return i.substring(s.length,i.length)}return null},a=function(e){if(e)return function(e,s,t){let a;if(!e&&!s)return!1;if(t){const e=new Date;e.setTime(e.getTime()+24*t*60*60*1e3),a="; expires="+e.toGMTString()}else a="";document.cookie=e+"="+s+a+"; path=/"}(e,"",-1),!0};function i(e){$.ajax({type:"get",url:e,success:function(e){current_conv=e.current_conv;const s=null==e.active_thumbnail?"/static/img/user.png":e.active_thumbnail;$(".avatar-container").append(`<img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${s}"\n               alt="Picture Profile"\n                style="width:30px;height:30px;border-radius: 50%;"\n                class="user-avatar rounded-circle profile-header-avatar img-fluid"\n                id="pic">\n                `),$(".username").append(`  <span>${e.active_username}</span>`),e.msgs.map((function(t){t.sender_username==e.active_username?(null!=t.image&&$("#conversation").append(`<div class="chat-message is-received">\n                      <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${s}"\n                      alt="Picture Profile" style="width:30px;height:30px;border-radius: 50%;"\n                      class="rounded-circle profile-header-avatar img-fluid" id="pic">\n\n                      <div class="message-block">\n                          <span>${moment(t.timestamp).format("MMM. Do h:mm")}</span>\n\n                      <a data-fancybox="gallery" style="width: 250px; height: 250px;"\n                        href="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${t.image}">\n                        <img style="width: 250px; height: 250px;"\n                          src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${t.img_preview} " />\n                       </a>\n                      </div>\n                  </div > `),null!=t.classified_title&&$("#conversation").append(`<div class="chat-message is-received" style="background-color: transparent;">\n                        <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${s}"\n                        alt="Picture Profile" style="width:30px;height:30px;border-radius: 50%;"\n                        class="rounded-circle profile-header-avatar img-fluid" id="pic">\n\n                          <div class="message-block">\n                            <span>${moment(t.timestamp).format("MMM. Do h:mm")}</span>\n\n                            <div class="message-text">\n                            <div class="card classified-card mr-2 mb-3 justify-content-center is-flex"\n                            style="max-width: 295px">\n\n                            <a href="/classifieds/${t.classified_slug}"\n                            style="color:black; text-decoration:none; background-color:none" class="is-flex">\n                              <div class="card-img-top img-responsive">\n                                               <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${t.classified_thumbnail}" alt="${t.classified_title}" style="max-width: 70px">\n                              </div>\n                              <div style"margin-left: 5px">\n                                <h6 class="card-title"> ${t.classified_title} </h6>\n                                <p class="card-subtitle O-cl-red"> CNY ${t.classified_price} </p>\n                              </div>\n                            </a>\n                          </div></div>\n                      </div>\n                  </div>`),null!=t.message&&$("#conversation").append(`<div class="chat-message is-received" ><img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${s}" alt="Picture Profile"\n                          style="width:30px;height:30px;border-radius: 50%;"\n                          class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid" id="pic">\n\n                          <div class="message-block">\n                            <span>${moment(t.timestamp).format("MMM. Do h:mm")}</span>\n                            <div class="message-text">${t.message}</div>\n                          </div>\n                      </div>`)):(null!=t.image&&$("#conversation").append(`<div class="chat-message is-sent">\n\n                          <img src="${currentUserThumbnail}" alt="Picture Profile"\n                              style="width:30px;height:30px;border-radius: 50%;"\n                              class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid" id="pic">\n\n                          <div class="message-block">\n                              <span>${moment(t.timestamp).format("MMM. Do h:mm")}</span>\n                              <a data-fancybox="gallery" style="width: 250px; height: 250px;"\n                href="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${t.image}"><img\n                    style="width: 250px; height: 250px;"\n                    src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${t.img_preview} " /></a>\n                          </div>\n                      </div > `),null!=t.classified_title&&$("#conversation").append(`<div class="chat-message is-sent "style="background-color: transparent;"><img src="${currentUserThumbnail}" alt="Picture Profile"\n                          style="width:30px;height:30px;border-radius: 50%;"\n                          class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid" id="pic">\n\n                          <div class="message-block">\n                            <span>${moment(t.timestamp).format("MMM. Do h:mm")}</span>\n                            <div class="message-text"><div class="card classified-card mr-2 mb-3 justify-content-center is-flex p-2 " style="max-width: 295px">\n            <a href="/classifieds/${t.classified_slug}" style="color:black; text-decoration:none; background-color:none" class="is-flex">\n              <div class="card-img-top img-responsive">\n                <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${t.classified_thumbnail}" alt="${t.classified_title}" style="max-width: 70px">\n              </div>\n              <div style"margin-left: 5px">\n                <h6 class="card-title"> ${t.classified_title} </h6>\n                <p class="card-subtitle O-cl-red"> CNY ${t.classified_price} </p>\n              </div>\n            </a>\n          </div></div></div></div>`),null!=t.message&&$("#conversation").append(`<div class="chat-message is-sent" ><img src="${currentUserThumbnail}" alt="Picture Profile"\n                          style="width:30px;height:30px;border-radius: 50%;"\n                          class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid" id="pic">\n\n                          <div class="message-block">\n                            <span>${moment(t.timestamp).format("MMM. Do h:mm")}</span>\n                            <div class="message-text">${t.message}</div>\n                          </div>\n                      </div>`))})),$(".sendTo").val(e.active_username),activeUser=e.active_username,$("#conversation").scrollTop(99999999999)}})}t("active-chat")&&($("#chat-window").modal("show"),i(t("active-chat")),bottomNav.style.display="none",a("active-chat")),$(".open-chat").click((function(){i($(this).data("url")),bottomNav.style.display="none"})),$(".delete").click((function(e){$("#conversation").html(""),$(".avatar-container").html(""),$(".username").html(""),$("body").removeClass("modal-open"),$("body").removeClass("is-frozen"),bottomNav.style.display="block";const s=document.getElementById(current_conv);current_lst_stamp!==last_stamp&&(document.getElementsByClassName("users-list")[0].prepend(s),s.querySelector(".msg").innerHTML=last_msg,s.querySelector(".timestamp").innerHTML=last_stamp,current_lst_stamp=last_stamp),s.querySelector(".msg-notification").style.display="none"})),$("textarea[name='message']").on("input selectionchange propertychange",(function(){""===$("textarea").val()?$("#addBtn").removeClass("is-hidden"):$("#addBtn").addClass("is-hidden")})),$("textarea[name='message']").on("focus",(function(e){$("#addBtn").removeClass("is-hidden"),$("#conversation").scrollTop(99999999999)})),$("#send").submit((function(e){if(e.preventDefault(),""!==$("textarea").val()){const e=moment().format("MMM. Do h:mm"),s=`<div class="chat-message is-sent">\n            <img src="${currentUserThumbnail}"\n            alt="Picture Profile" style="width:30px;height:30px;border-radius: 50%;"\n            class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid"\n            id="pic">\n            <div class="message-block">\n                <span>${e}</span>\n                <div class="message-text">${$("#sendText").val()}</div>\n            </div>\n        </div>`;$("#conversation").append(s),$.ajax({url:"/ws/messages/send-message/",data:$("#send").serialize(),cache:!1,type:"POST",success:function(s){""===(last_msg=$("#sendText").val().substring(0,50))&&(last_msg="Attachment"),last_stamp=e,$("#send")[0].reset(),$("textarea").val(""),$("textarea[name='message']").focus(),$("#conversation").scrollTop(99999999999)},fail:function(){$.wnoty({type:"error",autohide:!1,message:"failed to send the message"})}})}return!1})),$("#send-text").click((function(e){e.preventDefault(),$("#send").trigger("submit")})),$("#sendText").keypress((function(e){13!=e.which||e.shiftKey||$(".send-btn").is('[disabled="disabled"]')||($("#send").trigger("submit"),setTimeout((function(e){$("#conversation").scrollTop(99999999999)}),0))}));const r=("https:"==window.location.protocol?"wss":"ws")+"://"+window.location.host+"/ws/messages/"+currentUser+"/",n=new channels.WebSocketBridge;n.connect(r),window.onbeforeunload=function(){payload={type:"recieve",sender:currentUser,set_status:"offline",key:"set_status"},n.send(payload)},n.socket.onopen=function(){payload={type:"recieve",sender:currentUser,set_status:"online",key:"set_status"},n.send(payload)},n.listen((function(e){switch(void 0===e.key&&(e=JSON.parse(e)),e.key){case"message":""!=activeUser&&null!=activeUser&&(e.sender===activeUser?(s=e.message_id,$.ajax({url:"/ws/messages/receive-message/",data:{message_id:s},cache:!1,success:function(e){$("#conversation").append(e),setTimeout((function(){$("#conversation").scrollTop(99999999999)}),200)}}),scrollMessages(),setTimeout((function(){$("#unread-count").hide()}),1)):$("#new-message-"+e.sender).show());break;case"set_status":!function(e,s){const t=$(".online-stat");t&&("online"===s&&e===activeUser?($(".status-light").css("color","#28a745"),t.text("online")):($(".status-light").css("color","#ffc107"),t.text("offline")))}(e.sender,e.set_status)}var s;scrollMessages()}))}));var images,img_error,client,imgClient,uploader={fileList:[],fileStats:{totalFilesNum:0,totalFilesSize:0,uploadFinishedFilesNum:0,curFileSize:0}},Buffer=OSS.Buffer,STS=OSS.STS,FileMaxSize=13e6,ossUpload="",obrisk_oss_url="https://obrisk.oss-cn-hangzhou.aliyuncs.com/";let retryCount=0;const retryCountMax=5;OssUpload.prototype={constructor:OssUpload,bindEvent:function(){const s=this;$("#chooseFile, #addBtn").click((function(){document.getElementById("image-file").click()})),$('input[type="file"]').change((function(e){if(e.target.files&&e.target.files[0]){const s=new FileReader;s.onload=function(){const e=`<div class="chat-message is-sent"><img src="${currentUserThumbnail}" alt="Picture Profile" style="width:30px;height:30px;border-radius: 50%;" class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid is-hidden-mobile" id="pic"><div class="message-block"><span>${moment().format("MMM. Do h:mm")}</span><a data-fancybox="gallery" href="${s.result}"><img style="width: 250px; height: 250px;" src="${s.result}"></a></div></div>`;$("#conversation").append(e),$("#conversation").scrollTop(99999999999)},s.readAsDataURL(e.target.files[0])}var t=e.target.files,a=uploader.fileList.length,i=t.length,r=null;if($("#uploader .placeholder").hide(),$("#statusBar").css("display","flex"),0==t.length)alert("No image selected , Please select one or more images");else{for(var n=0;n<i;n++)(r=t[n]).size<=FileMaxSize?(uploader.fileList[a+n]=r,r.id=uploader.fileList[a+n].id="image"+(a+n+1),uploader.fileStats.totalFilesSize+=r.size):alert(r.name+" is larger than 13MB, please select images small than 13MB ");$(".addBtn").hide()}if(uploader.fileStats.totalFilesNum=uploader.fileList.length,0==uploader.fileStats.totalFilesNum)event.preventDefault(),alert("Please select images to upload!"),$(".start-uploader").css("display","block");else{var o=uploader.fileStats.totalFilesNum;for(n=0;n<o;n++){var l=genKey();r=uploader.fileList[n],s.uploadFile(r,l)}uploader={fileList:[],fileStats:{totalFilesNum:0,totalFilesSize:0,uploadFinishedFilesNum:0,curFileSize:0}}}})),$(".retry-upload").on("click",(function(t){e.preventDefault();for(var a=uploader.fileStats.totalFilesNum,i=0;i<a;i++){var r=genKey();file=uploader.fileList[i],s.uploadFile(file,r)}uploader={fileList:[],fileStats:{totalFilesNum:0,totalFilesSize:0,uploadFinishedFilesNum:0,curFileSize:0}}}))},uploadFile:function(e,s){$totalProgressbar.css("width","30%").html("Uploading..."),applyTokenDo().then(t=>{if(void 0!==(client=t.direct?new OSS({region:t.region,accessKeyId:t.accessId,accessKeySecret:t.stsTokenKey,bucket:t.bucket}):new OSS({region:t.region,accessKeyId:t.accessKeyId,accessKeySecret:t.accessKeySecret,stsToken:t.SecurityToken,bucket:t.bucket}))){const t=async()=>{try{return await client.multipartUpload(s,e,{progress:progress,partSize:204800,timeout:12e4}).then((function(s){$.ajax({url:obrisk_oss_url+s.name+"?x-oss-process=image/average-hue",success:function(){$("#"+e.id).children(".success-span").addClass("success"),$("#"+e.id).children(".file-panel").hide(),uploader.fileStats.uploadFinishedFilesNum++,uploader.fileStats.curFileSize+=e.size,progressBarNum=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2),progressBar=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2)+"%",100==progressBarNum?$totalProgressbar.css("width",progressBar).html("Upload complete"):$totalProgressbar.css("width",progressBar).html(progressBar),$("#image").val(s.name),$.ajax({url:"/ws/messages/send-message/",data:$("#upload").serialize(),cache:!1,type:"POST",success:function(e){$("#image").val("")},fail:function(e){$("body").trigg("showRetry"),console.log(e)}})},error:function(a){retryCount<5?(retryCount++,console.error("retryCount : "+retryCount),t()):($("#"+e.id).children(".success-span").addClass("fail"),$("#"+e.id).children(".file-panel").hide(),uploader.fileStats.uploadFinishedFilesNum++,uploader.fileStats.curFileSize+=e.size,progressBarNum=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2),progressBar=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2)+"%",100==progressBarNum?$totalProgressbar.css("width",progressBar).html("Upload complete"):$totalProgressbar.css("width",progressBar).html(progressBar),img_error=s.name+", Message: Corrupted image, RequestID: "+s.name,images||(images="undef,classifieds/error-img.jpg",alert("Oops! an error occured when uploading your image(s). Please try again later")))}})})).catch(e=>{console.error(e),console.log("err.name : "+e.name),console.log("err.message : "+e.message),console.log("err.request : "+e.requestId),$totalProgressbar.css("width","40%").html("Retrying..."),-1!==e.name.toLowerCase().indexOf("connectiontimeout")?retryCount<5?(retryCount++,console.error("retryCount : "+retryCount),t()):($totalProgressbar.css("width","94%").html("Completed with minor errors!"),$("ul.filelist li").children(".success-span").addClass("fail"),img_error=e.name+", Message: "+e.message+", RequestID: "+e.requestId,images||(images="undef,classifieds/error-img.jpg",alert("Oops! an error occured when uploading your image(s). Please try again later"))):($totalProgressbar.css("width","94%").html("Completed with minor errors!"),img_error=e.name+", Message: "+e.message+", RequestID: "+e.requestId,images||(images="undef,classifieds/error-img.jpg",alert("Oops! an error occured when uploading your image(s). Please try again later")))})}catch(e){alert("Oops! an error occured when uploading your image(s),                     Please try again later or contact us via support@obrisk.com. "+e),$(".start-uploader").css("display","block"),console.log(e)}};return t()}alert("Oops!, it looks like there is a network problem,             Please try again later or contact us at support@obrisk.com"),$(".start-uploader").css("display","block")}).catch(e=>{alert("Oops! an error occured before upload started, Please try again later or contact us via support@obrisk.com"+e),console.log(e)})}};var progressBar=0,progress="",$wrap=$("#uploader"),$queue=$('<ul class="filelist"></ul>').appendTo($wrap.find(".queueList")),$totalProgressbar=$("#totalProgressBar"),applyTokenDo=(progress=function(e){return function(e){$totalProgressbar.css("width",progressBar),e()}},function(){return new Promise((e,s)=>{$.ajax({url:oss_url,success:function(s){e(s)},error:function(e){s(e)}})})});function OssUpload(){const e=this;e.init=function(){e.initPage(),e.bindEvent()},e.initPage=function(){}}function genKey(){return"media/images/messages/"+currentUser+"/"+activeUser+"/"+"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,(function(e){var s=16*Math.random()|0;return("x"==e?s:3&s|8).toString(16)}))}function slugify(e){const s="àáäâãåăæçèéëêǵḧìíïîḿńǹñòóöôœøṕŕßśșțùúüûǘẃẍÿź·/_,:;",t=new RegExp(s.split("").join("|"),"g");return e.toString().toLowerCase().replace(/\s+/g,"-").replace(t,e=>"aaaaaaaaceeeeghiiiimnnnooooooprssstuuuuuwxyz------".charAt(s.indexOf(e))).replace(/&/g,"-and-").replace(/[^\w\-]+/g,"").replace(/\-\-+/g,"-").replace(/^-+/,"").replace(/-+$/,"")}document.addEventListener("DOMContentLoaded",(function(){(ossUpload=new OssUpload).init()})),navigator.share=navigator.share||function(){if(navigator.share)return navigator.share;let e=navigator.userAgent.match(/Android/i),s=!(navigator.userAgent.match(/iPhone|iPad|iPod/i)||e),t=e=>(s?"https://api.whatsapp.com/send?text=":"whatsapp://send?text=")+e,a=(e,s)=>"mailto:?subject="+s+"&body="+e,i=e=>"sms:?body="+e;const r=new class{_init(){if(this._initialized)return Promise.resolve();this._initialized=!0;const e=document.createElement("div");e.innerHTML='<div class="web-share" style="display: none">\n      <div class="web-share-container web-share-grid">\n        <div class="web-share-title">SHARE VIA</div>\n        <a class="web-share-item web-share-whatsapp" data-action="share/whatsapp/share" target="_blank">\n          <div class="web-share-icon-whatsapp"></div>\n          <div class="web-share-item-desc">Whatsapp</div>\n        </a>\n        <a class="web-share-item web-share-email">\n          <div class="web-share-icon-email"></div>\n          <div class="web-share-item-desc">Email</div>\n        </a>\n        <a class="web-share-item web-share-sms">\n          <div class="web-share-icon-sms"></div>\n          <div class="web-share-item-desc">SMS</div>\n        </a>\n        <a class="web-share-item web-share-copy">\n          <div class="web-share-icon-copy"></div>\n          <div class="web-share-item-desc">Copy</div>\n        </a>\n      </div>\n      <div class="web-share-container web-share-cancel">Cancel</div>\n    </div>',this.$root=e.querySelector(".web-share"),this.$whatsapp=e.querySelector(".web-share-whatsapp"),this.$email=e.querySelector(".web-share-email"),this.$sms=e.querySelector(".web-share-sms"),this.$copy=e.querySelector(".web-share-copy"),this.$copy.onclick=()=>this._copy(),this.$root.onclick=()=>this._hide(),this.$root.classList.toggle("desktop",s),document.body.appendChild(e)}_setPayload(e){let s=e.text+"  Click the link to view. "+e.url,r=e.title;this.url=e.url,s=encodeURIComponent(s),r=encodeURIComponent(r),this.$whatsapp.href=t(s),this.$email.href=a(s,r),this.$sms.href=i(s)}_copy(){const e=document.createElement("span");e.textContent=this.url,e.style.whiteSpace="pre",e.style.position="absolute",e.style.left="-9999px",e.style.top="-9999px";const s=window,t=s.getSelection();s.document.body.appendChild(e);const a=s.document.createRange();t.removeAllRanges(),a.selectNode(e),t.addRange(a);let i=!1;try{i=s.document.execCommand("copy")}catch(e){}return t.removeAllRanges(),e.remove(),i}show(e){this._init(),clearTimeout(this._hideTimer),this._setPayload(e),this.$root.style.display="flex",this.$root.offsetWidth,this.$root.style.background="rgba(0,0,0,.4)",document.querySelectorAll(".web-share-container").forEach(e=>{e.style.transform="translateY(0)",e.style.opacity=1})}_hide(){this.$root.style.background=null,document.querySelectorAll(".web-share-container").forEach(e=>{e.style.transform=null,e.style.opacity=null}),this._hideTimer=setTimeout(()=>this.$root.style.display=null,400)}};return e=>r.show(e)}();