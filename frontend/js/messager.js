//let audio = new Audio("/static/sound/chime.mp3");
var current_conv, last_stamp, last_msg, current_lst_stamp;

try {
    last_msg = document.getElementById('last-msg').value;
    current_lst_stamp = document.getElementById('last-timestamp').value;
} catch (err) {}

const bottomNav = document.getElementById('navbarBottom');

function scrollMessages() {
  /* Set focus on the input box from the form, and rolls to show the
        the most recent message.
    */
  $("textarea[name='message']").focus();
  $("#conversation").scrollTop(99999999999);
}

$(function() {
  //scroll when on textarea
  const div = document.querySelector(".message-scroll");
  const ta = document.querySelector("textarea");

  ta.addEventListener("keydown", autosize);

  function autosize() {
    setTimeout(function() {
      const height = Math.min(20 * 5, ta.scrollHeight);
      div.style.cssText = "height:" + height + "px";
      ta.style.cssText = "height:" + height + "px";
    }, 0);
  }

  const setCookie = function(name, value, days) {
    let expires;

    if (!name && !value) {
        return false;
    } else if (days) {
        const date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toGMTString();
    } else expires = "";

    document.cookie = name + "=" + value + expires + "; path=/";
    return true;
  };

  const getCookie = function(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(";");
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) === " ") c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  };

  const deleteCookie = function(name) {
    if (name) {
      setCookie(name, "", -1);
      return true;
    }
  };

  function loadMessages(chat) {
    $.ajax({
      type: "get",
      url: chat,
      success: function(response) {
        current_conv = response.current_conv; 

        const activeUserThumbnail =
          response.active_thumbnail == null
            ? "/static/img/user.png"
            : response.active_thumbnail;

        $(".avatar-container").append(
          `<img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${activeUserThumbnail}"
               alt="Picture Profile"
                style="width:30px;height:30px;border-radius: 50%;"
                class="user-avatar rounded-circle profile-header-avatar img-fluid"
                id="pic">
                `
        );

        $(".username").append(`  <span>${response.active_username}</span>`);

        response.msgs.map(function(el) {
          if (el.sender_username == response.active_username) {
            if (el.image != null) {
              $("#conversation").append(
                  `<div class="chat-message is-received">
                      <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${activeUserThumbnail}"
                      alt="Picture Profile" style="width:30px;height:30px;border-radius: 50%;"
                      class="rounded-circle profile-header-avatar img-fluid" id="pic">

                      <div class="message-block">
                          <span>${moment(el.timestamp).format(
                            "MMM. Do h:mm"
                          )}</span>

                      <a data-fancybox="gallery" style="width: 250px; height: 250px;"
                        href="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${el.image}">
                        <img style="width: 250px; height: 250px;"
                          src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${
                              el.img_preview
                          } " />
                       </a>
                      </div>
                  </div > `
              );
            }
            if (el.classified_title != null) {
              $("#conversation")
                .append(
                    `<div class="chat-message is-received" style="background-color: transparent;">
                        <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${activeUserThumbnail}"
                        alt="Picture Profile" style="width:30px;height:30px;border-radius: 50%;"
                        class="rounded-circle profile-header-avatar img-fluid" id="pic">

                          <div class="message-block">
                            <span>${moment(el.timestamp).format(
                              "MMM. Do h:mm"
                            )}</span>

                            <div class="message-text">
                            <div class="card classified-card mr-2 mb-3 justify-content-center is-flex"
                            style="max-width: 295px">

                            <a href="/classifieds/${el.classified_slug}"
                            style="color:black; text-decoration:none; background-color:none" class="is-flex">
                              <div class="card-img-top img-responsive">
                                               <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${
                                                 el.classified_thumbnail
                                               }" alt="${el.classified_title}" style="max-width: 70px">
                              </div>
                              <div style"margin-left: 5px">
                                <h6 class="card-title"> ${el.classified_title} </h6>
                                <p class="card-subtitle O-cl-red"> CNY ${
                                  el.classified_price
                                } </p>
                              </div>
                            </a>
                          </div></div>
                      </div>
                  </div>`
               );
            }
            if (el.message != null) {
              $("#conversation")
                .append(`<div class="chat-message is-received" >
                          <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${activeUserThumbnail}" alt="Picture Profile"
                          style="width:30px;height:30px;border-radius: 50%;"
                          class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid" id="pic">

                          <div class="message-block">
                            <span>${moment(el.timestamp).format(
                              "MMM. Do h:mm"
                            )}</span>
                            <div class="message-text">${el.message}</div>
                          </div>
                      </div>`);
            }
          } else {
            if (el.image != null) {
              $("#conversation").append(`<div class="chat-message is-sent">

                          <img src="${currentUserThumbnail}" alt="Picture Profile"
                              style="width:30px;height:30px;border-radius: 50%;"
                              class="rounded-circle profile-header-avatar img-fluid" id="pic">

                          <div class="message-block">
                              <span>${moment(el.timestamp).format(
                                "MMM. Do h:mm"
                              )}</span>
                              <a data-fancybox="gallery" style="width: 250px; height: 250px;"
                href="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${
                  el.image
                }"><img
                    style="width: 250px; height: 250px;"
                    src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${
                      el.img_preview
                    } " /></a>
                          </div>
                      </div > `);
            }
            if (el.classified_title != null) {
              $("#conversation")
                .append(`<div class="chat-message is-sent "style="background-color: transparent;">
                          <img src="${currentUserThumbnail}" alt="Picture Profile"
                          style="width:30px;height:30px;border-radius: 50%;"
                          class="rounded-circle profile-header-avatar img-fluid" id="pic">

                          <div class="message-block">
                            <span>${moment(el.timestamp).format(
                              "MMM. Do h:mm"
                            )}</span>
                            <div class="message-text">
                                <div class="card classified-card justify-content-center is-flex"
                                style="max-width: 295px">
                                    <a href="/classifieds/${el.classified_slug }" class="is-flex" 
                                      style="color:black; text-decoration:none; background-color:none">
                                      <div class="card-img-top img-responsive">
                                        <img src="https://obrisk.oss-cn-hangzhou.aliyuncs.com/${
                                          el.classified_thumbnail
                                        }" alt="${el.classified_title}" style="max-width: 70px">
                                      </div>
                                      <div style"margin-left: 5px">
                                        <h6 class="card-title"> ${el.classified_title} </h6>
                                        <p class="card-subtitle O-cl-red"> CNY ${
                                          el.classified_price
                                        } </p>
                                      </div>
                                    </a>
                              </div>
                            </div>
                          </div>
                        </div>`
                );
            }
            if (el.message != null) {
              $("#conversation")
                .append(`<div class="chat-message is-sent" ><img src="${currentUserThumbnail}" alt="Picture Profile"
                          style="width:30px;height:30px;border-radius: 50%;"
                          class="rounded-circle profile-header-avatar img-fluid" id="pic">

                          <div class="message-block">
                            <span>${moment(el.timestamp).format(
                              "MMM. Do h:mm"
                            )}</span>
                            <div class="message-text">${el.message}</div>
                          </div>
                      </div>`
                );
            }
          }
        });

        $(".sendTo").val(response.active_username);
        activeUser = response.active_username;
        $("#conversation").scrollTop(99999999999);
      }
    });
  }

  //This will only run once and then delete the cookies
  if (getCookie("active-chat")) {
    $("#chat-window").modal("show");
    loadMessages(getCookie("active-chat"));
    bottomNav.style.display = "none";
    //Clear the cookies obtained from the classified details
    deleteCookie("active-chat");
  }

  $(".open-chat").click(function() {
    loadMessages($(this).data("url"));
    bottomNav.style.display = "none";
  });

  $(".delete").click(function(e) {
    //Clear previous chat
    $("#conversation").html("");
    $(".avatar-container").html("");
    $(".username").html("");
    $("body").removeClass("modal-open");
    $("body").removeClass("is-frozen");
    bottomNav.style.display = "block";

    const lst_conv = document.getElementById(current_conv)

    if (current_lst_stamp !== last_stamp) {
        document.getElementsByClassName('users-list')[0].prepend(
            lst_conv
        );
        lst_conv.querySelector('.msg').innerHTML = last_msg;
        lst_conv.querySelector('.timestamp').innerHTML = last_stamp;
        current_lst_stamp = last_stamp;
    }

    try {
        const notif_icon = lst_conv.querySelector('.msg-notification');
        if (notif_icon !== null) 
            notif_icon.style.display = 'none';
    } catch (err) {}
  });

  function setUserOnlineOffline(username, status) {
    /* This function enables the client to switch the user connection
        status, allowing to show if an user is connected or not.
        */
    const elem = $(".online-stat");
    if (elem) {
      if (status === "online" && username === activeUser) {
        $(".status-light").css("color", "#28a745");
        elem.text("online");
      } else {
        $(".status-light").css("color", "#ffc107");
        elem.text("offline");
      }
    }
  }

  function addNewMessage(message_id) {
    /* This function calls the respective AJAX view, so it will be able to
        load the received message in a proper way.*/
    $.ajax({
      url: "/ws/messages/receive-message/",
      data: {
        message_id: message_id
      },
      cache: false,
      success: function(data) {
        $("#conversation").append(data);
        setTimeout(function() {
          $("#conversation").scrollTop(99999999999);
        }, 200);
      }
    });
    scrollMessages();
  }

  //Remove file upload when user start typing
  $("textarea[name='message']").on(
    "input selectionchange propertychange",
    function() {
      if ($("textarea").val() === "") {
        $("#addBtn").removeClass("is-hidden");
      } else {
        $("#addBtn").addClass("is-hidden");
      }
    }
  );

  $("textarea[name='message']").on("focus", function(e) {
    $("#addBtn").removeClass("is-hidden");
    $("#conversation").scrollTop(99999999999);
  });

  $("#send").submit(function(e) {
    e.preventDefault();
    //make sure the textarea isn't empty before submitting the form
    if ($("textarea").val() !== "") {
      const tme_stamp = moment().format("MMM. Do h:mm");

      const msg = `<div class="chat-message is-sent">
            <img src="${currentUserThumbnail}"
            alt="Picture Profile" style="width:30px;height:30px;border-radius: 50%;"
            class="rounded-circle  mb-3 mb-md-0 mr-md-3 profile-header-avatar img-fluid"
            id="pic">
            <div class="message-block">
                <span>${tme_stamp}</span>
                <div class="message-text">${$("#sendText").val()}</div>
            </div>
        </div>`;
      $("#conversation").append(msg);

      $.ajax({
        url: "/ws/messages/send-message/",
        data: $("#send").serialize(),
        cache: false,
        type: "POST",
        success: function(data) {
          //enable send button after message is sent
          //$('.send-btn').removeAttr("disabled");
          last_msg = $("#sendText").val().substring(0, 48);
          last_stamp = tme_stamp;

          $("#send")[0].reset();
          $("textarea").val("");
          $("textarea[name='message']").focus();
          $("#conversation").scrollTop(99999999999);

        },
        fail: function() {
          $.wnoty({
            type: "error",
            autohide: false,
            message: "failed to send the message"
          });
        }
      });
    }
    return false;
  });

  $("#send-text").click(function(e) {
    e.preventDefault();
    $("#send").trigger("submit");
  });

  //This helps the text in the textarea of the message to be send
  //when press enter and go new line with shift + enter!
  $("#sendText").keypress(function(e) {
    if (
      e.which == 13 &&
      !e.shiftKey &&
      !$(".send-btn").is('[disabled="disabled"]')
    ) {
      $("#send").trigger("submit");
      setTimeout(function(e) {
        $("#conversation").scrollTop(99999999999);
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
              $("#unread-count").hide();
            }, 1);
          } else {
            $("#new-message-" + event.sender).show();
          }
        }
        break;

      case "set_status":
        setUserOnlineOffline(event.sender, event.set_status);
        break;
      default:
        break;
    }
    scrollMessages();
  });
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
var FileMaxSize = 13000000;
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

    $("#chooseFile, #addBtn").click(function() {
      document.getElementById("image-file").click();
    });

    $('input[type="file"]').change(function(e) {
      if (e.target.files && e.target.files[0]) {
        const reader = new FileReader();
        reader.onload = function() {

          const tme_stamp = moment().format("MMM. Do h:mm");

          const image = `<div class="chat-message is-sent"><img src="${currentUserThumbnail}"
                            alt="Picture Profile"
                            style="width:30px;height:30px;border-radius: 50%;"
                            class="rounded-circle profile-header-avatar img-fluid is-hidden-mobile"
                            id="pic">
                            <div class="message-block"><span>${tme_stamp} </span>
                              <a data-fancybox="gallery" href="${reader.result}">
                                <img style="width: 250px; height: 250px;" src="${reader.result}">
                              </a>
                            </div>
                        </div>`;
          $("#conversation").append(image);
          $("#conversation").scrollTop(99999999999);

          last_msg = 'Attachment';
          last_stamp = tme_stamp;

        };
        reader.readAsDataURL(e.target.files[0]);
      }
      var files = e.target.files;
      //The length of the file already in the plugin, append
      var curIndex = uploader.fileList.length;
      var NumberOfSelectedFiles = files.length;
      var file = null;
      $("#uploader .placeholder").hide();
      $("#statusBar").css("display", "flex");

      if (files.length == 0) {
        alert("No image selected , Please select one or more images");
      } else {
        for (var i = 0; i < NumberOfSelectedFiles; i++) {
          file = files[i];
          //don't upload files with size greater than 13MB
          if (file.size <= FileMaxSize) {
            uploader.fileList[curIndex + i] = file;
            file.id = uploader.fileList[curIndex + i].id =
              "image" + (curIndex + i + 1); //Add id to each file
            uploader.fileStats.totalFilesSize += file.size; //Statistical file size
          } else {
            alert(
              file.name +
                " is larger than 13MB, please select images small than 13MB "
            );
          }
        }
        $(".addBtn").hide();
      }
      uploader.fileStats.totalFilesNum = uploader.fileList.length;
      if (uploader.fileStats.totalFilesNum == 0) {
        event.preventDefault();
        alert("Please select images to upload!");
        $(".start-uploader").css("display", "block");
      } else {
        var length = uploader.fileStats.totalFilesNum;

        for (var i = 0; i < length; i++) {
          var filename = genKey();
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

    $(".retry-upload").on("click", function(image) {
      e.preventDefault();
      var length = uploader.fileStats.totalFilesNum;

      for (var i = 0; i < length; i++) {
        var filename = genKey();
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
    });
  },

  /***
   *  upload files
   * @param file files to be uploaded
   * @param filename to which location to upload the file. In the official doc is named key
   * oss is object storage, there is no path path concept, it can still be viewed as a path
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
                  //Try to get the dominat color from the uploaded image
                  //if it fails it means the image was corrupted during upload

                  //
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
                      //Successfully uploaded + 1
                      uploader.fileStats.uploadFinishedFilesNum++;
                      //Currently uploaded file size
                      uploader.fileStats.curFileSize += file.size;
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

                      $("#image").val(res.name);
                      //Send image to chat

                      $.ajax({
                        url: "/ws/messages/send-message/",
                        data: $("#upload").serialize(),
                        cache: false,
                        type: "POST",
                        success: function(data) {
                          $("#image").val("");
                        },
                        fail: function(err) {
                          $("body").trigg("showRetry");
                          console.log(err);
                        }
                      });
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
                        if (!images) {
                          images = "undef,classifieds/error-img.jpg";
                          alert(
                            "Oops! an error occured when uploading your image(s). Please try again later"
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
                      img_error =
                        err.name +
                        ", Message: " +
                        err.message +
                        ", RequestID: " +
                        err.requestId;

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
                    $totalProgressbar
                      .css("width", "94%")
                      .html("Completed with minor errors!");

                    img_error =
                      err.name +
                      ", Message: " +
                      err.message +
                      ", RequestID: " +
                      err.requestId;

                    if (!images) {
                      images = "undef,classifieds/error-img.jpg";
                      alert(
                        "Oops! an error occured when uploading your image(s). Please try again later"
                      );
                    }
                  }
                });
              return results;
            } catch (e) {
              alert(
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
          alert(
            "Oops!, it looks like there is a network problem, \
            Please try again later or contact us at support@obrisk.com"
          );
          $(".start-uploader").css("display", "block");
        }
      })
      .catch(e => {
        alert(
          "Oops! an error occured before upload started, Please try again later or contact us via support@obrisk.com" +
            e
        );
        console.log(e);
      });
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
  //p percentage 0~1
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
  return new Promise((resolve, reject) => {
    $.ajax({
      url: oss_url,
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
    "media/images/messages/" +
    currentUser +
    "/" +
    activeUser +
    "/" +
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
  ossUpload = new OssUpload();
  ossUpload.init();
});


/* 
 * Sharing Code for inviting users on Chat
 */
navigator.share =
  navigator.share ||
  (function() {
    if (navigator.share) {
      return navigator.share;
    }

    let android = navigator.userAgent.match(/Android/i);
    let ios = navigator.userAgent.match(/iPhone|iPad|iPod/i);
    let isDesktop = !(ios || android); // on those two support "mobile deep links", so HTTP based fallback for all others.

    // sms on ios 'sms:;body='+payload, on Android 'sms:?body='+payload
    let shareUrls = {
      whatsapp: payload =>
        (isDesktop
          ? "https://api.whatsapp.com/send?text="
          : "whatsapp://send?text=") + payload,
      facebook: (payload, fbid, url) =>
        !fbid
          ? ""
          : (isDesktop
              ? "https://www.facebook.com/dialog/share?app_id=" +
                fbid +
                "&display=popup&href=" +
                url +
                "&redirect_uri=" +
                encodeURIComponent(location.href) +
                "&quote="
              : "fb-messenger://share/?message=") + payload,
      email: (payload, title) =>
        "mailto:?subject=" + title + "&body=" + payload,
      sms: payload => "sms:?body=" + payload
    };

    class WebShareUI {
      /*async*/
      _init() {
        if (this._initialized) return Promise.resolve();
        this._initialized = true;

        const template = `<div class="web-share" style="display: none">
      <div class="web-share-container web-share-grid">
        <div class="web-share-title">SHARE VIA</div>
        <a class="web-share-item web-share-whatsapp" data-action="share/whatsapp/share" target="_blank">
          <div class="web-share-icon-whatsapp"></div>
          <div class="web-share-item-desc">Whatsapp</div>
        </a>
        <a class="web-share-item web-share-email">
          <div class="web-share-icon-email"></div>
          <div class="web-share-item-desc">Email</div>
        </a>
        <a class="web-share-item web-share-sms">
          <div class="web-share-icon-sms"></div>
          <div class="web-share-item-desc">SMS</div>
        </a>
        <a class="web-share-item web-share-copy">
          <div class="web-share-icon-copy"></div>
          <div class="web-share-item-desc">Copy</div>
        </a>
      </div>
      <div class="web-share-container web-share-cancel">Cancel</div>
    </div>`;

        const el = document.createElement("div");
        el.innerHTML = template;

        this.$root = el.querySelector(".web-share");
        this.$whatsapp = el.querySelector(".web-share-whatsapp");
        this.$email = el.querySelector(".web-share-email");
        this.$sms = el.querySelector(".web-share-sms");
        this.$copy = el.querySelector(".web-share-copy");
        this.$copy.onclick = () => this._copy();
        this.$root.onclick = () => this._hide();
        this.$root.classList.toggle("desktop", isDesktop);

        document.body.appendChild(el);
      }

      _setPayload(payloadObj) {
        let payload =
          payloadObj.text + "  Click the link to view. " + payloadObj.url;
        let title = payloadObj.title;
        this.url = payloadObj.url;
        payload = encodeURIComponent(payload);
        title = encodeURIComponent(title);
        this.$whatsapp.href = shareUrls.whatsapp(payload);
        this.$email.href = shareUrls.email(payload, title);
        this.$sms.href = shareUrls.sms(payload);
      }

      _copy() {
        // A <span> contains the text to copy
        const span = document.createElement("span");
        span.textContent = this.url;
        span.style.whiteSpace = "pre"; // Preserve consecutive spaces and newlines

        // Paint the span outside the viewport
        span.style.position = "absolute";
        span.style.left = "-9999px";
        span.style.top = "-9999px";

        const win = window;
        const selection = win.getSelection();
        win.document.body.appendChild(span);

        const range = win.document.createRange();
        selection.removeAllRanges();
        range.selectNode(span);
        selection.addRange(range);

        let success = false;
        try {
          success = win.document.execCommand("copy");
        } catch (err) {}

        selection.removeAllRanges();
        span.remove();

        return success;
      }

      /*async*/
      show(payloadObj) {
        this._init();
        clearTimeout(this._hideTimer);
        this._setPayload(payloadObj);
        this.$root.style.display = "flex";
        this.$root.offsetWidth; // style update
        this.$root.style.background = "rgba(0,0,0,.4)";
        document.querySelectorAll(".web-share-container").forEach(el => {
          el.style.transform = "translateY(0)";
          el.style.opacity = 1;
        });
      }

      _hide() {
        this.$root.style.background = null;
        document.querySelectorAll(".web-share-container").forEach(el => {
          el.style.transform = null;
          el.style.opacity = null;
        });
        this._hideTimer = setTimeout(
          () => (this.$root.style.display = null),
          400
        );
      }
    }

    const shareUi = new WebShareUI();

    /* async */
    return data => shareUi.show(data);
  })();

/* Todo: auto select value to open native copy/share dialog */

/* Todo: facebook share message dialog for desktops
http://www.facebook.com/dialog/send
	?app_id=123456789
		&link=http://www.nytimes.com/
		&redirect_uri=https://www.domain.com/
	*/

// See also: http://chriswren.github.io/native-social-interactions/

// See also: https://www.sharethis.com/platform/share-buttons/

