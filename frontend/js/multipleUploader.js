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
const Buffer = OSS.Buffer;
const STS = OSS.STS;
const obrisk_oss_url = "https://obrisk.oss-cn-hangzhou.aliyuncs.com/";
const MaxImageSize = 30000000; //30MB
const MaxVideoSize = 200000000; //200MB
const s3Upload = false;
const aliyunUpload = true;

var images = "";
var videos = "";
var img_error; //Records the errors happened during upload.
var client;
var imgClient; //If we'll  be checking the file size.
var ossUpload = "";
var files = ""; 
//The length of the file already in the plugin, append
var curIndex = 0;
var NumberOfSelectedFiles = 0;
var hasErrors = false;
var retryCount = 0;
var retryCountMax = 5;
var TotalFilesMaxSize = 10;


OssUpload.prototype = {
  constructor: OssUpload,
  // Binding event
  bindEvent: function() {
    var _this = this;

    $("#chooseFile, #addBtn").click(function() {
      document.getElementById("image-file").click();
    });
    $("#addVideo").click(function() {
      document.getElementById("video-file").click();
    });

    $("#image-file").change(function(e) {
          $("#wrapper .container").css("display", "block");
          $(".submit-button").removeClass("is-disabled");
          files = e.target.files;
          //The length of the file already in the plugin, append
          curIndex = uploader.fileList.length;
          NumberOfSelectedFiles = files.length;
          var file = null;
          $("#uploader .placeholder").hide();

          var AllowUploadQuantity = TotalFilesMaxSize - curIndex;

          //check if the upload quantity has reach max
          if (AllowUploadQuantity === 0) {
                $.wnoty({
                  type: "error",
                  autohide: false,
                  message: "Only " + TotalFilesMaxSize + " images are allowed"
                });
                $("#addBtn").hide();
          } else if (files.length === 0) {
                $.wnoty({
                  type: "error",
                  autohide: false,
                  message: "No image selected , Please select one or more images"
                });
          } else {
             //Add only the allow # of files to upload qeue
             if (
                  NumberOfSelectedFiles <= AllowUploadQuantity &&
                  NumberOfSelectedFiles > 0
              ) {
                  for (var i = 0; i < NumberOfSelectedFiles; i++) {
                    file = files[i];
                    //don't upload files with size greater than 13MB
                    if (file.size <= MaxImageSize) {
                      uploader.fileList[curIndex + i] = file;
                      file.id = uploader.fileList[curIndex + i].id =
                        "image" + (curIndex + i + 1); //Add id to each file
                      uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                      _this.addFile(file); //Add to control view
                      $("#addVideo").hide();
                    } else {
                      $.wnoty({
                        type: "error",
                        autohide: false,
                        message:
                          file.name +
                          " is larger than 13MB, please select images small than 13MB "
                      });
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
                    if (file.size <= MaxImageSize) {
                      uploader.fileList[curIndex + i] = file;
                      file.id = uploader.fileList[curIndex + i].id =
                        "image" + (curIndex + i + 1); //Add id to each file
                      uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                      _this.addFile(file); //Add to control view
                      $("#addVideo").hide();
                    } else {
                      $.wnoty({
                        type: "error",
                        autohide: false,
                        message:
                          file.name +
                          " is larger than 13MB, please select images small than 13MB "
                      });
                    }
                  }
                  $.wnoty({
                    type: "error",
                    autohide: false,
                    message: "Only " + TotalFilesMaxSize + " images are allowed"
                  });
                }
          }
          uploader.fileStats.totalFilesNum = uploader.fileList.length;
    });

    $("#video-file").change(function(e) {
          $("#wrapper .container").css("display", "block");
          $(".submit-button").removeClass("is-disabled");
          //console.log(e)
          files = e.target.files;
          curIndex = uploader.fileList.length; //The length of the file already in the plugin, append
          NumberOfSelectedFiles = files.length;
          var file = null;
          $("#uploader .placeholder").hide();

          var AllowUploadQuantity = 1 - curIndex;

          //check if the upload quantity has reach max
          if (AllowUploadQuantity == 0) {
            $.wnoty({
              type: "error",
              autohide: false,
              message: "Only " + 1 + " video is allowed"
            });
            $("#addVideo").hide();
          } else if (files.length == 0) {
            $.wnoty({
              type: "error",
              autohide: false,
              message: "No video selected, Please select one or more videos"
            });
          } else {
            //Add only the allow # of files to upload qeue
            if (
              NumberOfSelectedFiles <= AllowUploadQuantity &&
              NumberOfSelectedFiles > 0
            ) {
              for (var i = 0; i < NumberOfSelectedFiles; i++) {
                file = files[i];
                //don't upload files with size greater than 13MB
                if (file.size <= MaxVideoSize) {
                  uploader.fileList[curIndex + i] = file;
                  file.id = uploader.fileList[curIndex + i].id =
                    "video" + (curIndex + i + 1); //Add id to each file
                  uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                  _this.addFile(file); //Add to control view
                  $("#addBtn").hide();
                } else {
                  $.wnoty({
                    type: "error",
                    autohide: false,
                    message:
                      file.name +
                      " is larger than 13MB, please select videos small than 13MB "
                  });
                }
              }
            } else {
              for (
                var i = 0;
                i < NumberOfSelectedFiles && uploader.fileList.length < 1;
                i++
              ) {
                file = files[i];
                //don't upload files with size greater than 13MB
                if (file.size <= MaxVideoSize) {
                  uploader.fileList[curIndex + i] = file;
                  file.id = uploader.fileList[curIndex + i].id =
                    "video" + (curIndex + i + 1); //Add id to each file
                  uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                  _this.addFile(file); //Add to control view
                  $("#addBtn").hide();
                } else {
                  $.wnoty({
                    type: "error",
                    autohide: false,
                    message:
                      file.name +
                      " is larger than 13MB, please select videos small than 13MB "
                  });
                }
              }
              $.wnoty({
                type: "error",
                autohide: false,
                message: "Only " + 1 + " video is allowed"
              });
            }
          }
          uploader.fileStats.totalFilesNum = uploader.fileList.length;
    });

    $("body").on("submitClicked", function() {
          $("#statusBar").css("display", "flex");
          var length = uploader.fileStats.totalFilesNum;
          var file;
          $(".start-uploader").css("display", "none");
          $totalProgressbar
            .css("width", "40%")
            .html("Upload Started please wait...");
          for (var i = 0; i < length; i++) {
            file = uploader.fileList[i];
            var filename = genKey(file.type);
            _this.uploadFile(file, filename, file.type);
          }
    });

    $(".queueList .filelist").delegate("li span.cancel", "click", function() {
          var $this = $(this);
          var $li = $this.parent().parent();
          var id = $li.attr("id");
          var list = uploader.fileList;
          var len = list.length;
          for (var i = 0; i < len; i++) {
            if (len <= 0) {
              $("#addBtn").show();
              $("#addVideo").hide();
            }
            if (uploader.fileList[i].id == id) {
              uploader.fileStats.totalFilesSize -= uploader.fileList[i].size; //Statistical file size
              uploader.fileList.splice(i, 1); //Delete a file from the file list
              uploader.fileStats.totalFilesNum = uploader.fileList.length;
              break;
            }
          }

          $li.remove();
          if (uploader.fileList.length == 0) {
            $("#wrapper .placeholder").css("display", "block");
            $("#addBtn").show();
            $("#addVideo").show();
          }
    });

  },

  /***
   *  upload files
   * @param file files to be uploaded
   * @param filename to which location to upload the file. According to the official statement is the key
   * oss is object storage, there is no path path concept, but personally think this can be better understood as a path
   */
  uploadFile: function(file, filename, type) {
    $totalProgressbar.css("width", "30%").html("Uploading...");
    if (aliyunUpload) {
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
                    //Here need to add the code to check if the image upload succeeeded.
                    //There has to be a fetch to get the meta of the images from Aliyun
                    if (/^video/.test(type)) {
                      url = obrisk_oss_url + res.name;
                    } 

                        $("#" + file.id).children(".success-span").addClass("success");
                        $("#" + file.id).children(".file-panel").hide();
                        uploader.fileStats.uploadFinishedFilesNum++; //Successfully uploaded + 1
                        uploader.fileStats.curFileSize += file.size; //Currently uploaded file size
                        progressBarNum = (
                            uploader.fileStats.curFileSize /
                            uploader.fileStats.totalFilesSize
                        ).toFixed(2) * 100;

                        progressBar = (
                            uploader.fileStats.curFileSize /
                            uploader.fileStats.totalFilesSize
                          ).toFixed(2) * 100 + "%";

                        if (/^image/.test(type)) {
                          if (images == "") {
                            images += res.name;
                          } else {
                            images += "," + res.name;
                          }
                        } else {
                          if (videos == "") {
                            videos += res.name;
                          } else {
                            videos += "," + res.name;
                          }
                        }

                        if (progressBarNum == 100) {
                          $totalProgressbar.css("width", progressBar).html("Upload complete");
                          $("body").trigger("uploadComplete");
                        } else {
                          progressBar = parseFloat(progressBar);

                          $totalProgressbar
                            .css("width", progressBar.toFixed(0))
                            .html(progressBar);
                        }

                  }).catch(err => {
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
                        $totalProgressbar.css("width", "94%")
                          .html("Completed with minor errors!");

                        $("ul.filelist li").children(".success-span").addClass("fail");
                        $("#addBtn").hide();

                        img_error = err.name + ", Message: " + err.message +
                          ", RequestID: " + err.requestId;
                        $("#retry-button").removeClass("is-hidden");

                        if (!images) {
                          if (app == "classifieds") {
                            images = "classifieds/error-img.jpg";
                          } else {
                            //don't add error images to stories
                          }

                          $.wnoty({
                            type: "error",
                            autohide: false,
                            message:
                              "Oops! an error occured on image(s). \
                                But you can submit the post without images ."
                          });
                        }
                      }
                    } else {
                      //Not timeout out error and there is nothing we can do
                      //Allow the users to submit the form atleast with default image.
                      $totalProgressbar
                        .css("width", "94%")
                        .html("Completed with minor errors!");
                      img_error =
                        err.name +
                        ", Message: " +
                        err.message +
                        ", RequestID: " +
                        err.requestId;
                      $("#retry-button").removeClass("is-hidden");
                      if (!images) {
                        if (app == "classifieds") {
                          images = "classifieds/error-img.jpg";
                        } else {
                          //Don't add error message for stories
                        }
                        console.log(hasErrors);
                        if (!hasErrors) {
                          $.wnoty({
                            type: "error",
                            autohide: false,
                            message: "Oops! an error occured on image(s). \
                                            But you can submit the post without images ."
                          });
                          hasErrors = true;
                        }
                      }
                    }
                  });
                return results;
              } catch (e) {
                $.wnoty({
                  type: "error",
                  autohide: false,
                  message:
                    "Oops! an error occured when uploading your image(s), \
                    Please try again or contact us via WechatID: Obrisk. "
                });
                $(".start-uploader").css("display", "block");
                console.log(e);
              }
            };
            return upload();
          } else {
            $.wnoty({
              type: "error",
              autohide: false,
              message:
                "Oops!, it looks like there is a network problem, \
                try again later or contact us via wechatID: Obrisk"
            });
            $(".start-uploader").css("display", "block");
          }
        })
        .catch(e => {
          $.wnoty({
            type: "error",
            autohide: false,
            message:
              "Oops! an error occured. Try again later or contact us via wechatID: Obrisk"
          });
          console.log(e);
        });
    }
    if (s3Upload) {
      getPresignedURL().then(result => {
        const s3 = new AWS.S3({
          credentials: new AWS.Credentials({
            accessKeyId: result.AccessKeyId,
            secretAccessKey: result.SecretAccessKey
          }),
          region: "cn-northwest-1"
        });
        const params = {
          Bucket: "obdev-ac-media-s3",
          ContentType: file.type,
          Expires: 60 * 10,
          Key: genKey(type)
        };
        const upload = async () => {
          try {
            s3.getSignedUrl("putObject", params, function(err, presignedURL) {
              if (err) {
                console.error("Presigning encountered an error", err);
                showError();
              } else {
                $.ajax({
                  type: "PUT",
                  url: presignedURL,
                  contentType: file.type,
                  processData: false,
                  data: file,
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
                    progressBar =
                      (
                        uploader.fileStats.curFileSize /
                        uploader.fileStats.totalFilesSize
                      ).toFixed(2) *
                        100 +
                      "%";

                    if (/^image/.test(type)) {
                      if (images == "") {
                        images += res.name;
                      } else {
                        images += "," + res.name;
                      }
                    } else {
                      if (videos == "") {
                        videos += res.name;
                      } else {
                        videos += "," + res.name;
                      }
                    }

                    if (progressBarNum == 100) {
                      $totalProgressbar
                        .css("width", progressBar)
                        .html("Upload complete");

                      $("body").trigger("uploadComplete");
                    } else {
                      progressBar = parseFloat(progressBar);

                      $totalProgressbar
                        .css("width", progressBar.toFixed(0))
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
                        if (app == "classifieds") {
                          images = "classifieds/error-img.jpg";
                          $.wnoty({
                            type: "error",
                            autohide: false,
                            message:
                              "Oops! an error occured. You can submit this post without images"
                          });
                        } else {
                          $.wnoty({
                            type: "error",
                            autohide: false,
                            message:
                              "Sorry! Images error occured. You can post without images"
                          });
                        }
                      }
                    }
                  }
                });
              }
            });
          } catch (error) {
            $.wnoty({
              type: "error",
              autohide: false,
              message:
                "Oops! an error occured. Try again later or contact us via support@obrisk.com"
            });
            console.log(e);
          }
        };
        return upload();
      });
    }
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
    } else {
      var fileReader = new FileReader();
      fileReader.onload = function() {
        var blob = new Blob([fileReader.result], { type: file.type });
        var url = URL.createObjectURL(blob);
        var video = document.createElement("video");
        var timeupdate = function() {
          if (snapImage()) {
            video.removeEventListener("timeupdate", timeupdate);
            video.pause();
          }
        };
        video.addEventListener("loadeddata", function() {
          if (snapImage()) {
            video.removeEventListener("timeupdate", timeupdate);
          }
        });
        var snapImage = function() {
          var canvas = document.createElement("canvas");
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          canvas
            .getContext("2d")
            .drawImage(video, 0, 0, canvas.width, canvas.height);
          var image = canvas.toDataURL();
          var success = image.length > 100000;
          if (success) {
            var img = document.createElement("img");
            img.src = image;
            $wrap.empty().append($(img));
            URL.revokeObjectURL(url);
          }
          return success;
        };
        video.addEventListener("timeupdate", timeupdate);
        video.preload = "metadata";
        video.src = url;
        // Load video in Safari / IE11
        video.muted = true;
        video.playsInline = true;
        video.play();
      };
      fileReader.readAsArrayBuffer(file);
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
      success: function(response) {
        resolve(response);
      },
      error: function(e) {
        reject(e);
      }
    });
  });
};

