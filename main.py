from flask import Flask, render_template
from flask_socketio import SocketIO, send
from chatbot_conversation_model import chatbot as con_model
from chatbot_disease_prediction_model_v2 import chatbot_disease_prediction_v2 as dis_pre_model
from common import intents, socket_io_event
from socket_io_response import SocketIOResponse

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!Tunglete'

socketIO = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')


@socketIO.on(socket_io_event.EVENT_CONNECT)
def connect():
    print("A user connected!")


@socketIO.on(socket_io_event.EVENT_DISCONNECT)
def disconnect():
    print("A user disconnected!")


@socketIO.on(socket_io_event.EVENT_DISEASE_PREDICTION)
def handle_disease_prediction():
    response = SocketIOResponse(intents.DISEASE_PREDICTION, 'What is your disease symptoms?',
                                socket_io_event.EVENT_RECEIVE_SYMPTOMS)
    socketIO.send(response.as_dictionary())

    @socketIO.on(socket_io_event.EVENT_RECEIVE_SYMPTOMS)
    def handle_receive_symptoms(symptoms):
        predict_disease = dis_pre_model.predict_disease(symptoms)
        predict_response = SocketIOResponse(intents.DISEASE_PREDICTION, predict_disease, '')
        socketIO.send(predict_response.as_dictionary())


@socketIO.on(socket_io_event.EVENT_MESSAGE)
def handle_receive_message(message):
    print(f"Receive: {message}")
    result = con_model.response(message)
    response = SocketIOResponse(result['intent'], result['content'], '')
    socketIO.send(response.as_dictionary())

    user_intent = result['intent']
    if user_intent == intents.DISEASE_PREDICTION:
        handle_disease_prediction()


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    socketIO.run(app=app, debug=True, host='192.168.1.85', port=5004)
