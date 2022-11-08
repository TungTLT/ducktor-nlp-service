from flask import Flask, render_template
from flask_socketio import SocketIO, send
from conversation_model import chatbot as con_model
from disease_prediction_model_v2 import chatbot_disease_prediction_v2 as disease_prediction_model
from common import intents, socket_io_event
from socket_io_response import SocketIOResponse
from named_entity_recognition_model import nltk_ner as disease_info_model


app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!Tunglete'

socketIO = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')


@socketIO.on(socket_io_event.EVENT_CONNECT)
def connect():
    print("A user connected!")


@socketIO.on(socket_io_event.EVENT_DISCONNECT)
def disconnect():
    print("A user disconnected!")


# @socketIO.on(socket_io_event.EVENT_DISEASE_PREDICTION)
def handle_disease_prediction():
    response = SocketIOResponse(intents.DISEASE_PREDICTION, 'What is your disease symptoms?',
                                socket_io_event.EVENT_RECEIVE_SYMPTOMS)
    socketIO.send(response.as_dictionary())

    @socketIO.on(socket_io_event.EVENT_RECEIVE_SYMPTOMS)
    def handle_receive_symptoms(symptoms):
        # predict disease
        predict_disease = disease_prediction_model.predict_disease(symptoms)
        if predict_disease == '':
            predict_message = 'Sorry, I can\'t figure out your disease!'
        else:
            predict_message = f'You\'re maybe contracted to {predict_disease}'

        predict_response = SocketIOResponse(intents.DISEASE_PREDICTION, predict_message, '')
        socketIO.send(predict_response.as_dictionary())
        socketIO.sleep(1)

        # get information about that disease
        description = disease_prediction_model.get_disease_description(predict_disease)
        if description != '':
            description_response = SocketIOResponse(intents.DISEASE_PREDICTION, description, '')
            socketIO.send(description_response.as_dictionary())
            socketIO.sleep(1)

        precaution = disease_prediction_model.get_disease_precaution(predict_disease)
        if precaution:
            precaution_response = SocketIOResponse(intents.DISEASE_PREDICTION,
                                                   f'You should {precaution[0]}, {precaution[1]}, {precaution[2]} and {precaution[3]}',
                                                   '')
            socketIO.send(precaution_response.as_dictionary())
            socketIO.sleep(1)

        # ask if continue to predict
        socketIO.send(SocketIOResponse(intents.DISEASE_PREDICTION,
                                       'Do you want me to continue to predict your disease?',
                                       socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT).as_dictionary())

    @socketIO.on(socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT)
    def ask_for_continue_predict(message):
        if message == 'yes' or 'yes' in message or message == 'y':
            response = SocketIOResponse(intents.DISEASE_PREDICTION, 'What is your disease symptoms?',
                                        socket_io_event.EVENT_RECEIVE_SYMPTOMS)
            socketIO.send(response.as_dictionary())
        elif message == 'no' or 'no' in message or message == 'n':
            response = SocketIOResponse(intents.OPTIONS, 'What can I help you next?',
                                        socket_io_event.EVENT_MESSAGE)
            socketIO.send(response.as_dictionary())
        else:
            response = SocketIOResponse(intents.DISEASE_PREDICTION, 'Please answer yes or no!',
                                        socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT)
            socketIO.send(response.as_dictionary())


def handle_disease_information(user_input):
    searching_disease = disease_info_model.get_disease_tagger_words(user_input)
    # Calling API
    print(searching_disease)


@socketIO.on(socket_io_event.EVENT_MESSAGE)
def handle_receive_message(message):
    print(f"Receive: {message}")
    result = con_model.response(message)
    response = SocketIOResponse(result['intent'], result['content'], '')
    socketIO.send(response.as_dictionary())

    user_intent = result['intent']
    if user_intent == intents.DISEASE_PREDICTION:
        handle_disease_prediction()
    elif user_intent == intents.DISEASE_INFORMATION:
        handle_disease_information(message)


@app.route('/')
def home():
    return render_template('index.html')


host = '192.168.1.85'
port = 5004

if __name__ == '__main__':
    socketIO.run(app=app, debug=True, host=host, port=port)
