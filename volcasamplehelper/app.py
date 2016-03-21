from flask import Flask, request, redirect, url_for, render_template
import os
import shutil
import json
import glob
from flask_bootstrap import Bootstrap
from af import afplay, syroconvert, syroplay

app = Flask(__name__)
Bootstrap(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_ROOT = "static/uploads"

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload/<slot_id>', methods=["POST"])
def upload(slot_id):
    """Handle the upload of a file."""
    form = request.form

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = os.path.join(APP_ROOT, UPLOAD_ROOT, slot_id) 

    if os.path.isdir(target):
        shutil.rmtree(target)

    os.mkdir(target)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        upload.save(destination)

    # convert the file to syro format
    syroconvert(os.path.join(APP_ROOT, destination), slot_id)

    return ajax_response(True, slot_id)


@app.route("/play/<slot_id>")
def play(slot_id):
    """
    Returns the path of the sound file for the browser to play
    """
    # Get the files.
    web_root = os.path.join(UPLOAD_ROOT, slot_id)
    root = os.path.join(APP_ROOT, web_root)

    files = []
    for file in glob.glob("%s/*.*" % root):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    filename = os.path.join(web_root,files[0])

    return ajax_response(True, filename)

@app.route("/syroupload/<slot_id>")
def syroupload(slot_id):

    """
    Plays the syro-encoded file via the server audio jack
    """

    # Get the files.
    root = os.path.join(APP_ROOT, UPLOAD_ROOT, slot_id)

    if not os.path.isdir(root):
        return "Error: Slot directory not found!"

    files = []
    for file in glob.glob("%s/*.*" % root):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    filename = os.path.join(root,files[0])

    print filename

    syroplay(filename)

    return ajax_response(True, filename)

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
