$(function () {
  $("#post-submit").click(function (event) {
    event.preventDefault();
    $("input[name='status']").val("P");

    if ($("#id_title").val() == "" || $("#id_image").val() == "") {
      event.preventDefault();
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please fill in all the required fields.",
      });
    } else {
      $("#id_content_html").val(quill.root.innerHTML);
      $("#id_content_json").val(JSON.stringify(quill.getContents()));
      $("#posts-form").submit();
    }
  });

  $("#post-update").click(function () {
    $("input[name='status']").val("P");
    $("input[name='edited']").val("True");

    if ($("#id_title").val() == "" || $("#id_image").val() == "") {
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please fill in all the required fields.",
      });
    } else {
      $("#id_content_html").val(quill.root.innerHTML);
      $("#id_content_json").val(JSON.stringify(quill.getContents()));
      $("#posts-form").submit();
    }
  });

  $("#post-draft").click(function () {
    $("input[name='status']").val("D");

    event.preventDefault();
    if ($("#id_title").val() == "" || $("#id_image").val() == "") {
      event.preventDefault();
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please fill in all the required fields.",
      });
    } else {
      $("#id_content_html").val(quill.root.innerHTML);
      $("#id_content_json").val(JSON.stringify(quill.getContents()));
      $("#posts-form").submit();
    }
  });

  $("#chooseFile").click(function () {
    $("#uploader").show();
  });

  $("body").on("uploadComplete", function (event) {
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

  $("#startImgUpload").click(function (event) {
    console.log("clicked");
    if (uploader.fileStats.totalFilesNum > 0) {
      $("body").trigger("submitClicked");
      console.log("submit trigged");
    } else {
      $.wnoty({
        type: "error",
        autohide: false,
        message: "Please upload at least one image for your post",
      });
    }
  });
});

$(document).ready(function () {
  $.fn.serializeToJSON = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
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
  $(function () {
    $(".comment-btn").click(function (event) {
      event.preventDefault();

      $.ajax({
        method: "POST",
        url: url,
        data: $("#commentForm").serialize(),
        processData: false,
        success: function (data) {
          $("#comment-notify").html(data);
          $("#commentForm")[0].reset();
          location.reload();
        },
        error: function (err) {
          console.log(err);
        },
      });
    });
  });
});
