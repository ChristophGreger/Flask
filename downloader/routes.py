import unicodedata
from flask import render_template, flash, url_for, redirect, request, stream_with_context, Response, g, Blueprint
from pytube import YouTube, request as pytube_request
from pytube.exceptions import AgeRestrictedError
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from downloader import app, socketio


# convert unicode string to latin-1
def convert(s):
    r = ''
    for c in s:
        try:
            c.encode('latin-1')
        except UnicodeEncodeError:
            c = unicodedata.normalize('NFKD', c).encode('latin-1', 'ignore').decode('latin-1')
        r += c
    return r


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "GET":
        return render_template("home.html", video=None)

    if request.method == "POST":
        video_url = request.form.get("video_url")

        # User submitted a video URL
        if request.form.get("submit_video_url"):
            # Check if the URL is a valid YouTube URL
            if not check_video_url(video_url):
                flash("Invalid URL. Please make sure it is a valid YouTube URL.", category="danger")
                return redirect(url_for("home_page"))

            # Display video details
            video = YouTube(video_url)
            only_audio_streams = video.streams.filter(only_audio=True, type="audio")
            only_video_streams = video.streams.filter(only_video=True, type="video")
            video_streams = video.streams.filter(progressive=True)

            # Extract necessary information from the streams
            only_audio_streams_info = [{'itag': s.itag, 'abr': s.abr, 'mime_type': s.mime_type} for s in
                                       only_audio_streams]
            only_video_streams_info = [{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type} for s in
                                       only_video_streams]
            video_streams_info = [{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type} for s in
                                  video_streams]

            return render_template("home.html", video=video, video_url=video_url,
                                   only_audio_streams=only_audio_streams_info,
                                   only_video_streams=only_video_streams_info,
                                   video_streams=video_streams_info)
        else:
            flash("Something went wrong. Please try again.", category="danger")

    return render_template("home.html")


# Necessary for the after_request handling
download = Blueprint('simple_page', __name__)


@download.route("/download", methods=["GET"])
def download_video():
    video_url = request.args.get("video_url")
    g.sid = request.args.get("sid")
    try:
        # Evaluate the quality settings
        video_itag = request.args.get("quality_select")

        if not video_itag:
            flash("Please select a video format.", category="danger")
            return redirect(url_for("home_page"))

        # Download video
        url = YouTube(video_url)
        video = url.streams.get_by_itag(int(video_itag))

        response = Response(stream_with_context(pytube_request.stream(video.url)))
        response.headers['Content-Type'] = video.mime_type
        response.headers['Content-Disposition'] = 'attachment; filename=' + convert(video.title) + '.' + video.subtype
        response.headers['Content-Length'] = str(video.filesize)
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['ETag'] = str(video.filesize)
        response.headers['accept-ranges'] = 'bytes'
        return response
    except AgeRestrictedError:
        flash("Video is age restricted. Cannot download.", category="danger")
        return redirect(url_for("home_page"))


# Used for emiting the download button color change on download start
@download.after_request
def download_after_request(response):
    socketio.emit("downloadstarted", room=g.sid)
    return response


app.register_blueprint(download)


def check_video_url(video_url):
    return video_url.startswith('https://www.youtube.com/') or video_url.startswith('https://youtu.be/')
