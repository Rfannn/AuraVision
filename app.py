from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import colorama
from colorama import Fore, Style

from config import SECRET_KEY, FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

colorama.init()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update", methods=["POST"])
def update():
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify(success=False, error="No text provided"), 400

    text = data["text"].strip()
    if not text:
        return jsonify(success=False, error="Empty text"), 400

    print(Fore.GREEN + "Received text: " + Style.RESET_ALL + text)
    socketio.emit("update_text", {"text": text})
    return jsonify(success=True)


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    socketio.run(app, host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
