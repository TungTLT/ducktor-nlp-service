from flask import Flask, render_template
from config import AppConfig
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

load_dotenv()
java_path = "C:/Program Files/Java/jdk-19/bin/java.exe"
os.environ['JAVAHOME'] = java_path

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!Tunglete'


@app.route('/')
def home():
    return render_template('index.html')


socketIO = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet', logger=True, engineio_logger=True)

# don't remove these lines
import socket_io.socket_io_event_handler
import routers.get_covid_infomation_router

host = os.getenv('HOST')
port = os.getenv('PORT')

if __name__ == '__main__':
    socketIO.run(app=app, host=host, port=port, debug=True)
