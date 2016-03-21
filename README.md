# Korg Volca Sample Helper

##About

Simple Korg Volca Sample librarian. Run it on a computer attached to the Volca Sample 'sync in' socket. Drag samples to the slots to upload, click to audition the file, long-click to download to the sampler.

Uses the [Korg Syro example app](http://korginc.github.io/volcasample/) to encode the audio to Volca Sample-compatible audio.

##Installation

Clone the repo somewhere sensible. Change to the flask-volcasampler-helper directory.

Install the requirements:
```
pip -r requirements.txt
```

Note: Depending on your system you may need to alter the playback device and the version of the Syro example app. Modify af.py to suit.

##Usage

Run the app:
```
python runserver.py
```

You should see:
```
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Success! point your browser at that address and you'll see the UI.

