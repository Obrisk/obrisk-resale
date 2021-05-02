//let audio = new Audio("/static/sound/chime.mp3");
var url;

function scrollMessages() {
  /* Set focus on the input box from the form, and rolls to show the
        the most recent message.
    */
  document.querySelector("textarea[name='message']").focus();
  document.querySelector("#conversation").scrollTop = 99999999999;
}

function addListenerMulti(el, s, fn) {
  s.split(' ').forEach(e => el.addEventListener(e, fn, false));
}

function getFormatedTime() {
  let a = [{month: 'short'}, {day: 'numeric'}];
  const now = new Date();

   function format(m) {
      let f = new Intl.DateTimeFormat('en', m);
      return f.format(now);
   }

  return a.map(format).join(' ') + ` ${now.getHours()}:${now.getMinutes()}`;
}

document.addEventListener('DOMContentLoaded', function() {
  scrollMessages();
  //scroll when on textarea
  const div = document.querySelector(".message-scroll");
  const ta = document.querySelector("textarea");

  ta.addEventListener("keydown", autosize);

  function setUserOnlineOffline(username, status) {
    /* This function enables the client to switch the user connection
        status, allowing to show if an user is connected or not.
        */
    const elem = document.querySelector(".online-stat");
    if (elem) {
      if (status === "online" && username === activeUser) {
        document.querySelector(".status-light").style.color = "#28a745";
        elem.textContent = "online";
      } else {
        document.querySelector(".status-light").style.color = "#ffc107";
        elem.textContent = "offline";
      }
    }
  }

  function addNewMessage(message_id) {
    /* This function calls the respective AJAX view, so it will be able to
        load the received message in a proper way.*/
     fetch(
          "/ws/messages/receive-message/", {
          method : "GET",
          body: {
            message_id: message_id
          },
          credentials: 'same-origin',
          headers: {
            "X-Requested-With": "XMLHttpRequest"
          }
        }).then (resp => resp.text())
          .then (data => {
            document.getElementById("conversation").insertAdjacentHTML('beforeend', data);
            setTimeout(function() {
              document.getElementById("conversation").scrollTop = 99999999999;
            }, 200);
        })
    scrollMessages();
  }

  addListenerMulti(
      document.querySelector("textarea[name='message']"),
      'input selectionchange', function(event) {
      if (document.querySelector(".textarea").value === "") {
        document.getElementById("addBtn").classList.remove("is-hidden");
      } else {
        document.getElementById("addBtn").classList.add("is-hidden");
      }
  });

  document.querySelector("textarea[name='message']").addEventListener("focus", function(e) {
    document.getElementById("addBtn").classList.remove("is-hidden");
    document.getElementById("conversation").scrollTop = 99999999999;
  });

  document.getElementById("send").addEventListener('submit', function(e) {
    e.preventDefault();
    //make sure the textarea isn't empty before submitting the form
    if (document.querySelector(".textarea").value !== "") {

      const tme_stamp = getFormatedTime();

      const msg = `<div class="chat-message is-sent">
            <img src="${currentUserThumbnail}"
            alt="Picture Profile" style="width:42px;height:42px;border-radius: 50%;"
            class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid"
            id="pic">
            <div class="message-block">
                <span>${tme_stamp}</span>
                <div class="message-text">${document.getElementById("sendText").value}</div>
            </div>
        </div>`;
      document.getElementById("conversation").insertAdjacentHTML('beforeend', msg)

      fetch(
          "/ws/messages/send-message/", {
          method : "POST",
          body: new FormData(document.getElementById("send")),
          credentials: 'same-origin',
          headers: {
            "X-Requested-With": "XMLHttpRequest"
          }
        }).then (resp => resp.text())
          .then (data => {
              document.getElementById("send").reset();
              document.querySelector("textarea").value = "";
              document.getElementById("addBtn").classList.remove('is-hidden');
              document.querySelector("textarea[name='message']").focus();
              document.getElementById("conversation").scrollTop = 99999999999;
        })
    }
    return false;
  });

  document.getElementById("send-text").addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById("send").dispatchEvent(new Event('submit', { bubbles: true }));
  });

  //This helps the text in the textarea of the message to be send
  //when press enter and go new line with shift + enter!
  document.getElementById("sendText").addEventListener('keyup', function(e) {

    const sendCode = event.which || event.keyCode || event.charCode
    if ( sendCode == 13 && !e.shiftKey ) {
      document.getElementById("send").dispatchEvent(new Event("submit", { bubbles: true }));
      setTimeout(function(e) {
        document.getElementById("conversation").scrollTop=99999999999;
      }, 0);
    }
  });

  // WebSocket connection management block.
  // Correctly decide between ws:// and wss://
  const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  const ws_path =
    ws_scheme +
    "://" +
    window.location.host +
    "/ws/messages/" +
    currentUser +
    "/";
  const webSocket = new channels.WebSocketBridge();
  webSocket.connect(ws_path);

  window.onbeforeunload = function() {
    // Small function to run instruction just before closing the session.
    payload = {
      type: "recieve",
      sender: currentUser,
      set_status: "offline",
      key: "set_status"
    };
    webSocket.send(payload);
  };

  // Helpful debugging
  webSocket.socket.onopen = function() {
    // console.log("Connected to inbox stream");
    // Commenting this block until I find a better way to manage how to
    // report the user status.

    payload = {
      type: "recieve",
      sender: currentUser,
      set_status: "online",
      key: "set_status"
    };

    webSocket.send(payload);
  };

  webSocket.listen(function(event) {
    if (event.key === undefined) event = JSON.parse(event);
    switch (event.key) {
      case "message":
        if (activeUser != "" && activeUser != undefined) {
          if (event.sender === activeUser) {
            addNewMessage(event.message_id);
            // I hope there is a more elegant way to work this out.
            setTimeout(function() {
              document.getElementById("unread-count").classList.add('is-hidden');
            }, 1);
          } else {
            document.getElementById("new-message-" + event.sender).classList.remove('is-hidden');
          }
        }
        break;

      case "set_status":
        setUserOnlineOffline(event.sender, event.set_status);
        break;
      default:
        break;
    }
  });

  ossUpload = new OssUpload();
  ossUpload.init();
