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
};

//Upload instance object
var Buffer = OSS.Buffer;
var OSS = OSS.Wrapper;
var STS = OSS.STS;
var FileMaxSize = 13000000
var TotalFilesMaxSize = 8
var images; //holds all uploaded images as a string 
var client;
var ossUpload = '';
OssUpload.prototype = {
    constructor: OssUpload,
    // Binding event
    bindEvent: function () {
        var _this = this;

        $("#chooseFile, #addBtn").click(function () {
            document.getElementById("image-file").click();
        });

        $('input[type="file"]').change(function (e) {
            //console.log(e)
            var files = e.target.files;
            var curIndex = uploader.fileList.length; //The length of the file already in the plugin, append
            var NumberOfSelectedFiles = files.length;
            //console.log('total files selected ' + NumberOfSelectedFiles);
            var file = null;
            $('#uploader .placeholder').hide();
            $("#statusBar").css('display', 'flex');
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
            if ($("#id_title").val() == '' || $("#id_details").val() == '' ||
                $("#id_located_area").val() == '' || $("#id_tags").val() == '') {
                event.preventDefault();
                bootbox.alert("Please fill in all of the information before uploading the images!");
            } else if (uploader.fileStats.totalFilesNum == 0) {
                event.preventDefault();
                bootbox.alert("Please select images to upload!");
                $(".start-uploader").css('display', 'block');

            } else {
                var length = uploader.fileStats.totalFilesNum;
                var file;
                $(".start-uploader").css('display', 'none');
                $totalProgressbar.css('width', '40%')
                    .html('Upload Started please be patient');
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

        var total = 0;

        applyTokenDo();

        //make sure we get the sts token
        if (client !== undefined) {

            const upload = async () => {
                try {
                    const results = await client.multipartUpload(filename, file, {
                            progress: progress
                        })
                        .then(function (res) {
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
                        });
                    return results;
                } catch (e) {
                    bootbox.alert("Oops! an error occured during the image upload, \
                    Please try again later or contact us via support@obrisk.com")
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
    $.ajax({
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
        },
        error: function (e) {
            bootbox.alert('Oops! an error occured during the upload, Please try again later or contact us via support@obrisk.com')
            //console.log(e)
        }
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
    return "classifieds/" + user + '/' + slugify($('#id_title').val()) +
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


    $(".create").click(function (event) {
        if (!images) {
            event.preventDefault();
            bootbox.alert("Please upload at least one image for your advertisement!");
        } else {
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