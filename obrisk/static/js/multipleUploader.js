var uploader={fileList:[],fileStats:{totalFilesNum:0,totalFilesSize:0,uploadFinishedFilesNum:0,curFileSize:0}};const Buffer=OSS.Buffer,STS=OSS.STS,obrisk_oss_url="https://obrisk.oss-cn-hangzhou.aliyuncs.com/",MaxImageSize=13e6,MaxVideoSize=2e8,s3Upload=!1,aliyunUpload=!0;var img_error,client,imgClient,images="",videos="",ossUpload="",files="",curIndex=0,NumberOfSelectedFiles=0,hasErrors=!1,retryCount=0,retryCountMax=5,TotalFilesMaxSize=8;OssUpload.prototype={constructor:OssUpload,bindEvent:function(){var e=this;$("#chooseFile, #addBtn").click((function(){document.getElementById("image-file").click()})),$("#addVideo").click((function(){document.getElementById("video-file").click()})),$("#image-file").change((function(s){$("#wrapper .container").css("display","block"),$(".submit-button").removeClass("is-disabled"),files=s.target.files,curIndex=uploader.fileList.length,NumberOfSelectedFiles=files.length;var t=null;$("#uploader .placeholder").hide();var r=TotalFilesMaxSize-curIndex;if(0===r)$.wnoty({type:"error",autohide:!1,message:"Only "+TotalFilesMaxSize+" images are allowed"}),$("#addBtn").hide();else if(0===files.length)$.wnoty({type:"error",autohide:!1,message:"No image selected , Please select one or more images"});else if(NumberOfSelectedFiles<=r&&NumberOfSelectedFiles>0)for(var a=0;a<NumberOfSelectedFiles;a++)(t=files[a]).size<=13e6?(uploader.fileList[curIndex+a]=t,t.id=uploader.fileList[curIndex+a].id="image"+(curIndex+a+1),uploader.fileStats.totalFilesSize+=t.size,e.addFile(t),$("#addVideo").hide()):$.wnoty({type:"error",autohide:!1,message:t.name+" is larger than 13MB, please select images small than 13MB "});else{for(a=0;a<NumberOfSelectedFiles&&uploader.fileList.length<TotalFilesMaxSize;a++)(t=files[a]).size<=13e6?(uploader.fileList[curIndex+a]=t,t.id=uploader.fileList[curIndex+a].id="image"+(curIndex+a+1),uploader.fileStats.totalFilesSize+=t.size,e.addFile(t),$("#addVideo").hide()):$.wnoty({type:"error",autohide:!1,message:t.name+" is larger than 13MB, please select images small than 13MB "});$.wnoty({type:"error",autohide:!1,message:"Only "+TotalFilesMaxSize+" images are allowed"})}uploader.fileStats.totalFilesNum=uploader.fileList.length})),$("#video-file").change((function(s){$("#wrapper .container").css("display","block"),$(".submit-button").removeClass("is-disabled"),files=s.target.files,curIndex=uploader.fileList.length,NumberOfSelectedFiles=files.length;var t=null;$("#uploader .placeholder").hide();var r=1-curIndex;if(0==r)$.wnoty({type:"error",autohide:!1,message:"Only 1 video is allowed"}),$("#addVideo").hide();else if(0==files.length)$.wnoty({type:"error",autohide:!1,message:"No video selected, Please select one or more videos"});else if(NumberOfSelectedFiles<=r&&NumberOfSelectedFiles>0)for(var a=0;a<NumberOfSelectedFiles;a++)(t=files[a]).size<=2e8?(uploader.fileList[curIndex+a]=t,t.id=uploader.fileList[curIndex+a].id="video"+(curIndex+a+1),uploader.fileStats.totalFilesSize+=t.size,e.addFile(t),$("#addBtn").hide()):$.wnoty({type:"error",autohide:!1,message:t.name+" is larger than 13MB, please select videos small than 13MB "});else{for(a=0;a<NumberOfSelectedFiles&&uploader.fileList.length<1;a++)(t=files[a]).size<=2e8?(uploader.fileList[curIndex+a]=t,t.id=uploader.fileList[curIndex+a].id="video"+(curIndex+a+1),uploader.fileStats.totalFilesSize+=t.size,e.addFile(t),$("#addBtn").hide()):$.wnoty({type:"error",autohide:!1,message:t.name+" is larger than 13MB, please select videos small than 13MB "});$.wnoty({type:"error",autohide:!1,message:"Only 1 video is allowed"})}uploader.fileStats.totalFilesNum=uploader.fileList.length})),$("body").on("submitClicked",(function(){$("#statusBar").css("display","flex");var s,t=uploader.fileStats.totalFilesNum;$(".start-uploader").css("display","none"),$totalProgressbar.css("width","40%").html("Upload Started please wait...");for(var r=0;r<t;r++){var a=genKey((s=uploader.fileList[r]).type);e.uploadFile(s,a,s.type)}})),$(".queueList .filelist").delegate("li span.cancel","click",(function(){for(var e=$(this).parent().parent(),s=e.attr("id"),t=uploader.fileList.length,r=0;r<t;r++)if(t<=0&&($("#addBtn").show(),$("#addVideo").hide()),uploader.fileList[r].id==s){uploader.fileStats.totalFilesSize-=uploader.fileList[r].size,uploader.fileList.splice(r,1),uploader.fileStats.totalFilesNum=uploader.fileList.length;break}e.remove(),0==uploader.fileList.length&&($("#wrapper .placeholder").css("display","block"),$("#addBtn").show(),$("#addVideo").show())}))},uploadFile:function(e,s,t){$totalProgressbar.css("width","30%").html("Uploading..."),applyTokenDo().then(r=>{if(void 0!==(client=r.direct?new OSS({region:r.region,accessKeyId:r.accessId,accessKeySecret:r.stsTokenKey,bucket:r.bucket}):new OSS({region:r.region,accessKeyId:r.accessKeyId,accessKeySecret:r.accessKeySecret,stsToken:r.SecurityToken,bucket:r.bucket}))){const r=async()=>{try{return await client.multipartUpload(s,e,{progress:progress,partSize:204800,timeout:12e4}).then((function(s){/^video/.test(t)?url=obrisk_oss_url+s.name:url=obrisk_oss_url+s.name+"?x-oss-process=image/average-hue",$.ajax({url:url,success:function(){$("#"+e.id).children(".success-span").addClass("success"),$("#"+e.id).children(".file-panel").hide(),uploader.fileStats.uploadFinishedFilesNum++,uploader.fileStats.curFileSize+=e.size,progressBarNum=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2),progressBar=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2)+"%",/^image/.test(t)?images+=""==images?s.name:","+s.name:videos+=""==videos?s.name:","+s.name,100==progressBarNum?($totalProgressbar.css("width",progressBar).html("Upload complete"),$("body").trigger("uploadComplete")):(progressBar=parseFloat(progressBar),$totalProgressbar.css("width",progressBar.toFixed(0)).html(progressBar))},error:function(t){retryCount<retryCountMax?(retryCount++,console.error("retryCount : "+retryCount),r()):($("#"+e.id).children(".success-span").addClass("fail"),$("#"+e.id).children(".file-panel").hide(),uploader.fileStats.uploadFinishedFilesNum++,uploader.fileStats.curFileSize+=e.size,progressBarNum=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2),progressBar=100*(uploader.fileStats.curFileSize/uploader.fileStats.totalFilesSize).toFixed(2)+"%",100==progressBarNum?$totalProgressbar.css("width",progressBar).html("Upload complete"):$totalProgressbar.css("width",progressBar).html(progressBar),img_error=s.name+", Message: Corrupted image, RequestID: "+s.name,$("#retry-button").removeClass("is-hidden"),images||("classifieds"==app?(images="classifieds/error-img.jpg",$.wnoty({type:"error",autohide:!1,message:"Sorry an error occured when uploading your image(s).                                                     You can submit this post without images ."})):$.wnoty({type:"error",autohide:!1,message:"Sorry! an error occured when uploading your image(s). You can still post without images"})))}})})).catch(e=>{console.error(e),console.log("err.name : "+e.name),console.log("err.message : "+e.message),console.log("err.request : "+e.requestId),$totalProgressbar.css("width","40%").html("Retrying..."),-1!==e.name.toLowerCase().indexOf("connectiontimeout")?retryCount<retryCountMax?(retryCount++,console.error("retryCount : "+retryCount),r()):($totalProgressbar.css("width","94%").html("Completed with minor errors!"),$("ul.filelist li").children(".success-span").addClass("fail"),$("#addBtn").hide(),img_error=e.name+", Message: "+e.message+", RequestID: "+e.requestId,$("#retry-button").removeClass("is-hidden"),images||("classifieds"==app&&(images="classifieds/error-img.jpg"),$.wnoty({type:"error",autohide:!1,message:"Oops! an error occured when uploading your image(s).                                             But you can submit this post without images ."}))):($totalProgressbar.css("width","94%").html("Completed with minor errors!"),img_error=e.name+", Message: "+e.message+", RequestID: "+e.requestId,$("#retry-button").removeClass("is-hidden"),images||("classifieds"==app&&(images="classifieds/error-img.jpg"),console.log(hasErrors),hasErrors||($.wnoty({type:"error",autohide:!1,message:"Oops! an error occured when uploading your image(s).                                             But you can submit this post without images ."}),hasErrors=!0)))})}catch(e){$.wnoty({type:"error",autohide:!1,message:"Oops! an error occured when uploading your image(s),                     Please try again later or contact us via support@obrisk.com. "}),$(".start-uploader").css("display","block"),console.log(e)}};return r()}$.wnoty({type:"error",autohide:!1,message:"Oops!, it looks like there is a network problem,                 try again later or contact us at support@obrisk.com"}),$(".start-uploader").css("display","block")}).catch(e=>{$.wnoty({type:"error",autohide:!1,message:"Oops! an error occured before upload started, Please try again later or contact us via support@obrisk.com"}),console.log(e)})},addFile:function(e){var s,t=$('<li id="'+e.id+'"><p class="title">'+e.name+'</p><p class="imgWrap"></p><p class="upload-state"><span></span></p><span class="success-span"></span></li>'),r=($('<div class="file-panel"><span class="cancel">cancel</span></div>').appendTo(t),t.find("p.upload-state span"),t.find("p.imgWrap"));$('<p class="error"></p>');if(/^image\//.test(e.type)){var a=document.createElement("img");a.classList.add("obj"),a.file=e,a.style.width="100%",a.style.height="100%",r.empty().append($(a));var i=new FileReader;i.onload=(s=a,function(e){s.src=e.target.result}),i.readAsDataURL(e)}else{var o=new FileReader;o.onload=function(){var s=new Blob([o.result],{type:e.type}),t=URL.createObjectURL(s),a=document.createElement("video"),i=function(){l()&&(a.removeEventListener("timeupdate",i),a.pause())};a.addEventListener("loadeddata",(function(){l()&&a.removeEventListener("timeupdate",i)}));var l=function(){var e=document.createElement("canvas");e.width=a.videoWidth,e.height=a.videoHeight,e.getContext("2d").drawImage(a,0,0,e.width,e.height);var s=e.toDataURL(),i=s.length>1e5;if(i){var o=document.createElement("img");o.src=s,r.empty().append($(o)),URL.revokeObjectURL(t)}return i};a.addEventListener("timeupdate",i),a.preload="metadata",a.src=t,a.muted=!0,a.playsInline=!0,a.play()},o.readAsArrayBuffer(e)}t.appendTo($queue)}};var progressBar=0,progress="",$wrap=$("#uploader"),$queue=$('<ul class="filelist"></ul>').appendTo($wrap.find(".queueList")),$totalProgressbar=$("#totalProgressBar"),applyTokenDo=(progress=function(e){return function(e){$totalProgressbar.css("width",progressBar),e()}},function(){var e=oss_url;return new Promise((s,t)=>{$.ajax({url:e,success:function(e){s(e)},error:function(e){t(e)}})})}),getPresignedURL=function(){return new Promise((e,s)=>{$.ajax({url:"/get-oss-auth/stories.video/",success:function(s){e(s)},error:function(e){s(e)}})})};function OssUpload(){var e=this;e.init=function(){e.initPage(),e.bindEvent()},e.initPage=function(){}}function genKey(e){var s="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,(function(e){var s=16*Math.random()|0;return("x"==e?s:3&s|8).toString(16)}))+"."+e.split("/")[1],t=(new Date).toISOString().split("T")[0];if("stories"==app)return/^video/.test(e)?"media/videos/"+app+"/"+slugify(user)+"/"+t+"/"+s:"media/images/"+app+"/"+slugify(user)+"/"+t+"/"+s;if("classifieds"==app){const e=document.getElementById("id_title").value;return"undefined"===e?"media/images/"+app+"/"+slugify(user)+"/item-no-title/"+t+"/"+s:"media/images/"+app+"/"+slugify(user)+"/"+slugify(e)+"/"+t+"/"+s}return"articles"==app?"media/images/"+app+"/"+slugify(user)+"/"+t+"/"+s:void 0}$((function(){(ossUpload=new OssUpload).init(),$("body").on("resetUpload",(function(){uploader={fileList:[],fileStats:{totalFilesNum:0,totalFilesSize:0,uploadFinishedFilesNum:0,curFileSize:0}},$(".queueList ul").html(""),img_error="",images="",$totalProgressbar.css("width","0%").html(""),hasErrors=!1,$("#addVideo").show(),$("#addBtn").show()})),$("#retry-button").click((function(e){e.preventDefault(),$("body").trigger("resetUpload"),$("#retry-button").addClass("is-hidden"),$("#addBtn").show()}))}));