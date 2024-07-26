from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import colorama
from colorama import Fore, Style
# Setup the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Initialize Colorama
colorama.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    if 'text' in data:
        print(Fore.GREEN + "Received text: " + Style.RESET_ALL + data['text'])
        socketio.emit('update_text', {'text': data['text']})
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="No text provided"), 400

if __name__ == '__main__':
    socketio.run(app, port=5000)
