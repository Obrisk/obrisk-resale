$(function () {
    function getCookie(name) {
        // Function to get any cookie available in the session.
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // This sets up every ajax call with proper headers.
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $("input, textarea").val('');

    $(".infinite-container").on("click", ".like-wrapper", function () {
        // Ajax call on action on like button.
        var li = $(this).closest(".card");
        var stories = $(li).attr("stories-id");

        $.ajax({
            url: '/stories/like/',
            data: {
                'stories': stories
            },
            type: 'GET',
            cache: false,
            success: function (data) {
                li.find(".likes-count .count").text(data.likes);

            }
        });
        return false;
    });

    //Cose comments
    $(".infinite-container").on("click", ".close-comments", function () {
        // Ajax call to request a given Stories object detail and thread, and to
        // show it in a modal.
        var post = $(this).closest(".card");
        var stories = $(post).attr("stories-id");
        post.find('.content-wrap').toggleClass('is-hidden');
        post.find('.comments-wrap').toggleClass('is-hidden')
    });


    //Show comments
    $(".infinite-container").on("click", ".is-comment", function () {
        // Ajax call to request a given Stories object detail and thread, and to
        var post = $(this).closest(".card");
        var stories = $(post).attr("stories-id");
        post.find('.content-wrap').toggleClass('is-hidden');
        post.find('.comments-wrap').toggleClass('is-hidden');
        $(".emojionearea-editor").keyup(function () {
            var counter = $(this).closest(".textarea-parent");
            counter.find(".counter .count").text(400 - $(this).val().length);
            $(this).height('auto');
            $(this).height($(this).prop('scrollHeight'));
        });
        $("input, textarea").val('');
        $('.emojionearea-editor').html("");
        $.ajax({
            url: '/stories/get-thread/',
            data: {
                'stories': stories
            },
            cache: false,

            success: function (data) {
                if (data.thread.trim() != "")
                    post.find(".comments-body").html(data.thread);
                post.find("input[name=parent]").val(data.uuid)
            }
        });
        $('.comment-textarea').addClass("focused");
    });

    //Comment on a story
    $("a#post-comment-button").click(function () {
        // Ajax call to register a reply to any given Stories object.
        post = $(this).closest('.card');
        $.ajax({
            url: '/stories/post-comment/',
            data: post.find(".replyStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function () {
                post.find(".comment-textarea").val("");
                post.find('.comments-count .count').html(parseInt(post.find('.comments-count .count').html(), 10) + 1);
                post.find('.content-wrap').toggleClass('is-hidden');
                post.find('.comments-wrap').toggleClass('is-hidden');
                var stories = $(post).attr("stories-id");
                $("input, textarea").val('');
                setTimeout(function () {
                    $.ajax({
                        url: '/stories/get-thread/',
                        data: {
                            'stories': stories
                        },
                        cache: false,

                        success: function (data) {
                            if (data.thread.trim() != "")
                                post.find(".comments-body").html(data.thread);
                            post.find("input[name=parent]").val(data.uuid)
                        }
                    });
                    post.find('.content-wrap').toggleClass('is-hidden');
                    post.find('.comments-wrap').toggleClass('is-hidden');

                }, 200);
            },
            error: function (data) {
                bootbox.alert(data.responseText);
            },
        });

    });

    //Character count 
    $("textarea").keyup(function () {
        var counter = $(this).closest(".textarea-parent");
        counter.find(".counter .count").text(400 - $(this).val().length);
        $(this).height('auto');
        $(this).height($(this).prop('scrollHeight'));
    });

    //Open publish mode
    $('#publish').on('click', function () {
        $('.app-overlay').addClass('is-active');
        $('.close-wrap').removeClass('d-none');
        $('.is-new-content').addClass('is-highlighted');

    });
    //Enable and disable publish button based on the textarea value length (1)
    $('#publish').on('input', function () {
        var valueLength = $(this).val().length;

        if (valueLength >= 1) {
            $('#publish-button').removeClass('is-disabled');
        } else {
            $('#publish-button').addClass('is-disabled');
        }
    })

    //Close compose box
    $('.close-publish').on('click', function () {
        $('.app-overlay').removeClass('is-active');
        $('.is-new-content').removeClass('is-highlighted');
        $('.close-wrap').addClass('d-none');
    });
    //Comment on a story
    $(".comment-button").click(function () {
        // Ajax call to register a reply to any given Stories object.
        $.ajax({
            url: '/stories/post-comment/',
            data: $("#replyStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function () {
                $(".comment-textarea").val("");
                $('.is-comment-count').html(parseInt($('.is-comment-count').html(), 10) + 1);
            },
            error: function (data) {
                bootbox.alert(data.responseText);
            },
        });
    });
    //Show comments
    $(".infinite-container").on("click", ".is-comment", function () {

        // Ajax call to request a given Stories object detail and thread, and to
        // show it in a modal.
        var post = $(this).closest(".card");
        var stories = $(post).attr("stories-id");
        post.find('.content-wrap').addClass('is-hidden');
        post.find('.comments-wrap').removeClass('is-hidden');
        post.find('textarea').focus();

        $.ajax({
            url: '/stories/get-thread/',
            data: {
                'stories': stories
            },
            cache: false,

            success: function (data) {
                if (data.thread.trim() != "")
                    post.find(".comments-body").html(data.thread);
                post.find("input[name=parent]").val(data.uuid)
            }
        });
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
        curFileSize: 0,
    },
};

//Upload instance object
var Buffer = OSS.Buffer;
var STS = OSS.STS;
var FileMaxSize = 13000000
var TotalFilesMaxSize = 8
var images;
var img_error; //Records the errors happened during upload.
var client;
var imgClient; //If we'll  be checking the file size.
var ossUpload = '';
var obrisk_oss_url = "https://obrisk.oss-cn-hangzhou.aliyuncs.com/";

let retryCount = 0;
const retryCountMax = 5;


OssUpload.prototype = {
    constructor: OssUpload,
    // Binding event
    bindEvent: function () {
        var _this = this;

        $("#chooseFile, #addBtn").click(function () {
            document.getElementById("image-file").click();
        });

        $('input[type="file"]').change(function (e) {
            $("#wrapper .container").css('display', "block");
            //console.log(e)
            var files = e.target.files;
            var curIndex = uploader.fileList.length; //The length of the file already in the plugin, append
            var NumberOfSelectedFiles = files.length;
            //console.log('total files selected ' + NumberOfSelectedFiles);
            var file = null;
            $('#uploader .placeholder').hide();

            var AllowUploadQuantity = TotalFilesMaxSize - curIndex;
            //console.log('number of files ' + AllowUploadQuantity)

            //check if the upload quantity has reach max 
            if (AllowUploadQuantity == 0) {
                bootbox.alert("Only " + TotalFilesMaxSize + " images are allowed");
                $('.addBtn').hide();
            } else if (files.length == 0) {
                bootbox.alert("No image selected , Please select one or more images");
            } else {

                //Add only the allow # of files to upload qeue
                if (NumberOfSelectedFiles <= AllowUploadQuantity && NumberOfSelectedFiles > 0) {

                    for (var i = 0; i < NumberOfSelectedFiles; i++) {
                        file = files[i];
                        //don't upload files with size greater than 13MB
                        if (file.size <= FileMaxSize) {
                            uploader.fileList[curIndex + i] = file;
                            file.id = uploader.fileList[curIndex + i].id = "image" + (curIndex + i + 1); //Add id to each file
                            uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                            _this.addFile(file); //Add to control view
                        } else {
                            bootbox.alert(file.name + ' is larger than 13MB, please select images small than 13MB ')

                        }

                    }
                } else {
                    for (var i = 0; i < NumberOfSelectedFiles && uploader.fileList.length < TotalFilesMaxSize; i++) {
                        file = files[i];
                        //don't upload files with size greater than 13MB
                        if (file.size <= FileMaxSize) {
                            uploader.fileList[curIndex + i] = file;
                            file.id = uploader.fileList[curIndex + i].id = "image" + (curIndex + i + 1); //Add id to each file
                            uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                            _this.addFile(file); //Add to control view
                        } else {

                            bootbox.alert(file.name + ' is larger than 13MB, please select images small than 13MB ')
                        }

                    }
                    bootbox.alert("Only " + TotalFilesMaxSize + " images are allowed");
                    $('.addBtn').hide();
                }

            }
            uploader.fileStats.totalFilesNum = uploader.fileList.length;
        });

        $("#startUpload").click(function (event) {
            if ($("#publish").val() == '') {
                event.preventDefault();
                bootbox.alert("Please fill in all of the information before uploading the images!");
            } else if (uploader.fileStats.totalFilesNum == 0) {
                event.preventDefault();
                bootbox.alert("Please select images to upload!");
                $(".start-uploader").css('display', 'block');

            } else {
                $("#statusBar").css('display', 'flex');
                var length = uploader.fileStats.totalFilesNum;
                var file;
                $(".start-uploader").css('display', 'none');
                $totalProgressbar.css('width', '40%')
                    .html('Upload Started please wait...');
                for (var i = 0; i < length; i++) {
                    var filename = genKey();
                    file = uploader.fileList[i];
                    _this.uploadFile(file, filename);
                }
            }
        });
        $(".queueList .filelist").delegate('li span.cancel', 'click', function () {
            var $this = $(this);
            var $li = $this.parent().parent();
            var id = $li.attr('id');
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
            if (uploader.fileList.length <= TotalFilesMaxSize) {
                $('.addBtn').show();
            }
        });

    },

    /***
     *  upload files
     * @param file files to be uploaded
     * @param filename to which location to upload the file. According to the official statement is the key
     * oss is object storage, there is no path path concept, but personally think this can be better understood as a path
     */
    uploadFile: function (file, filename) {

        $totalProgressbar.css('width', '30%').html('Uploading...');
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
                        const results = await client.multipartUpload(filename, file, {
                            progress: progress,
                            partSize: 200 * 1024, //Minimum is 100*1024
                            timeout: 120000, // 2 minutes timeout

                        })
                            .then(function (res) {

                                //Try to get the dominat color from the uploaded image, if it fails it means the image
                                //was corrupted during upload
                                $.ajax({
                                    url: obrisk_oss_url + res.name + "?x-oss-process=image/average-hue",
                                    success: function () {

                                        $("#" + file.id).children(".success-span").addClass("success");
                                        $("#" + file.id).children(".file-panel").hide();
                                        uploader.fileStats.uploadFinishedFilesNum++; //Successfully uploaded + 1
                                        uploader.fileStats.curFileSize += file.size; //Currently uploaded file size
                                        progressBarNum = (uploader.fileStats.curFileSize / uploader.fileStats.totalFilesSize).toFixed(2) * 100;
                                        progressBar = (uploader.fileStats.curFileSize / uploader.fileStats.totalFilesSize).toFixed(2) * 100 + '%';

                                        if (progressBarNum == 100) {
                                            $totalProgressbar.css('width', progressBar)
                                                .html('Upload complete');
                                        } else {
                                            $totalProgressbar.css('width', progressBar)
                                                .html(progressBar);
                                        }

                                        images += ',' + res.name;
                                    },
                                    error: function (e) {

                                        // if a file is corrupted during upload retry 5 times to upload it then skip it and return an error message
                                        if (retryCount < retryCountMax) {
                                            retryCount++;
                                            console.error(`retryCount : ${retryCount}`);
                                            upload();
                                        } else {
                                            //We have retried to the max and there is nothing we can do
                                            //Allow the users to submit the form atleast with default image.

                                            $("#" + file.id).children(".success-span").addClass("fail");
                                            $("#" + file.id).children(".file-panel").hide();
                                            uploader.fileStats.uploadFinishedFilesNum++; //Successfully uploaded + 1
                                            uploader.fileStats.curFileSize += file.size; //Currently uploaded file size
                                            progressBarNum = (uploader.fileStats.curFileSize / uploader.fileStats.totalFilesSize).toFixed(2) * 100;
                                            progressBar = (uploader.fileStats.curFileSize / uploader.fileStats.totalFilesSize).toFixed(2) * 100 + '%';

                                            if (progressBarNum == 100) {
                                                $totalProgressbar.css('width', progressBar)
                                                    .html('Upload complete');
                                            } else {
                                                $totalProgressbar.css('width', progressBar)
                                                    .html(progressBar);
                                            }
                                            img_error = res.name + ", Message: " + "Corrupted image" + ", RequestID: " + res.name;
                                            if (!images) {
                                                images = 'undef,classifieds/error-img.jpg';
                                                bootbox.alert("Oops! an error occured when uploading your image(s). \
                                                But you can submit this form without images and edit your post later to add images");
                                            }
                                        }
                                    }


                                }); //End of ajax function

                            }).catch((err) => {
                                console.error(err);
                                console.log(`err.name : ${err.name}`);
                                console.log(`err.message : ${err.message}`);
                                console.log(`err.request : ${err.requestId}`);

                                $totalProgressbar.css('width', '40%')
                                    .html("Retrying...");

                                if (err.name.toLowerCase().indexOf('connectiontimeout') !== -1) {
                                    if (retryCount < retryCountMax) {
                                        retryCount++;
                                        console.error(`retryCount : ${retryCount}`);
                                        upload();
                                    } else {
                                        //We have retried to the max and there is nothing we can do
                                        //Allow the users to submit the form atleast with default image.
                                        $totalProgressbar.css('width', '94%')
                                            .html("Completed with minor errors!");
                                        $("ul.filelist li").children(".success-span").addClass("fail");
                                        img_error = err.name + ", Message: " + err.message + ", RequestID: " + err.requestId;

                                        if (!images) {
                                            images = 'undef,classifieds/error-img.jpg';
                                            bootbox.alert("Oops! an error occured when uploading your image(s). \
                                            But you can submit this form without images and edit your post later to add images");
                                        }
                                    }
                                } else {
                                    //Not timeout out error and there is nothing we can do
                                    //Allow the users to submit the form atleast with default image.
                                    $totalProgressbar.css('width', '94%')
                                        .html("Completed with minor errors!");

                                    img_error = err.name + ", Message: " + err.message + ", RequestID: " + err.requestId;

                                    if (!images) {
                                        images = 'undef,classifieds/error-img.jpg';
                                        bootbox.alert("Oops! an error occured when uploading your image(s). \
                                            But you can submit this form without images and edit your post later to add images");
                                    }
                                }

                            });
                        return results;
                    } catch (e) {
                        bootbox.alert("Oops! an error occured when uploading your image(s), \
                    Please try again later or contact us via support@obrisk.com. " + e);
                        $(".start-uploader").css('display', 'block');
                        console.log(e);
                    }
                }
                return upload()
            } else {
                bootbox.alert("Oops!, it looks like there is a network problem, \
            Please try again later or contact us at support@obrisk.com")
                $(".start-uploader").css('display', 'block');
            }
        }).catch(e => {
            bootbox.alert('Oops! an error occured before upload started, Please try again later or contact us via support@obrisk.com' + e);
            console.log(e)
        })
    },

    /**
     * Add file to preview
     */
    addFile: function (file) {
        var $li = $('<li id="' + file.id + '">' +
            '<p class="title">' + file.name + '</p>' +
            '<p class="imgWrap"></p>' +
            '<p class="upload-state"><span></span></p><span class="success-span"></span>' +
            '</li>'),
            $btns = $('<div class="file-panel">' +
                '<span class="cancel">cancel</span>' +
                '</div>').appendTo($li),
            $prgress = $li.find('p.upload-state span'),
            $wrap = $li.find('p.imgWrap'),
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
            reader.onload = (function (aImg) {
                return function (e) {
                    aImg.src = e.target.result;
                };
            })(img);
            reader.readAsDataURL(file);
        }
        $li.appendTo($queue);
    },
}

