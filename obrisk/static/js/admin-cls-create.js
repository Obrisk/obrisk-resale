const adminUrl="/classifieds/wsguatpotlfwccdi/admin-write-new-classified/";function printError(e){document.getElementsByClassName("notification")[0].classList.remove("is-hidden"),document.getElementById("notf-msg").innerHTML=e,window.scroll({top:0,left:0,behavior:"smooth"})}document.addEventListener("DOMContentLoaded",(function(){if(getCookie("classified")){const e=getCookie("classified");document.getElementById("id_title").value=e[0],document.getElementById("id_details").value=e[1],document.getElementById("id_price").value=e[2]}document.querySelectorAll(".close-dj-messages").forEach(e=>{e.addEventListener("click",e=>{e.currentTarget.parentElement.classList.add("is-hidden"),e.stopPropagation()})});const e=JSON.parse(localStorage.getItem("new-classified"));e&&(document.getElementById("id_title").value=e.title,document.getElementById("id_details").value=e.details,document.getElementById("id_price").value=e.price),$("body").on("uploadComplete",(function(e){$("input[name='status']").val("A"),$("#id_images").val(images),$("#id_img_error").val(img_error),$.ajax({url:adminUrl,data:$("form").serialize(),type:"POST",cache:!1,success:function(e){"200"==e.status?window.location.replace(adminUrl):(console.log(e),printError(e.error_message),window.scrollTo({top:0,behavior:"smooth"}))},error:function(e){void 0!==e.error_message?printError(e.error_message):printError("Sorry we can't process your request, please try again later")}})})),document.querySelector("#addBtn").addEventListener("click",(function(){$("#uploader").show()})),document.querySelector("#chooseFile").addEventListener("click",(function(){if(null==currentUser){let e=Object.fromEntries(new FormData(document.querySelector("form")));localStorage.setItem("new-classified",JSON.stringify(e)),window.location.replace("/auth/login/?next=/classifieds/write-new-classified/")}})),document.getElementById("create-btn").addEventListener("click",(function(e){if(uploader.fileStats.totalFilesNum<1||document.getElementById("id_title").value.length<2)printError("Please provide the title & at least 1 image");else if(""!=images&&$("#id_images").val()==images)$("body").trigger("uploadComplete");else{try{const e=document.getElementById("id_phone_number");null!==e&&""!==e.value&&0==e.value.startsWith("+86")&&(11===e.value.length?e.value="+86"+e.value:printError("The phone number is incorrect, Please verify"))}catch(e){console.error(e)}localStorage.removeItem("new-classified"),$("body").trigger("submitClicked")}})),document.getElementById("cancel-classified").addEventListener("click",(function(){localStorage.removeItem("new-classified")}))}));