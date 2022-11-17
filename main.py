from flask import Flask, render_template
from config import AppConfig
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!Tunglete'


@app.route('/')
def home():
    return render_template('index.html')


socketIO = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

# don't remove these lines
import socket_io.socket_io_client
import routers.get_covid_infomation_router

host = AppConfig.host
port = AppConfig.port

if __name__ == '__main__':
    socketIO.run(app=app, debug=True, host=host, port=port)