/**
 * Create progress bar
 */
var progressBar = 0;
var progress = '';
var $wrap = $('#uploader'),
    // Picture container
    $queue = $('<ul class="filelist"></ul>').appendTo($wrap.find('.queueList')),
    $totalProgressbar = $("#totalProgressBar");

var progress = function (p) { //p percentage 0~1
    console.log(p);
    return function (done) {
        $totalProgressbar.css('width', progressBar)
        done();
    }
};

/**
 * get sts token
 * 
 * TODO neeeds improvment to make ajax call ony when token has expired
 */
var applyTokenDo = function () {
    var url = oss_url; //Request background to obtain authorization address url
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            success: function (result) {
                resolve(result)
            },
            error: function (e) {
                reject(e);
            }
        });
    });

};

//File upload initializer 
function OssUpload() {
    var _this = this;
    _this.init = function () {
        _this.initPage();
        _this.bindEvent();
    };
    _this.initPage = function () {

    };
}


/**
 * generate file name using uuid
 *
 * @return  {string}  
 */

function genKey() {
    return "stories/" + user + '/' + slugify($("#publish").val().substring(0, 20)) +
        '/' + 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
}

/**
 * create a slug 
 *
 * @param   {string}  string  string to be slugified
 *
 * @return  {slug}          slugified string
 */
