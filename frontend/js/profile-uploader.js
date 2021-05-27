//Print error message
function printError(msg) {
  document.getElementsByClassName('notification')[0].classList.remove('is-hidden'); 
  document.getElementById('notf-msg').innerHTML = msg;
  window.scroll({
      top: 0, 
      left: 0, 
      behavior: 'smooth'
  });
}

function choosePic() {
    document.getElementById('temp_pic').click();
    document.getElementById('startUpload').classList.remove('is-hidden');
    document.getElementById('choosePic').classList.add('is-hidden');
}


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
var FileMaxSize = 200000000; //20MB
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

      $("#uploader .placeholder").hide();
      $("#statusBar").css("display", "flex");

      //check if the upload quantity has reach max
      if (!file) {
          printError("No image selected , Pls select an image first");
      } else {
        if (file.size <= 5000) {
          printError("The image is too small. Pls choose image greater than 5KB");
        }

        //don't upload files with size greater than 13MB
        if (file.size <= FileMaxSize) {
          uploader.file = file;
          uploader.totalFilesSize = file.size;
        } else {
          printError("This image is larger than 20MB, pls select smaller image ");
        }
      }
      uploader.totalFilesNum = 1;
    });

    $("#startUpload").click(function(event) {
      if (uploader.totalFilesNum == 0) {
        event.preventDefault();
        printError("Please select the image to be saved by clicking the choose pic button!");
      } else {
        var filename = genKey();
        var file = uploader.file;
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
                  partSize: 200 * 1024, //Minimum is 100*1024
                  timeout: 120000 // 2 minutes timeout
                })
                .then(function(res) {
                  uploader.uploadFinishedFilesNum++;
                  uploader.curFileSize += file.size;

                  var progressBarNum = (1).toFixed(2) * 100;

                  if (progressBarNum == 100) {
                    //Try to edit the uploaded image, if it fails it means the image
                    //was corrupted during upload
                    $.ajax({
                      url:
                        obrisk_oss_url +
                        res.name +
                        "?x-oss-process=image/average-hue",
                      success: function() {
                        $.ajax({
                          url: "/users/update-profile-pic/",
                          data: {
                            profile_pic: res.name
                          },
                          cache: false,
                          type: "POST",
                          success: function(result) {
                            if (result.success) {
                              $("#startUpload").hide();
                              document.getElementById('choosePic').classList.remove('is-hidden');
                              document.getElementById('successText').innerHTML = 'The photo has been updated✔️';
                            } else {
                              $("#startUpload").show();
                            }
                          },
                          error: function(e) {
                            console.log(e);
                            $("#startUpload").show();
                          }
                        });
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
                          $("#startUpload").show();
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
                    } 
                  } 
                });
              return results;
            } catch (e) {
              printError("Oops! an error has occured. Pls try again or add our wechat Obrisk");
              $(".start-uploader").css("display", "block");
              console.log(e);
            }
          };

          return upload();
        } else {
          printError("Oops! an error has occured. Pls try again or add our wechat Obrisk")
          $(".start-uploader").css("display", "block");
        }
      })
      .catch(e => {
        printError("Oops! an error has occured. Pls try again or add our wechat Obrisk")
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
      $("#avatar").attr("src", e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
    $("#startUpload").show();
  }
}


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
  return (
    "media/images/profile_pics/" +
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


document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.close-dj-messages').forEach(item => {
            item.addEventListener('click', e => {
                e.currentTarget.parentElement.classList.add('is-hidden');
                e.stopPropagation();
            });
      });

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

  //create and initialize upload object
  ossUpload = new OssUpload();
  ossUpload.init();

  $("#update-profile").click(function(event) {
    if ($("select[name='province']").val() && !$("select[name='city']").val()) {
        event.preventDefault();
        printError('Province and city must be updated together');
    } else {
      $("input[name='city']").val($("select[name='city']").val());
      $("input[name='province_region']").val($("select[name='province']").val());
      $("#update").submit();
    }
  });

});
