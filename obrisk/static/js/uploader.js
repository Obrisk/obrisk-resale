/**
 * Created By WiFi ON 2017/11/25 16:31
 * github: https://github.com/WiFiUncle/ossUploader
 */


'use strict';
//(function(w) {
/**
* The above four parameters are obtained from the background.The bucket and region can be written in the foreground, but
for the convenience of management in the future, it is recommended to obtain it from the background.
*The last two must not be written in js!
 * **/

/**
 * Upload file object
 * fileStats: File statistics
 * filePath: The address of the uploaded file
 * * */
var uploader = {
    fileList: [],
    fileStats: {
        totalFilesNum: 0,
        totalFilesSize: 0,
        uploadFinishedFilesNum: 0,
        curFileSize: 0,
    },
    filePath: "modelData/"
}; //Upload instance object
var Buffer = OSS.Buffer;
var OSS = OSS.Wrapper;
var STS = OSS.STS;


//Create a new client
//The front end uploads itself to oss, and does not go through the background to get relevant information. Only do the test, this can't be done in the project!

// var client = new OSS({
//     region: 'oss-cn-hangzhou',
//     accessKeyId: 'xxxx',
//     accessKeySecret: 'xxxx',
//     bucket: 'xxxxx'
// });
// https://help.aliyun.com/document_detail/63401.html?#h3--https-
//https 上传
// https://bbs.aliyun.com/read/282088.html


//client.options.endpoint.protocol = "https:" 
var progressBar = 0;
var progress = '';
var $wrap = $('#uploader'),
    // Picture container
    $queue = $('<ul class="filelist"></ul>').appendTo($wrap.find('.queueList')),
    $totalProgressbar = $("#totalProgressBar");
var FOLDER = 'folder';
var uploadType = ''; //Upload type



// =========================================================================================================================

/**
 * Method Two:
 *In actual production, use this.
 *Get authorization in the background, then generate the client
 */


var applyTokenDo = function () {
    var url = oss_url; //Request background to obtain authorization address url
    return $.ajax({
        url: url,
        async: false,
        success: function (result) {
            client = new OSS({
                region: 'oss-cn-hangzhou',
                accessKeyId: result.accessKeyId,
                accessKeySecret: result.accessKeySecret,
                bucket: 'obrisk'
            });
        }
    });
};


var progress = function (p) { //p percentage 0~1
    return function (done) {
        progressBar = (p * 100).toFixed(2) + '%';
        $totalProgressbar.css('width', progressBar)
            .html(progressBar);
        done();
    }
};

function getUploadFilePath() {
    return $("#uploadFilePath").val() || "/";
}


function OssUpload() {
    var _this = this;
    _this.init = function () {
        _this.initPage();
        _this.bindEvent();
    };
    _this.initPage = function () {
        // $("#statusBar").hide();
    };
}
var client;
OssUpload.prototype = {
    constructor: OssUpload,
    // Binding event
    bindEvent: function () {
        var _this = this;
        $("#chooseFile, #addBtn, #chooseFolder").click(function () {
            var $this = $(this);
            uploadType = $this.attr("data-type")
            console.log('bubtton clicked');
            if (uploadType == FOLDER) {
                document.getElementById("addDirectory").click();
            } else {
                document.getElementById("js-file").click();
            }
        });
        $('#js-file,#addDirectory').change(function (e) {
            var files = e.target.files;
            var curIndex = uploader.fileList.length; //The length of the file already in the plugin, append
            var length = files.length;
            var file = null;
            $('#uploader .placeholder').hide();
            $("#statusBar").css('display', 'flex');
            for (var i = 0; i < length; i++) {
                file = files[i];
                uploader.fileList[curIndex + i] = file;
                file.id = uploader.fileList[curIndex + i].id = "WU_LI_" + (curIndex + i + 1); //Add id to each file
                uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                _this.addFile(file); //Add to control view
            }
            uploader.fileStats.totalFilesNum = uploader.fileList.length;
        });

        $("#startUpload").click(function () {
            var length = uploader.fileStats.totalFilesNum;
            var filePath = getUploadFilePath(); //uploader.filePath;//Can adjust the upload location by yourself
            var file;
            for (var i = 0; i < length; i++) {
                file = uploader.fileList[i];
                _this.uploadFile(file, filePath);
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
                    uploader.fileList.splice(i, 1); //Delete a file from the file list
                    break;
                }
            }
            $li.remove();
        });
    },
    /***
     *  upload files
     * @param file files to be uploaded
     * @param filePath to which location to upload the file. According to the official statement is the key
     * oss is object storage, there is no path path concept, but personally think this can be better understood as a path
     */
    uploadFile: function (file, filePath) {

        var total = 0;
        if (uploadType != FOLDER) {
            filePath += file.name;
        } else { //Upload folder
            filePath = filePath + this.getParentDirName(file) + file.name;
        }
        applyTokenDo();
        client.multipartUpload(filePath, file, {
                progress: progress
            })
            .then(function (res) {
                $("#" + file.id).children(".success-span").addClass("success");
                uploader.fileStats.uploadFinishedFilesNum++; //Successfully uploaded + 1
                uploader.fileStats.curFileSize += file.size; //Currently uploaded file size
                /**
                 * There is a problem here:
                 * This is the size of the file in the successful callback, not real-time.
                 * Give a chestnut, you upload a 100M file, you have to wait until it is all uploaded, you know that it is uploaded, you don't know the progress.
                 * The uploaded process above looks like [0,1], and you have to calculate the size of the current file multiplied by the current progress to figure out how much the file has been uploaded.
                 *
                 */
                progressBar = (uploader.fileStats.curFileSize / uploader.fileStats.totalFilesSize).toFixed(2) * 100 + '%';

                if (total == uploader.fileStats.totalFilesNum) {
                    console.log("upload success!");
                    $("#startUpload").text('上传完成');
                }
                $totalProgressbar.css('width', progressBar)
                    .html(progressBar);
            });
    },

    /**
     * TODO is executed when a file is added, responsible for the creation of the view.
     * Baidu webuploader interface
     */
    addFile: function (file) {
        var $li = $('<li id="' + file.id + '">' +
                '<p class="title">' + file.name + '</p>' +
                '<p class="imgWrap"></p>' +
                '<p class="progress"><span></span></p><span class="success-span"></span>' +
                '</li>'),
            $btns = $('<div class="file-panel">' +
                '<span class="cancel">删除</span>' +
                '</div>').appendTo($li),
            $prgress = $li.find('p.progress span'),
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
//w.OssUpload = OssUpload;
//})(window)
var ossUpload = '';
$(function () {
    ossUpload = new OssUpload();
    ossUpload.init();
    $("#dl-button").click(function () {
        downloadFile();

    });
});