//End DomContentLoaded event listener code block
});

//localStorage.debug = "ali-oss";
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
var FileMaxSize = 20000000; //20MB
var images;
var img_error; //Records the errors happened during upload.
var client;
var imgClient; //If we'll  be checking the file size.
var ossUpload = "";
var obrisk_oss_url = "https://obrisk.oss-cn-hangzhou.aliyuncs.com/";

let retryCount = 0;
const retryCountMax = 5;

OssUpload.prototype = {
  constructor: OssUpload,
  // Binding event
  bindEvent: function() {
    const _this = this;

    document.querySelector("#chooseFile, #addBtn").addEventListener('click', function() {
      document.getElementById("image-file").click();
    });

    document.querySelector('input[type="file"]').addEventListener('change', function(e) {
      if (e.target.files && e.target.files[0]) {
        const reader = new FileReader();
        reader.onload = function() {

          const tme_stamp = getFormatedTime();

          const image = `<div class="chat-message is-sent"><img src="${currentUserThumbnail}"
                            alt="Picture Profile"
                            style="width:42px;height:42px;border-radius: 50%;"
                            class="rounded-circle profile-header-avatar img-fluid"
                            id="pic">
                            <div class="message-block"><span>${tme_stamp} </span>
                              <a data-fslightbox="gallery" href="${reader.result}">
                                <img style="width: 250px; height: 250px;" src="${reader.result}">
                              </a>
                            </div>
                        </div>`;
          document.getElementById("conversation").insertAdjacentHTML('beforeend', image);
          document.getElementById("conversation").scrollTop=99999999999;
        };
        reader.readAsDataURL(e.target.files[0]);
      }
      const files = e.target.files;
      //The length of the file already in the plugin, append
      const curIndex = uploader.fileList.length;
      let file = null;

      document.querySelector("#uploader .placeholder").classList.add('is-hidden');
      document.getElementById("statusBar").style.display = "flex";

      if (files.length == 0) {
        alert("No image selected , Please select one or more images");
      } else {
        for (let i = 0; i < files.length; i++) {
          file = files[i];
          //don't upload files with size greater than 20MB
          if (file.size <= FileMaxSize) {
            uploader.fileList[curIndex + i] = file;
            file.id = uploader.fileList[curIndex + i].id =
              "image" + (curIndex + i + 1); //Add id to each file
            uploader.fileStats.totalFilesSize += file.size; //Statistical file size
          } else {
            alert(
              file.name +
                " is larger than 20MB, please select images small than 20MB"
            );
          }
        }
        document.querySelector(".addBtn").classList.add('is-hidden');
      }
      uploader.fileStats.totalFilesNum = uploader.fileList.length;
      if (uploader.fileStats.totalFilesNum == 0) {
        event.preventDefault();
        alert("Please select images to upload!");
      } else {
        const length = uploader.fileStats.totalFilesNum;

        for (let i = 0; i < length; i++) {
          const filename = genKey();
          file = uploader.fileList[i];
          _this.uploadFile(file, filename);
        }
        uploader = {
          fileList: [],
          fileStats: {
            totalFilesNum: 0,
            totalFilesSize: 0,
            uploadFinishedFilesNum: 0,
            curFileSize: 0
          }
        };
      }
    });
  },

  /***
   *  upload files
   * @param file files to be uploaded
   * @param filename to which location to upload the file. In the official doc is named key
   * oss is object storage, there is no path path concept, it can still be viewed as a path
   */
  uploadFile: function(file, filename) {
    applyTokenDo().then(result => {
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
                }).then(function(res) {
                  //Try to get the dominat color from the uploaded image
                  //if it fails it means the image was corrupted during upload
                     submitOSSImage(res, upload);
                }).catch(err => {
                  console.error(err);
                  console.log(`err.name : ${err.name}`);
                  console.log(`err.message : ${err.message}`);
                  console.log(`err.request : ${err.requestId}`);

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
                      document.querySelector("ul.filelist li")
                        .querySelector(".success-span")
                        .classList.add("fail");
                      img_error = err.name + ", Message: " +
                        err.message + ", RequestID: " + err.requestId;

                      if (!images) {
                        images = "undef,classifieds/error-img.jpg";
                        alert(
                          "Oops! an error occured when uploading your image(s). Please try again later"
                        );
                      }
                    }
                  } else {
                    //Not timeout out error and there is nothing we can do
                    //Allow the users to submit the form atleast with default image.
                    img_error = err.name + ", Message: " +
                      err.message + ", RequestID: " + err.requestId;

                    if (!images) {
                      images = "undef,classifieds/error-img.jpg";
                      alert(
                        "Oops! an error occured, Pls try again or add our wechatID: Obrisk"
                      );
                    }
                  }
                });
              return results;
            } catch (e) {
              alert(
                "Oops! an error occured, Pls try again or add our wechatID: Obrisk"
              );
              console.log(e);
            }
          };
          return upload();
        } else {
          alert(
            "Oops!, it looks like there is a network problem, \
            Please try again later or contact us at support@obrisk.com"
          );
        }
      })
      .catch(e => {
        alert(
          "Oops! an error has occured, pls try again or add our wechatID: Obrisk"
        );
        console.log(e);
      });
   }
};

