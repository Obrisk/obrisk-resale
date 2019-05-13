/**
 * Enable upload when title has been entered 
 */




/**
 * Upload file object
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
}; //Upload instance object
var Buffer = OSS.Buffer;
var OSS = OSS.Wrapper;
var STS = OSS.STS;

//client.options.endpoint.protocol = "https:" 
var progressBar = 0;
var progress = '';
var $wrap = $('#uploader'),
    // Picture container
    $queue = $('<ul class="filelist"></ul>').appendTo($wrap.find('.queueList')),
    $totalProgressbar = $("#totalProgressBar");
var FOLDER = 'folder';
var uploadType = ''; //Upload type


/**
 * get sts token
 */
var applyTokenDo = function () {
    var url = oss_url; //Request background to obtain authorization address url
    return $.ajax({
        url: url,
        async: false,
        success: function (result) {
            client = new OSS({
                region: result.region,
                accessKeyId: result.accessKeyId,
                accessKeySecret: result.accessKeySecret,
                stsToken: result.SecurityToken,
                bucket: result.bucket
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

    };
}


/**
 * generate file name using uuid
 *
 * @return  {string}  
 */

function genKey() {
    return "classifieds/" + user + '/' + slugify($('#id_title').val()) +
        '/' + 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
}

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
var client;
var images;

OssUpload.prototype = {
    constructor: OssUpload,
    // Binding event
    bindEvent: function () {
        var _this = this;
        $('#id_title').on("blur", function () { 
            $("#chooseFile, #addBtn").click(function () {
                var $this = $(this);
                uploadType = $this.attr("data-type")
                document.getElementById("image-file").click();
            });
            $('#image-file').change(function (e) {
                var files = e.target.files;
                var curIndex = uploader.fileList.length; //The length of the file already in the plugin, append
                var length = files.length;
                var file = null;
                $('#uploader .placeholder').hide();
                $("#statusBar").css('display', 'flex');
                for (var i = 0; i < length; i++) {
                    file = files[i];
                    uploader.fileList[curIndex + i] = file;
                    file.id = uploader.fileList[curIndex + i].id = "image" + (curIndex + i + 1); //Add id to each file
                    uploader.fileStats.totalFilesSize += file.size; //Statistical file size
                    _this.addFile(file); //Add to control view
                }
                uploader.fileStats.totalFilesNum = uploader.fileList.length;
            });

            $("#startUpload").click(function (event) {
                if ($("#id_title").val() == '' || $("#id_details").val()== ''||
                    $("#id_located_area").val() == '' || $("#id_tags").val() == '' )
                {
                    event.preventDefault();
                    alert("Please fill in all of the information before uploading the images!");
                }
                else {
                    var length = uploader.fileStats.totalFilesNum;
                    var file;
                    $(".start-uploader").css('display', 'none');
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
                        uploader.fileList.splice(i, 1); //Delete a file from the file list
                        break;
                    }
                }
                $li.remove();
            });
        });
    },

    /***
     *  upload files
     * @param file files to be uploaded
     * @param filename to which location to upload the file. According to the official statement is the key
     * oss is object storage, there is no path path concept, but personally think this can be better understood as a path
     */
    uploadFile: function (file, filename) {

        var total = 0;
        applyTokenDo();
        client.multipartUpload(filename, file, {
                progress: progress
            })
            .then(function (res) {

                $("#" + file.id).children(".success-span").addClass("success");
                $("#" + file.id).children(".file-panel").hide();
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
                    $("#startUpload").text('Uploaded completed');
                }
                $totalProgressbar.css('width', progressBar)
                    .html(progressBar);

                images += ',' + res.name;
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
var ossUpload = '';
$(function () {
    ossUpload = new OssUpload();
    ossUpload.init();
    $("#dl-button").click(function () {
        downloadFile();

    });

   
    $(".create").click(function (event) {
        if (!images) {
            event.preventDefault();
            alert("Please upload at least one image for your advertisement!")
        }
        else {
            $("input[name='status']").val("A");
            $("#id_images").val(images);
            $("#classified-form").submit();
        }
    }); 
    
    $(".draft").click(function () {
        $("input[name='status']").val("E");
        $("#classified-form").submit();
    });
    
});