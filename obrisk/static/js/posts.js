$(function() {


    $("#posts-form").submit(function (e) {
      e.preventDefault();
      $(this).unbind('submit').submit();
    });


  $("#post-submit").click(function(event) {
    
    event.preventDefault();
    $("input[name='status']").val("P");

    if ($("#id_title").val() == "") {
          event.preventDefault();
          $.wnoty({
            type: "error",
            autohide: false,
            message: "Please fill in all the required fields."
          });
    } else {
          $("#id_content_html").val(quill.root.innerHTML);
          $("[name=content_json]").val(JSON.stringify(quill.getContents()))
          $("#posts-form").submit();
    }
  });



  $(".update").click(function() {
    $("input[name='status']").val("P");
    //$("input[name='edited']").prop("checked");
    $("input[name='edited']").val("True");
    if ($("#id_title").val() == "") {
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please fill in all the required fields."
      });
    } else {
      $("#posts-form").submit();
    }
  });

  $(".draft").click(function() {
    $("input[name='status']").val("D");
    if ($("#id_title").val() == "") {
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please fill in all the required fields."
      });
    } else {
      $("#posts-form").submit();
    }
  });

  $("#chooseFile").click(function() {
    $("#uploader").show();
  });

  $("body").on("uploadComplete", function(event) {
    //Todo check if images where uploaded or empty
    var imgs = images.split(",");
    for (var img in imgs) {
      $("#imgs-list").append(
        "<p>" +
          " https://obrisk.oss-cn-hangzhou.aliyuncs.com/" +
          imgs[img] +
          "</p>"
      );
    }
  });

  $("#startImgUpload").click(function(event) {
    console.log("clicked");
    if (uploader.fileStats.totalFilesNum > 0) {
      $("body").trigger("submitClicked");
      console.log("submit trigged");
    } else {
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please upload at least one image for your post"
      });
    }
  });
});

// adding a crsf token
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$(document).ready(function() {
  $.fn.serializeToJSON = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
      if (o[this.name]) {
        if (!o[this.name].push) {
          o[this.name] = [o[this.name]];
        }
        o[this.name].push(this.value || "");
      } else {
        o[this.name] = this.value || "";
      }
    });
    return o;
  };
  $(function() {
    $(".comment-btn").click(function(event) {
      event.preventDefault();

      $.ajax({
        method: "POST",
        url: url,
        data: $("#commentForm").serialize(),
        processData: false,
        success: function(data) {
          $("#comment-notify").html(data);
          $("#commentForm")[0].reset();
          location.reload();
        },
        error: function(err) {
          console.log(err);
        }
      });
    });
  });
});

/**
 * Upload file object
 * fileStats: File statistics
 * filename: The address of the uploaded file
 * * */
var uploader = {
  file: "",
  totalFilesNum: 0,
  totalFilesSize: 0,
  uploadFinishedFilesNum: 0,
  curFileSize: 0
};

//Upload instance object
var Buffer = OSS.Buffer;
var STS = OSS.STS;
var FileMaxSize = 13000000;
var TotalFilesMaxSize = 1;
var image; //holds all uploaded images as a string
var client;
var ossUpload = "";

var uploadRetryCount = 0;
const uploadRetryCountMax = 5;
var obrisk_oss_url = "https://obrisk.oss-cn-hangzhou.aliyuncs.com/";

