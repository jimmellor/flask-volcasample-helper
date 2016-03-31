from flask import Flask, request, redirect, url_for, render_template, jsonify
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

def get_file(root):
    """
    Return the first file in root
    """

    if not os.path.isdir(root):
        raise Exception("%s directory not found" % root)

    files = []
    for file in glob.glob("%s/*.*" % root):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return os.path.join(root,files[0])

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload/<slot_id>', methods=["POST"])
def upload(slot_id):
    """
    Upload a file
    """
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
    Play the syro-encoded file via the server audio jack
    """

    # Get the files.
    filename = get_file(os.path.join(APP_ROOT, UPLOAD_ROOT, slot_id))

    syroplay(filename)

    return ajax_response(True, filename)

@app.route("/status/<slot_id>")
def status(slot_id):
    """
    Check if there's a file in the slot
    """
    try:
        filename = get_file(os.path.join(APP_ROOT, UPLOAD_ROOT, slot_id))
        return ajax_response(True, filename)

    except Exception, e:
        return ajax_response(False, slot_id)

@app.context_processor
def utility_processor():
    def get_status(slot_id):
        try:
            get_file(os.path.join(APP_ROOT, UPLOAD_ROOT, str(slot_id)))
            return "ready"
        except Exception, e:
            return "empty"
    return dict(get_status=get_status)

def ajax_response(status, msg):
    status_code = 200 if status else 404

    message = {
            'status': status_code,
            'msg': msg,
    }
    resp = jsonify(message)
    resp.status_code = status_code

    return resp
