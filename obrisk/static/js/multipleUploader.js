$(function() {
  function getCookie(name) {
    // Function to get any cookie available in the session.
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  // This sets up every ajax call with proper headers.
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

});

//localStorage.debug = 'ali-oss';
/**
 * fileStats: File statistics
 * filename: The address of the uploaded file
 * * */
var uploader = {
  fileList: [],
  fileStats: {
    totalFilesNum: 0,
    totalFilesSize: 0,
    uploadFinishedFilesNum: 0,
    curFileSize: 0
  }
};

//Upload instance object
var Buffer = OSS.Buffer;
var STS = OSS.STS;
var FileMaxSize = 13000000;
var TotalFilesMaxSize = 8;
var images = "";
var img_error; //Records the errors happened during upload.
var client;
var imgClient; //If we'll  be checking the file size.
var ossUpload = "";
var obrisk_oss_url = "https://obrisk.oss-cn-hangzhou.aliyuncs.com/";

var retryCount = 0;
const retryCountMax = 5;

OssUpload.prototype = {
  constructor: OssUpload,
  // Binding event
  bindEvent: function() {
    var _this = this;

    $("#chooseFile, #addBtn").click(function() {
      document.getElementById("image-file").click();
    });

    $('input[type="file"]').change(function(e) {
      $("#wrapper .container").css("display", "block");
      $(".submit-button").removeClass("is-disabled");
      //console.log(e)
      var files = e.target.files;
      var curIndex = uploader.fileList.length; //The length of the file already in the plugin, append
      var NumberOfSelectedFiles = files.length;
      //console.log('total files selected ' + NumberOfSelectedFiles);
      var file = null;
      $("#uploader .placeholder").hide();

      var AllowUploadQuantity = TotalFilesMaxSize - curIndex;
      //console.log('number of files ' + AllowUploadQuantity)

      //check if the upload quantity has reach max
      if (AllowUploadQuantity == 0) {
        bootbox.alert("Only " + TotalFilesMaxSize + " images are allowed");
        $(".addBtn").hide();
      } else if (files.length == 0) {
        bootbox.alert("No image selected , Please select one or more images");
      } else {
        //Add only the allow # of files to upload qeue
        if (
          NumberOfSelectedFiles <= AllowUploadQuantity &&
          NumberOfSelectedFiles > 0
        ) {
          for (var i = 0; i < NumberOfSelectedFiles; i++) {
            file = files[i];
            //don't upload files with size greater than 13MB
            if (file.size <= FileMaxSize) {
              uploader.fileList[curIndex + i] = file;
              file.id = uploader.fileList[curIndex + i].id =
                "image" + (curIndex + i + 1); //Add id to each file
              uploader.fileStats.totalFilesSize += file.size; //Statistical file size
              _this.addFile(file); //Add to control view
            } else {
              bootbox.alert(
                file.name +
                  " is larger than 13MB, please select images small than 13MB "
              );
            }
          }
        } else {
          for (
            var i = 0;
            i < NumberOfSelectedFiles &&
            uploader.fileList.length < TotalFilesMaxSize;
            i++
          ) {
            file = files[i];
            //don't upload files with size greater than 13MB
            if (file.size <= FileMaxSize) {
              uploader.fileList[curIndex + i] = file;
              file.id = uploader.fileList[curIndex + i].id =
                "image" + (curIndex + i + 1); //Add id to each file
              uploader.fileStats.totalFilesSize += file.size; //Statistical file size
              _this.addFile(file); //Add to control view
            } else {
              bootbox.alert(
                file.name +
                  " is larger than 13MB, please select images small than 13MB "
              );
            }
          }
          bootbox.alert("Only " + TotalFilesMaxSize + " images are allowed");
          $(".addBtn").hide();
        }
      }
      uploader.fileStats.totalFilesNum = uploader.fileList.length;
    });

    $(".submit-button").click(function(event) {
      if (uploader.fileStats.totalFilesNum > 0) {
        $("#statusBar").css("display", "flex");
        var length = uploader.fileStats.totalFilesNum;
        var file;
        $(".start-uploader").css("display", "none");
        $totalProgressbar
          .css("width", "40%")
          .html("Upload Started please wait...");
        for (var i = 0; i < length; i++) {
          var filename = genKey();
          file = uploader.fileList[i];
          _this.uploadFile(file, filename);
        }
      }
    });
    $(".queueList .filelist").delegate("li span.cancel", "click", function() {
      var $this = $(this);
      var $li = $this.parent().parent();
      var id = $li.attr("id");
      var list = uploader.fileList;
      var len = list.length;
      for (var i = 0; i < len; i++) {
        if (uploader.fileList[i].id == id) {
          uploader.fileStats.totalFilesSize -= uploader.fileList[i].size; //Statistical file size
          uploader.fileList.splice(i, 1); //Delete a file from the file list
          uploader.fileStats.totalFilesNum = uploader.fileList.length;
          break;
        }
      }

      $li.remove();
      if (uploader.fileList.length == 0) {
        $("#wrapper .container").css("display", "none");
      }
    });
  },

  /***
   *  upload files
   * @param file files to be uploaded
   * @param filename to which location to upload the file. According to the official statement is the key
   * oss is object storage, there is no path path concept, but personally think this can be better understood as a path
   */
  uploadFile: function(file, filename) {
    $totalProgressbar.css("width", "30%").html("Uploading...");
    applyTokenDo()
      .then(result => {
        if (!result.direct) {
          client = new OSS({
            region: result.region,
            accessKeyId: result.accessKeyId,
            accessKeySecret: result.accessKeySecret,
            stsToken: result.SecurityToken,
            bucket: result.bucket
          });
        } else {
          client = new OSS({
            region: result.region,
            accessKeyId: result.accessId,
            accessKeySecret: result.stsTokenKey,
            bucket: result.bucket
          });
        }

        //make sure we get the sts token
        if (client !== undefined) {
          const upload = async () => {
            try {
              const results = await client
                .multipartUpload(filename, file, {
                  progress: progress,
                  partSize: 200 * 1024, //Minimum is 100*1024
                  timeout: 120000 // 2 minutes timeout
                })
                .then(function(res) {
                  //Try to get the dominat color from the uploaded image, if it fails it means the image
                  //was corrupted during upload
                  $.ajax({
                    url:
                      obrisk_oss_url +
                      res.name +
                      "?x-oss-process=image/average-hue",
                    success: function() {
                      $("#" + file.id)
                        .children(".success-span")
                        .addClass("success");
                      $("#" + file.id)
                        .children(".file-panel")
                        .hide();
                      uploader.fileStats.uploadFinishedFilesNum++; //Successfully uploaded + 1
                      uploader.fileStats.curFileSize += file.size; //Currently uploaded file size
                      progressBarNum =
                        (
                          uploader.fileStats.curFileSize /
                          uploader.fileStats.totalFilesSize
                        ).toFixed(2) * 100;
                      progressBar = (
                          uploader.fileStats.curFileSize /
                          uploader.fileStats.totalFilesSize
                        ).toFixed(2) * 100 + "%";

                      if (images == '') {
                          images += res.name;
                      }else {
                          images += "," + res.name;
                      }
                      if (progressBarNum == 100) {
                        $totalProgressbar
                          .css("width", progressBar)
                          .html("Upload complete");

                          $("body").trigger("uploadComplete");
                       
                      } else {
                        $totalProgressbar
                          .css("width", progressBar)
                          .html(progressBar);
                      }
                    },
                    error: function(e) {
                      // if a file is corrupted during upload retry 5 times to upload it then skip it and return an error message
                      if (retryCount < retryCountMax) {
                        retryCount++;
                        console.error(`retryCount : ${retryCount}`);
                        upload();
                      } else {
                        //We have retried to the max and there is nothing we can do
                        //Allow the users to submit the form atleast with default image.

                        $("#" + file.id)
                          .children(".success-span")
                          .addClass("fail");
                        $("#" + file.id)
                          .children(".file-panel")
                          .hide();
                        uploader.fileStats.uploadFinishedFilesNum++; //Successfully uploaded + 1
                        uploader.fileStats.curFileSize += file.size; //Currently uploaded file size
                        progressBarNum =
                          (
                            uploader.fileStats.curFileSize /
                            uploader.fileStats.totalFilesSize
                          ).toFixed(2) * 100;
                        progressBar =
                          (
                            uploader.fileStats.curFileSize /
                            uploader.fileStats.totalFilesSize
                          ).toFixed(2) *
                            100 +
                          "%";

                        if (progressBarNum == 100) {
                          $totalProgressbar
                            .css("width", progressBar)
                            .html("Upload complete");
                        } else {
                          $totalProgressbar
                            .css("width", progressBar)
                            .html(progressBar);
                        }
                        img_error =
                          res.name +
                          ", Message: " +
                          "Corrupted image" +
                          ", RequestID: " +
                          res.name;
                        $("#retry-button").removeClass("is-hidden");

                        if (!images) {
                          images = "classifieds/error-img.jpg";
                          bootbox.alert(
                            "Oops! an error occured when uploading your image(s). \
                                                But you can submit this post without images ."
                          );
                        }
                      }
                    }
                  }); //End of ajax function
                })
                .catch(err => {
                  console.error(err);
                  console.log(`err.name : ${err.name}`);
                  console.log(`err.message : ${err.message}`);
                  console.log(`err.request : ${err.requestId}`);

                  $totalProgressbar.css("width", "40%").html("Retrying...");

                  if (
                    err.name.toLowerCase().indexOf("connectiontimeout") !== -1
                  ) {
                    if (retryCount < retryCountMax) {
                      retryCount++;
                      console.error(`retryCount : ${retryCount}`);
                      upload();
                    } else {
                      //We have retried to the max and there is nothing we can do
                      //Allow the users to submit the form atleast with default image.
                      $totalProgressbar
                        .css("width", "94%")
                        .html("Completed with minor errors!");
                      $("ul.filelist li")
                        .children(".success-span")
                        .addClass("fail");
                      $("#addBtn").hide();
                      img_error =
                        err.name +
                        ", Message: " +
                        err.message +
                        ", RequestID: " +
                        err.requestId;
                      $("#retry-button").removeClass("is-hidden");
                      if (!images) {
                        images = "classifieds/error-img.jpg";
                        bootbox.alert(
                          "Oops! an error occured when uploading your image(s). \
                                            But you can submit this post without images ."
                        );
                      }
                    }
                  } else {
                    //Not timeout out error and there is nothing we can do
                    //Allow the users to submit the form atleast with default image.
                    $totalProgressbar
                      .css("width", "94%")
                      .html("Completed with minor errors!");
                    $("#addBtn").hide();
                    img_error =
                      err.name +
                      ", Message: " +
                      err.message +
                      ", RequestID: " +
                      err.requestId;
                    $("#retry-button").removeClass("is-hidden");
                    if (!images) {
                      images = "classifieds/error-img.jpg";
                      bootbox.alert(
                        "Oops! an error occured when uploading your image(s). \
                                            But you can submit this post without images ."
                      );
                    }
                  }
                });
              return results;
            } catch (e) {
              bootbox.alert(
                "Oops! an error occured when uploading your image(s), \
                    Please try again later or contact us via support@obrisk.com. " +
                  e
              );
              $(".start-uploader").css("display", "block");
              console.log(e);
            }
          };
          return upload();
        } else {
          bootbox.alert(
            "Oops!, it looks like there is a network problem, \
            Please try again later or contact us at support@obrisk.com"
          );
          $(".start-uploader").css("display", "block");
        }
      })
      .catch(e => {
        bootbox.alert(
          "Oops! an error occured before upload started, Please try again later or contact us via support@obrisk.com" +
            e
        );
        console.log(e);
      });
  },

  /**
   * Add file to preview
   */
  addFile: function(file) {
    var $li = $(
        '<li id="' +
          file.id +
          '">' +
          '<p class="title">' +
          file.name +
          "</p>" +
          '<p class="imgWrap"></p>' +
          '<p class="upload-state"><span></span></p><span class="success-span"></span>' +
          "</li>"
      ),
      $btns = $(
        '<div class="file-panel">' +
          '<span class="cancel">cancel</span>' +
          "</div>"
      ).appendTo($li),
      $prgress = $li.find("p.upload-state span"),
      $wrap = $li.find("p.imgWrap"),
      $info = $('<p class="error"></p>');
    var imageType = /^image\//;
    if (imageType.test(file.type)) {
      var img = document.createElement("img");
      img.classList.add("obj");
      img.file = file;
      img.style.width = "100%";
      img.style.height = "100%";
      $wrap.empty().append($(img));
      var reader = new FileReader();
      reader.onload = (function(aImg) {
        return function(e) {
          aImg.src = e.target.result;
        };
      })(img);
      reader.readAsDataURL(file);
    }
    $li.appendTo($queue);
  }
};

/**
 * Create progress bar
 */
var progressBar = 0;
var progress = "";
var $wrap = $("#uploader"),
  // Picture container
  $queue = $('<ul class="filelist"></ul>').appendTo($wrap.find(".queueList")),
  $totalProgressbar = $("#totalProgressBar");

var progress = function(p) {
  //console.log(p)    
  return function(done) {
    $totalProgressbar.css("width", progressBar);
    done();
  };
};

/**
 * get sts token
 *
 * TODO neeeds improvment to make ajax call ony when token has expired
 */
var applyTokenDo = function() {
  var url = oss_url; //Request background to obtain authorization address url
  return new Promise((resolve, reject) => {
    $.ajax({
      url: url,
      success: function(result) {
        resolve(result);
      },
      error: function(e) {
        reject(e);
      }
    });
  });
};

//File upload initializer
function OssUpload() {
  var _this = this;
  _this.init = function() {
    _this.initPage();
    _this.bindEvent();
  };
  _this.initPage = function() {};
}

/**
 * generate file name using uuid
 *
 * @return  {string}
 */


function genKey() {
  if (app == 'stories') { 
  
    if ($("#publish").val().substring(0, 20).length != 0){
        return (
        app +"/"+ user +"/" +slugify($("#publish").val().substring(0, 20)) +"/" +"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
            var r = (Math.random() * 16) | 0,v = c == "x" ? r : (r & 0x3) | 0x8;return v.toString(16);})
        );
    } else {
        return (
        "stories/" +
        user +
        "/" +
        "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
            var r = (Math.random() * 16) | 0,
            v = c == "x" ? r : (r & 0x3) | 0x8;
            return v.toString(16);
        }) +
        "/" +
        "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
            var r = (Math.random() * 16) | 0,
            v = c == "x" ? r : (r & 0x3) | 0x8;
            return v.toString(16);
        })
        );
    }
  }else if ( app == "classifieds" ){
    return "classifieds/" + user + '/' + slugify($('#id_title').val()) +
    '/' + 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
  } else {
      return "junk/"+ '/' + 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
  }

}