var getPresignedURL = function() {
  var url = "/get-oss-auth/stories.video/"; //Request background to obtain authorization address url
  return new Promise((resolve, reject) => {
    $.ajax({
      url: url,
      success: function(response) {
        resolve(response);
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

function genKey(extension) {
  var filename =
    "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
      var r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    }) +
    "." +
    extension.split("/")[1];

  var date = new Date().toISOString().split("T")[0];

  if (app == "stories") {
        if (/^video/.test(extension)) {
          return (
            "media/videos" + "/" + app + "/" + slugify(user) + "/" + date + "/" + filename
          );
        } else {
          return (
            "media/images" + "/" + app + "/" + slugify(user) + "/" + date + "/" + filename
          );
        }

  } else if (app == "classifieds") {
        const title = document.getElementById('id_title').value;
        if (title === 'undefined') {
            return (
              "media/images" + "/" + app + "/" + slugify(user) + "/item-no-title/" + date + "/" + filename
            );
        }
        else {
            return (
              "media/images" + "/" + app + "/" + slugify(user) + "/" + slugify(title) + "/" + date + "/" + filename
            );
        }
  } else if (app == "articles") {
        return (
          "media/images" + "/" + app + "/" + slugify(user) + "/" + date + "/" + filename
        );
  }
}


// Upload file to a private S3 bucket, using a presigned URL
$(function() {
  //create and initialize upload object
  ossUpload = new OssUpload();
  ossUpload.init();

  //Remove all the selected files from the upload list
  $("body").on("resetUpload", function() {
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
    $totalProgressbar.css("width", "0%").html("");
    hasErrors = false;
    $("#addVideo").show();
    $("#addBtn").show();
  });
  //Reset Button
  $("#retry-button").click(function(e) {
    e.preventDefault();
    $("body").trigger("resetUpload");
    $("#retry-button").addClass("is-hidden");
    $("#addBtn").show();
  });
});