function slugify(string) {
    const a = 'àáäâãåăæçèéëêǵḧìíïîḿńǹñòóöôœøṕŕßśșțùúüûǘẃẍÿź·/_,:;'
    const b = 'aaaaaaaaceeeeghiiiimnnnooooooprssstuuuuuwxyz------'
    const p = new RegExp(a.split('').join('|'), 'g')
    return string.toString().toLowerCase()
        .replace(/\s+/g, '-') // Replace spaces with -
        .replace(p, c => b.charAt(a.indexOf(c))) // Replace special characters
        .replace(/&/g, '-and-') // Replace & with ‘and’
        .replace(/[^\w\-]+/g, '') // Remove all non-word characters
        .replace(/\-\-+/g, '-') // Replace multiple - with single -
        .replace(/^-+/, '') // Trim - from start of text
        .replace(/-+$/, '') // Trim - from end of text
}




$(function () {

    //create and initialize upload object 
    ossUpload = new OssUpload();
    ossUpload.init();

    $("#publish-button").click(function () {
        // Ajax call after pushing button, to register a Stories object.
        $("#id_images").val(images);
        $("#id_img_error").val(img_error);
        $.ajax({
            url: '/stories/post-stories/',
            data: $("#postStoriesForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".infinite-container").prepend(data);
                $('[name="post"]').val("");
                $('.app-overlay').removeClass('is-active');
                $('.is-new-content').removeClass('is-highlighted');
                $('.close-wrap').addClass('d-none');
                feather.replace();
                $("#postStoriesForm")[0].reset();
                $("input, textarea").val('');
                $('#wrapper').html(`<div class="container" style="display: none;">
                                                <div id="uploader">
                                                <div class="queueList">
                                                    <div id="dndArea" class="placeholder" style="display: none;">
                                                    <div class="" id="uploaderPick">
                                                        <a id="chooseFile" href="javascript:void(0);" class="text">Add images</a>
                                                    </div>
                                                    </div>
                                                    <ul class="filelist"></ul>
                                                </div>
                                                </div>
                                                <div id="statusBar" class="statusBar  flex-column align-items-center" style="display: flex;">
                                                <div class="total-progress">
                                                    <div id="totalProgressBar" class="total-progress-bar" role="progressbar" aria-valuenow="0"
                                                    aria-valuemin="0" aria-valuemax="100">
                                                    </div>
                                                </div>
                                                <div class="upload-btn d-flex flex-column flex-md-row">
                                                    <div class="start-uploader startUploadBtn ml-2 mr-2">
                                                    <a id="startUpload" href="javascript:void(0);" class="text">Upload images</a>
                                                    </div>
                                                </div>
                                                </div>

                                                <div class="" style="clear: both;">
                                                <p class="text-center">
                                                    Notes:
                                                    Max number of files 8 &amp; Max size per file is 13MB
                                                </p>
                                                </div>
                                            </div>`);
            },
            error: function (data) {
                bootbox.alert(data.responseText);
            },
        });
    });


});