/**
 * create a slug
 *
 * @param   {string}  string  string to be slugified
 *
 * @return  {slug}          slugified string
 */
function slugify(string) {
  const a = "àáäâãåăæçèéëêǵḧìíïîḿńǹñòóöôœøṕŕßśșțùúüûǘẃẍÿź·/_,:;";
  const b = "aaaaaaaaceeeeghiiiimnnnooooooprssstuuuuuwxyz------";
  const p = new RegExp(a.split("").join("|"), "g");
  return string
    .toString()
    .toLowerCase()
    .replace(/\s+/g, "-") // Replace spaces with -
    .replace(p, c => b.charAt(a.indexOf(c))) // Replace special characters
    .replace(/&/g, "-and-") // Replace & with ‘and’
    .replace(/[^\w\-]+/g, "") // Remove all non-word characters
    .replace(/\-\-+/g, "-") // Replace multiple - with single -
    .replace(/^-+/, "") // Trim - from start of text
    .replace(/-+$/, ""); // Trim - from end of text
}

$(function() {
  //create and initialize upload object
  ossUpload = new OssUpload();
  ossUpload.init();

  $("#retry-button").click(function(e) {
    e.preventDefault();
    $("#addBtn").show();
    uploader = {
      fileList: [],
      fileStats: {
        totalFilesNum: 0,
        totalFilesSize: 0,
        uploadFinishedFilesNum: 0,
        curFileSize: 0
      }
    };

    $(".queueList ul").html(``);
    img_error = "";
    images = "";
    var progressBar = 0;
    var progress = "";
    var $wrap = $("#uploader ");
    $totalProgressbar.css("width", "0%").html("");
    $("#retry-button").addClass("is-hidden");
  });
});