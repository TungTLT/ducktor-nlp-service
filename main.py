from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!Tunglete'

socketIO = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')


@socketIO.on('connect')
def connect():
    print("A user connected!")


@socketIO.on('disconnect')
def disconnect():
    print("A user disconnected!")


@socketIO.on('message')
def handle_receive_message(message):
    print(f"Receive: {message}")
    socketIO.send("Server received " + message)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    socketIO.run(app=app, debug=True, host='192.168.1.85', port=5004)
