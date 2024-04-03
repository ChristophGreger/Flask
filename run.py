from downloader import app, socketio

if __name__ == "__main__":
    app.run(debug=True)
    socketio.run(app, debug=True)