function printError(e,r){template=`\n        <div class="notification is-danger" role="alert">\n            <button type="button" class="delete close-dj-messages"></button>\n          ${e}\n        </div>\n        `,$(""+r).prepend(template)}$((function(){$("body").on("uploadComplete",(function(e){$("input[name='status']").val("A"),$("#id_images").val(images),$("#id_img_error").val(img_error),$.ajax({url:"/classifieds/write-new-classified/",data:$("form").serialize(),type:"POST",cache:!1,success:function(e){"200"==e.status?window.location.replace("/classifieds/"):(console.log(e),printError(e.error_message,"#classified-form"),window.scrollTo({top:0,behavior:"smooth"}))},error:function(e){void 0!==e.error_message?printError(e.error_message,"#classified-form"):printError("Sorry we can't process your request, please try again later","#classified-form")}})})),$("#addBtn").click((function(){$("#uploader").show()})),$(".submit-button").click((function(e){const r=$("#id_phone_number").val();void 0!==r&&""!=r&&0==r.val().startsWith("+86")&&(11==r.val().length?r.val("+86"+r.val()):printError("Your phone number is incorrect, Please verify","#classified-form")),uploader.fileStats.totalFilesNum>0?""!=images&&$("#id_images").val()==images?$("body").trigger("uploadComplete"):$("body").trigger("submitClicked"):printError("Please provide all the details and upload at least 1 image","#classified-form")}))}));