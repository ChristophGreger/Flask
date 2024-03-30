from flask import render_template, flash, url_for, redirect, request, send_file
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from io import BytesIO
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from downloader import app

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
            only_audio_streams_info = [{'itag': s.itag, 'abr': s.abr, 'mime_type': s.mime_type} for s in only_audio_streams]
            only_video_streams_info = [{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type} for s in only_video_streams]
            video_streams_info = [{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type} for s in video_streams]

            return render_template("home.html", video=video, video_url=video_url,
                                   only_audio_streams=only_audio_streams_info,
                                   only_video_streams=only_video_streams_info,
                                   video_streams=video_streams_info)

        # User clicked on download button
        elif request.form.get("download_video"):
            try:
                # Evaluate the quality settings
                video_itag = request.form.get("quality_select")

                if not video_itag:
                    flash("Please select a video format.", category="danger")
                    return redirect(url_for("home_page"))

                # Download video
                buffer = BytesIO()
                url = YouTube(video_url)
                video = url.streams.get_by_itag(int(video_itag))
                video.stream_to_buffer(buffer)
                buffer.seek(0)
                return send_file(buffer, as_attachment=True, download_name=video.title, mimetype=video.mime_type)
            except AgeRestrictedError:
                flash("Video is age restricted. Cannot download.", category="danger")
                return redirect(url_for("home_page"))
        else:
            flash("Something went wrong. Please try again.", category="danger")

    return render_template("home.html")


def check_video_url(video_url):
    return video_url.startswith('https://www.youtube.com/') or video_url.startswith('https://youtu.be/')