OssUpload.prototype = {
  constructor: OssUpload,
  // Binding event
  bindEvent: function() {
    var _this = this;

    $('input[type="file"]').change(function(e) {
      var file = e.target.files[0];
      //check if the upload quantity has reach max
      if (!file) {
        $.wnoty({
          type: "error",
          autohide: false,
          message: "No image selected , Please select one or more images"
        });
      } else {
        if (file.size <= 5000) {
          $.wnoty({
            type: "error",
            autohide: false,
            message:
              "The image you've chosen is too small. Please choose a file greater than 5KB but lower than 13MB!"
          });
        }
        //don't upload files with size greater than 13MB
        if (file.size <= FileMaxSize) {
          uploader.file = file;
          uploader.totalFilesSize = file.size;
          uploader.totalFilesNum = 1;
          var filename = genKey(file.type);
          $.wnoty({
            type: "info",
            message: "Uploading Cover Image please wait."
          });
          _this.uploadFile(file, filename);
        } else {
          $.wnoty({
            type: "error",
            autohide: false,
            message:
              "This image/file is larger than 13MB, please select images small than 13MB "
          });
        }
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
                  uploader.uploadFinishedFilesNum++;
                  uploader.curFileSize += file.size;

                  progressBarNum = (1).toFixed(2) * 100;
                  progressBar = (1).toFixed(2) * 100 + "%";

                  if (progressBarNum == 100) {
                    $.wnoty({
                      type: "success",
                      message: "Cover Image uploaded Successfully."
                    });
                    //Try to edit the uploaded image, if it fails it means the image
                    //was corrupted during upload
                    $.ajax({
                      url:
                        obrisk_oss_url +
                        res.name +
                        "?x-oss-process=image/average-hue",
                      success: function() {
                        $('[name="image"]').val(res.name);
                      },
                      error: function(e) {
                        // if a file is corrupted during upload retry 5 times to upload it then skip it and return an error message
                        if (uploadRetryCount < uploadRetryCountMax) {
                          uploadRetryCount++;
                          console.error(
                            `uploadRetryCount : ${uploadRetryCount}`
                          );
                          upload();
                        } else {
                          //We have retried to the max and there is nothing we can do
                          //Allow the users to submit the form atleast with default image.
                          $.wnoty({
                            type: "error",
                            autohide: false,
                            message:
                              "Oops! an error occured when uploading your image, please try again later!"
                          });
                        }
                      }
                    }); //End of outer ajax call
                  } //End of the if progress bar == 100
                })
                .catch(err => {
                  console.error(err);
                  console.log(`err.name : ${err.name}`);
                  console.log(`err.message : ${err.message}`);

                  if (
                    err.name.toLowerCase().indexOf("connectiontimeout") !== -1
                  ) {
                    // timeout retry
                    if (uploadRetryCount < uploadRetryCountMax) {
                      uploadRetryCount++;
                      console.error(`uploadRetryCount : ${uploadRetryCount}`);
                      upload();
                    } else {
                      //We have retried to the max and there is nothing we can do
                      //Allow the users to submit the form atleast with default image.
                      $totalProgressbar
                        .css("width", "100%")
                        .html("Upload failed!");
                    }
                  } else {
                    //Not timeout out error and there is nothing we can do
                    //Allow the users to submit the form atleast with default image.
                    $totalProgressbar
                      .css("width", "100%")
                      .html("Upload failed!");
                  }
                });
              return results;
            } catch (e) {
              $.wnoty({
                type: "error",
                autohide: false,
                message:
                  "Oops! an error occured during the image upload, \
                    Please try again later or contact us via support@obrisk.com" +
                  e
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
            Please try again later or contact us at support@obrisk.com"
          });
          $(".start-uploader").css("display", "block");
        }
      })
      .catch(e => {
        $.wnoty({
          type: "error",
          autohide: false,
          message:
            "Oops! an error occured before upload started, Please try again later or contact us via support@obrisk.com" +
            e
        });
        console.log(e);
      });
  }
};

/**
 * Allow users preview upload profile picture
 */

function uploadPreview(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $("#cover").attr("src", e.target.result);
      $("#cover").removeClass("d-none");
    };

    reader.readAsDataURL(input.files[0]);
  }
}

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
  //p percentage 0~1
  return function(done) {
    $totalProgressbar
      .css("width", "100%")
      .html("Upload started, please wait...");
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

function genKey(extension) {
  var filename =
    "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
      var r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    }) +
    "." +
    extension.split("/")[1] +
    "/";

  var date = new Date().toISOString().split("T")[0];
  return "media/images" + "/articles/" + user + "/" + date + "/" + filename;
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
});
