function printError(e,r){template=`\n        <div class="alert alert-danger alert-dismissible fade show" role="alert">\n          ${e}\n          <button type="button" class="close" data-dismiss="alert" aria-label="Close">\n            <span aria-hidden="true">&times;</span>\n          </button>\n        </div>\n        `,$(""+r).prepend(template)}$((function(){$("body").on("uploadComplete",(function(e){$("input[name='status']").val("A"),$("#id_images").val(images),$("#id_img_error").val(img_error),$.ajax({url:"/classifieds/write-new-classified/",data:$("form").serialize(),type:"POST",cache:!1,success:function(e){"200"==e.status?window.location.replace("/classifieds/"):(console.log(e),$(".alert-error").removeClass("d-none"),$("#data-errors").html(e.error_message),window.scrollTo({top:0,behavior:"smooth"}))},error:function(e){void 0!==e.error_message?printError(e.error_message,"#classified-form"):printError("Sorry we can't process your request, please try again later","#classified-form")}})})),$("#addBtn").click((function(){$("#uploader").show()})),$(".submit-button").click((function(e){void 0!==$("#id_phone_number").val()&&0==$("#id_phone_number").val().startsWith("+86")&&(11==$("#id_phone_number").val().length?$("#id_phone_number").val("+86"+$("#id_phone_number").val()):printError("Your phone number is incorrect, Please verify","#classified-form")),uploader.fileStats.totalFilesNum>0?""!=images&&$("#id_images").val()==images?$("body").trigger("uploadComplete"):$("body").trigger("submitClicked"):printError("Please provide all the details and upload at least 1 image","#classified-form")}))}));