/**
 * get sts token
 *
 * TODO neeeds improvment to make ajax call ony when token has expired
 */
var applyTokenDo = function() {
  return new Promise((resolve, reject) => {
    fetch( oss_url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    }).then (result =>  {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        resolve(result);

    }).catch(error => {
        reject(e);
    });
  });
};

function submitOSSImage (res, upload) {
    fetch(
      obrisk_oss_url + res.name +"?x-oss-process=image/average-hue", {
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    }).then (resp =>  {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        document.getElementById(file.id)
            .children(".success-span").addClass("success");
        document.getElementById(file.id)
           .children(".file-panel").style.display = 'none';
        //Successfully uploaded + 1
        uploader.fileStats.uploadFinishedFilesNum++;
        //Currently uploaded file size
        uploader.fileStats.curFileSize += file.size;

        document.getElementById("image").value = res.name;
        //Send image to chat
        fetch(
          "/ws/messages/send-message/", {
          method: "POST",
          body: new FormData(document.getElementById("upload")),
          credentials: 'same-origin',
          headers: {
            "X-Requested-With": "XMLHttpRequest"
          }
        }).then (resp => resp.text())
          .then (data => {
              document.getElementById("image").value = "";
        }).catch (error => {
            printError('Image upload failed, please re-submit');
        });
     }).catch(error => {
        // if a file is corrupted during upload retry 5 times to upload it
        if (retryCount < retryCountMax) {
            retryCount++;
            console.error(`retryCount : ${retryCount}`);
            upload();
        } else {
            //We have retried to the max and there is nothing we can do
            //Allow the users to submit the form atleast with default image.
            uploader.fileStats.uploadFinishedFilesNum++; //Successfully uploaded + 1
            uploader.fileStats.curFileSize += file.size; //Currently uploaded file size

            img_error = res.name + ", Message: Corrupted image" +
              ", RequestID: " + res.name;
            if (!images) {
                images = "undef,classifieds/error-img.jpg";
                printError(
                  "Oops! an error occured, please try again later"
                );
            }
        }
    });
}

//File upload initializer
function OssUpload() {
  const _this = this;
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
    "media/images/messages/" + usernameSlug + "/" +
    activeUserSlug + "/" +
    "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
      const r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    })
  );
}
