from flask import Flask, render_template, jsonify, abort
from flask_socketio import SocketIO
from conversation_model import chatbot as con_model
from disease_prediction_model import chatbot_disease_prediction_v2 as disease_prediction_model
from common import intents, socket_io_event
from socket_io_response import SocketIOResponse
from named_entity_recognition_model import nltk_ner as disease_info_model
from get_disease_information.disease_information_client import GetDiseaseInformationClient
from get_covid_information.covid_information_client import CovidAPI

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


@socketIO.on(socket_io_event.EVENT_DISEASE_INFORMATION)
def handle_disease_information(user_input):
    def handle_send_disease_info_message(disease_info):
        if disease_info.is_not_valid():
            socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                           'Sorry! I found nothing about that disease!',
                                           socket_io_event.EVENT_MESSAGE).as_dictionary())
            return

        socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                       f'I found these information about {response_list[0].name}',
                                       '').as_dictionary())
        socketIO.sleep(1)

        name_message = f'{disease_info.name.upper()}'
        socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                       name_message,
                                       '').as_dictionary())
        socketIO.sleep(1)

        if disease_info.overview != '':
            overview_message = 'Overview: ' + disease_info.overview
            socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                           overview_message,
                                           '').as_dictionary())
            socketIO.sleep(1)

        if disease_info.diagnosis != '':
            diagnosis_message = 'Diagnosis: ' + disease_info.diagnosis
            socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                           diagnosis_message,
                                           '').as_dictionary())
            socketIO.sleep(1)

        if disease_info.prevention != '':
            prevention_message = 'Prevention: ' + disease_info.prevention
            socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                           prevention_message,
                                           '').as_dictionary())
            socketIO.sleep(1)

        if disease_info.treatment != '':
            treatment_message = 'Treatment: ' + disease_info.treatment
            socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                           treatment_message,
                                           '').as_dictionary())
            socketIO.sleep(1)

        socketIO.send(SocketIOResponse(intents.OPTIONS,
                                       'That is all I know. What can I help you next?',
                                       socket_io_event.EVENT_MESSAGE).as_dictionary())

    searching_disease = disease_info_model.get_disease_tagger_words(user_input)
    socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION, 'Give me a second!', '').as_dictionary())
    client = GetDiseaseInformationClient()
    response_list = client.search_for_disease_information(searching_disease)
    response_len = len(response_list)
    max_selection = 5 if response_len > 5 else response_len

    if response_len > 1:
        for index, disease in enumerate(response_list):
            if index < max_selection:
                socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                               f'{index + 1}: {disease.name}', '').as_dictionary())
                socketIO.sleep(1)
            else:
                break

        socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                       f'Which disease do you want to know? (type 1 - {max_selection})',
                                       socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION).as_dictionary())
    elif response_len == 1:
        disease_info = client.get_disease_information(response_list[0].url)
        handle_send_disease_info_message(disease_info)

    else:
        socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                       'Sorry! I found nothing about that disease!',
                                       socket_io_event.EVENT_MESSAGE).as_dictionary())

    @socketIO.on(socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION)
    def ask_for_selection(user_selection: str):
        try:
            user_number_selection = int(user_selection)
            if 1 <= user_number_selection <= max_selection:
                disease_info = client.get_disease_information(response_list[user_number_selection - 1].url)
                handle_send_disease_info_message(disease_info)
            else:
                raise ValueError
        except ValueError:
            socketIO.send(SocketIOResponse(intents.DISEASE_INFORMATION,
                                           f'Please type 1 - {max_selection}',
                                           socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION).as_dictionary())


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


@app.route('/covid/global/get-today-infected')
def global_get_infect_today():
    result = CovidAPI().get_infected_in_day_global()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/global/get-total-infected')
def global_get_infect_total():
    result = CovidAPI().get_total_infected_global()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/global/get-today-death')
def global_get_death_today():
    result = CovidAPI().get_death_in_day_global()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/global/get-total-death')
def global_get_death_total():
    result = CovidAPI().get_total_death_global()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/global/get-today-recovered')
def global_get_recovered_today():
    result = CovidAPI().get_recover_in_day_global()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/global/get-total-recovered')
def global_get_recovered_total():
    result = CovidAPI().get_total_recover_global()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-today-infected')
def vn_get_infected_today():
    result = CovidAPI().get_infected_in_day_vietnam()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-total-infected')
def vn_get_infected_total():
    result = CovidAPI().get_total_infected_vietnam()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-today-death')
def vn_get_death_today():
    result = CovidAPI().get_death_in_day_vietnam()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-total-death')
def vn_get_death_total():
    result = CovidAPI().get_total_death_vietnam()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-today-recovered')
def vn_get_recovered_today():
    result = CovidAPI().get_recover_in_day_vietnam()
    if result is None:
        abort(404)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-total-recovered')
def vn_get_recovered_total():
    result = CovidAPI().get_total_recover_vietnam()
    if result is None:
        abort(404)
    return jsonify(result), 200


host = '192.168.1.85'
port = 5004

if __name__ == '__main__':
    socketIO.run(app=app, debug=True, host=host, port=port)
