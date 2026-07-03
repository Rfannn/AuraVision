import logging
import os
import sys
from functools import wraps
from typing import Any

import pyaudio
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS

from config import (
    SECRET_KEY,
    AUTH_TOKEN,
    FLASK_HOST,
    FLASK_PORT,
    FLASK_DEBUG,
    LOG_LEVEL,
    BASE_DIR,
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.ERROR),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("auravision")

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = SECRET_KEY
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

detected_lang: str = "en"


def require_token(f: Any) -> Any:
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if AUTH_TOKEN:
            token = request.headers.get("X-Auth-Token", "")
            if token != AUTH_TOKEN:
                return jsonify(success=False, error="Unauthorized"), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index() -> Any:
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon() -> Any:
    return send_from_directory(app.static_folder, "favicon.svg", mimetype="image/svg+xml")


@app.route("/mics")
def list_mics() -> Any:
    pa = pyaudio.PyAudio()
    mics = []
    default_idx = -1
    try:
        default_info = pa.get_default_input_device_info()
        default_idx = default_info["index"]
    except OSError:
        pass
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            mics.append({
                "index": i,
                "name": info["name"],
                "channels": int(info["maxInputChannels"]),
                "rate": int(info["defaultSampleRate"]),
            })
    pa.terminate()
    return jsonify(mics=mics, default=default_idx)


@app.route("/update", methods=["POST"])
@require_token
def update() -> Any:
    global detected_lang

    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify(success=False, error="No text provided"), 400

    text = data["text"].strip()
    lang = data.get("lang", "en")
    partial = data.get("partial", False)

    if not text:
        return jsonify(success=False, error="Empty text"), 400

    if lang != detected_lang:
        detected_lang = lang
        socketio.emit("lang_change", {"lang": lang})

    logger.info("[%s] %s%s", lang, text, " (partial)" if partial else "")

    event = "partial_text" if partial else "update_text"
    socketio.emit(event, {"text": text, "lang": lang})
    return jsonify(success=True)


@app.route("/health")
def health() -> Any:
    return jsonify(status="ok")


@socketio.on("connect")
def on_connect() -> None:
    logger.debug("Client connected")
    socketio.emit("lang_change", {"lang": detected_lang})


@socketio.on("disconnect")
def on_disconnect() -> None:
    logger.debug("Client disconnected")


if __name__ == "__main__":
    socketio.run(app, host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
