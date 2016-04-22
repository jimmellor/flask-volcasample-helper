/******************************************************************************
 * HTML5 Multiple File Uploader Demo                                          *
 ******************************************************************************/

// Constants
var MAX_UPLOAD_FILE_SIZE = 1024*1024; // 1 MB
var UPLOAD_URL = "/upload/";
var PLAY_URL = "/play/";
var SYRO_PLAY_URL = "/syroupload/";
var NEXT_URL   = "/files/";

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];

$.event.special.tap.emitTapOnTaphold = false;


$(document).ready(function() {
    // Set up the drag/drop zone.
    initDropbox();

    // Set up the handler for the file input box.
    $("#file-picker").on("change", function() {
        handleFiles(this.files);
    });

    // Handle the submit button.
    $("#upload-button").on("click", function(e) {
        // If the user has JS disabled, none of this code is running but the
        // file multi-upload input box should still work. In this case they'll
        // just POST to the upload endpoint directly. However, with JS we'll do
        // the POST using ajax and then redirect them ourself when done.
        e.preventDefault();
        doUpload();
    })
});


function doUpload(slot) {
    $("#progress").show();
    var $progressBar   = $("#progress-bar");


    slot.addClass("uploading");

    // Collect the form data.
    fd = collectFormData();

    // Attach the files.
    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
        // Collect the other form data.
        fd.append("file", PENDING_FILES[i]);
    }

    // Inform the back-end that we're doing this over ajax.
    fd.append("__ajax", "true");

    var upload_slot_url = UPLOAD_URL + slot.attr('id');

    var xhr = $.ajax({
        xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener("progress", function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total    = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                        var str = "" + percent
                        var pad = "00"
                        var padded_percent = pad.substring(0, pad.length - str.length) + str
                    }

                    // Display the progress.
                    if (percent == 100) {
                        slot.text("OK");
                    } else {
                        slot.text(padded_percent);
                    }
                }, false)
            }

            return xhrobj;
            
        },
        url: upload_slot_url,
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd,
        success: function(data) {
            $progressBar.css({"width": "100%"});

            // How'd it go?
            if (data.status === "error") {
                // Uh-oh.
                window.alert(data.msg);
                $("#upload-form :input").removeAttr("disabled");
                return;
            }
            else {
                // Ok! Get the UUID.
                var uuid = data.msg;
                PENDING_FILES = [];
                // window.location = NEXT_URL + uuid;
            }
        },
    });
}




function collectFormData() {
    // Go through all the form fields and collect their names/values.
    var fd = new FormData();

    $("#upload-form :input").each(function() {
        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();

        // No name = no care.
        if (name === undefined) {
            return;
        }

        // Skip the file upload box for now.
        if (type === "file") {
            return;
        }

        // Checkboxes? Only add their value if they're checked.
        if (type === "checkbox" || type === "radio") {
            if (!$this.is(":checked")) {
                return;
            }
        }

        fd.append(name, value);
    });
    return fd;
}


function handleFiles(files) {
    // Add them to the pending files list.
    // for (var i = 0, ie = files.length; i < ie; i++) {
    //     PENDING_FILES.push(files[i]);
    // }
    PENDING_FILES[0] = files[0];
}

function syroPlaySample(slot) {
    syroPlayStart(slot);
    $.ajax({
        type: 'GET',
        url: SYRO_PLAY_URL + slot.attr('id'),
        success: function(data) {
            syroPlayStop(slot);
        }
    });
}

function syroPlayStart(slot) {
    slot.addClass("download");
    slot.text("DL");
}

function syroPlayStop(slot) {
    slot.removeClass("download");
    slot.text(slot.attr('id'));
}

function playSample(slot) {
    $.ajax({
        type: 'GET',
        url: PLAY_URL + slot.attr('id'),
        success: function(data) {
            playStart(slot);
            audioPlay(data.msg);
            playStop(slot);
        }
    });
}

function audioPlay(url) {
    audio = new Audio(url);
    audio.play();
}

function playStart(slot) {
    slot.addClass("play");
    slot.text("PL");
}

function playStop(slot) {
    slot.removeClass("play");
    slot.text(slot.attr('id'));
}



function initDropbox() {
    var $dropbox = $(".samplebox");

    // On drag enter...
    $dropbox.on("dragenter", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).addClass("hot");
        $(this).text("UL");
    });

    // On tap hold...
    $dropbox.on("taphold", function(e) {
        e.stopPropagation();
        e.preventDefault();
        syroPlaySample($(this));
    });
    
    $dropbox.on("dragleave", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).removeClass("hot");
        $(this).text($(this).attr('id'));
    });

    // On drag over...
    $dropbox.on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    // On click...
    $dropbox.on("tap", function(e) {
        e.stopPropagation();
        e.preventDefault();
        playSample($(this));
    });

    // On drop...
    $dropbox.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass("hot");
        $(this).addClass("active");

        // Get the files.
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);

        // Update the display to acknowledge the number of pending files.
        //$dropbox.text(PENDING_FILES.length + " files ready for upload!");
        doUpload($(this)); 
    });

    // If the files are dropped outside of the drop zone, the browser will
    // redirect to show the files in the window. To avoid that we can prevent
    // the 'drop' event on the document.
    function stopDefault(e) {
        e.stopPropagation();
        e.preventDefault();
    }
    $(document).on("dragenter", stopDefault);
    $(document).on("dragover", stopDefault);
    $(document).on("drop", stopDefault);
    $(document).on("taphold", stopDefault);
    $(document).on("dragleave", stopDefault);
}