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

let retryCount = 0;
const retryCountMax = 5;

OssUpload.prototype = {
  constructor: OssUpload,
  // Binding event
  bindEvent: function() {
    var _this = this;

    $('input[type="file"]').change(function(e) {
      var file = e.target.files[0];

      $("#uploader .placeholder").hide();
      $("#statusBar").css("display", "flex");

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
              "The file you've chosen is too small. Please choose a file greater than 5KB but lower than 13MB!"
          });
        }

        //don't upload files with size greater than 13MB
        if (file.size <= FileMaxSize) {
          uploader.file = file;
          uploader.totalFilesSize = file.size;
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
      uploader.totalFilesNum = 1;
    });

    $("#startUpload").click(function(event) {
      if (uploader.totalFilesNum == 0) {
        event.preventDefault();
        $.wnoty({
          type: "error",
          autohide: false,
          message:
            "Please select the image to upload first by clicking the choose pic button!"
        });
      } else {
        var filename = genKey();
        var file = uploader.file;
        $totalProgressbar.html("Upload has started, please wait...");
        $("#startUpload").hide();
        _this.uploadFile(file, filename);
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
    applyTokenDo();

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
                $totalProgressbar
                  .css("width", progressBar)
                  .html(
                    "Upload has completed. Please save the changes at the bottom of the page!"
                  );
                $("#startUpload").hide();
              }
              image = res.name;
            })
            .catch(err => {
              console.error(err);
              console.log(`err.name : ${err.name}`);
              console.log(`err.message : ${err.message}`);

              if (err.name.toLowerCase().indexOf("connectiontimeout") !== -1) {
                // timeout retry
                if (retryCount < retryCountMax) {
                  retryCount++;
                  console.error(`retryCount : ${retryCount}`);
                  upload();
                } else {
                  //We have retried to the max and there is nothing we can do
                  //Allow the users to submit the form atleast with default image.
                  $totalProgressbar
                    .css("width", "80%")
                    .html("Upload facing errors!");
                }
              } else {
                //Not timeout out error and there is nothing we can do
                //Allow the users to submit the form atleast with default image.
                $totalProgressbar
                  .css("width", "80%")
                  .html("Upload facing error!");
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
  }
};

/**
 * Allow users preview upload profile picture
 */

function uploadPreview(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $("#avatar").attr("src", e.target.result);
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
    $totalProgressbar.html("Upload has started, please wait...");
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
  $.ajax({
    url: url,
    async: false,
    success: function(result) {
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
    },
    error: function(e) {
      $.wnoty({
        type: "error",
        autohide: false,
        message:
          "Oops! an error occured before upload started, Please try again later or contact us via support@obrisk.com" +
          e
      });
      console.log(e);
    }
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
  return (
    "media/profile_pics/" +
    user +
    "/pics/" +
    "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
      var r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    })
  );
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

  $("#post-submit").click(function(event) {
    if (
      $("#id_title").val() == "" ||
      $("#id_details").val() == "" ||
      $("#id_tags").val() == ""
    ) {
      event.preventDefault();
      $.wnoty({
        type: "error",
        autohide: false,
        message:
          "Please fill in all of the information before uploading the images!"
      });
    } else if (uploader.fileStats.totalFilesNum == 0) {
      event.preventDefault();
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please select images to upload!"
      });
      $(".start-uploader").css("display", "block");
    } else {
      var file;
      var filename = genKey();
      file = uploader.fileList[i];
      _this.uploadFile(file, filename);
    }

    $("input[name='status']").val("A");
    $("#oss_image").val(image);
    $("#classified-form").submit();
  });

  $("#post-draft").click(function() {
    $("input[name='status']").val("E");
    $("#classified-form").submit();
  });
});
