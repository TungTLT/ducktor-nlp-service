from flask import request

from conversation_model import chatbot as con_model
from disease_prediction_model import chatbot_disease_prediction_v2 as disease_prediction_model
from common import intents, socket_io_event
from socket_io.socket_io_response import SocketIOResponse
from named_entity_recognition_model import nltk_ner as disease_info_model
from get_disease_information.disease_information_client import GetDiseaseInformationClient
from __main__ import socketIO
from find_healthcare_location.healthcare_location_client import HealthCareLocationClient
import json
from common.suggest_message_provider import SuggestMessageProvider

sug_mes_provider = SuggestMessageProvider()
userId = ''


@socketIO.on(socket_io_event.EVENT_CONNECT)
def connect():
    global userId
    print("A user connected!")
    userId = request.sid
    message = "Hello! It's Ducktor. How can I help you?"
    suggest_messages = sug_mes_provider.get_conversation_messages()
    socketIO.send(SocketIOResponse(content=message, suggest_messages=suggest_messages).as_dictionary(), to=userId)


@socketIO.on(socket_io_event.EVENT_DISCONNECT)
def disconnect():
    print("A user disconnected!")


def handle_disease_prediction():
    global userId
    suggest_messages = sug_mes_provider.get_predict_disease_enter_symptoms_messages()
    response = SocketIOResponse('What is your disease symptoms?',
                                socket_io_event.EVENT_RECEIVE_SYMPTOMS, suggest_messages=suggest_messages)
    socketIO.send(response.as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_RECEIVE_SYMPTOMS)
    def handle_receive_symptoms(symptoms):
        global userId
        # predict disease
        predict_disease = disease_prediction_model.predict_disease(symptoms)
        if predict_disease == '':
            predict_message = 'Sorry, I can\'t figure out your disease!'
        else:
            predict_message = f'You\'re maybe contracted to {predict_disease}'

        predict_response = SocketIOResponse(predict_message)
        socketIO.send(predict_response.as_dictionary(), to=userId)
        socketIO.sleep(1)

        # get information about that disease
        description = disease_prediction_model.get_disease_description(predict_disease)
        if description != '':
            description_response = SocketIOResponse(description)
            socketIO.send(description_response.as_dictionary(), to=userId)
            socketIO.sleep(1)

        precaution = disease_prediction_model.get_disease_precaution(predict_disease)
        if precaution:
            precaution_response = SocketIOResponse(
                f'You should {precaution[0]}, {precaution[1]}, {precaution[2]} and {precaution[3]}')
            socketIO.send(precaution_response.as_dictionary(), to=userId)
            socketIO.sleep(1)

        # ask if continue to predict
        suggest_messages = sug_mes_provider.get_predict_disease_continue_messages()
        socketIO.send(SocketIOResponse('Do you want me to continue to predict your disease?',
                                       socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT,
                                       suggest_messages=suggest_messages).as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT)
    def ask_for_continue_predict(message: str):
        global userId
        message = message.lower()
        suggest_messages = sug_mes_provider.get_predict_disease_enter_symptoms_messages()
        if message == 'yes' or 'yes' in message or message == 'y':
            response = SocketIOResponse('What is your disease symptoms?',
                                        socket_io_event.EVENT_RECEIVE_SYMPTOMS,
                                        suggest_messages=suggest_messages)
            socketIO.send(response.as_dictionary(), to=userId)
        elif message == 'no' or 'no' in message or message == 'n':
            response = SocketIOResponse('What can I help you next?',
                                        socket_io_event.EVENT_MESSAGE)
            socketIO.send(response.as_dictionary(), to=userId)
        else:
            response = SocketIOResponse('Please answer yes or no!',
                                        socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT)
            socketIO.send(response.as_dictionary(), to=userId)


@socketIO.on(socket_io_event.EVENT_DISEASE_INFORMATION)
def handle_disease_information(user_input):
    global userId

    def handle_send_disease_info_message(disease_info):
        global userId
        if disease_info.is_not_valid():
            socketIO.send(SocketIOResponse('Sorry! I found nothing about that disease!',
                                           socket_io_event.EVENT_MESSAGE).as_dictionary(), to=userId)
            return

        socketIO.send(SocketIOResponse(f'I found these information about {response_list[0].name}').as_dictionary(),
                      to=userId)
        socketIO.sleep(1)

        name_message = f'{disease_info.name.upper()}'
        socketIO.send(SocketIOResponse(name_message).as_dictionary(), to=userId)
        socketIO.sleep(1)

        if disease_info.overview != '':
            overview_message = 'Overview: ' + disease_info.overview
            socketIO.send(SocketIOResponse(overview_message).as_dictionary(), to=userId)
            socketIO.sleep(1)

        if disease_info.diagnosis != '':
            diagnosis_message = 'Diagnosis: ' + disease_info.diagnosis
            socketIO.send(SocketIOResponse(diagnosis_message).as_dictionary(), to=userId)
            socketIO.sleep(1)

        if disease_info.prevention != '':
            prevention_message = 'Prevention: ' + disease_info.prevention
            socketIO.send(SocketIOResponse(prevention_message).as_dictionary(), to=userId)
            socketIO.sleep(1)

        if disease_info.treatment != '':
            treatment_message = 'Treatment: ' + disease_info.treatment
            socketIO.send(SocketIOResponse(treatment_message).as_dictionary(), to=userId)
            socketIO.sleep(1)

        socketIO.send(SocketIOResponse('That is all I know. What can I help you next?',
                                       socket_io_event.EVENT_MESSAGE).as_dictionary(), to=userId)

    searching_disease = disease_info_model.get_disease_tagger_words(user_input)
    socketIO.send(SocketIOResponse('Give me a second!').as_dictionary(), to=userId)
    client = GetDiseaseInformationClient()
    response_list = client.search_for_disease_information(searching_disease)
    response_len = len(response_list)
    max_selection = 5 if response_len > 5 else response_len

    if response_len > 1:
        for index, disease in enumerate(response_list):
            if index < max_selection:
                socketIO.send(SocketIOResponse(f'{index + 1}: {disease.name}', '').as_dictionary(), to=userId)
                socketIO.sleep(1)
            else:
                break

        socketIO.send(SocketIOResponse(f'Which disease do you want to know? (type 1 - {max_selection})',
                                       socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION).as_dictionary(), to=userId)
    elif response_len == 1:
        disease_info = client.get_disease_information(response_list[0].url)
        handle_send_disease_info_message(disease_info)

    else:
        socketIO.send(SocketIOResponse('Sorry! I found nothing about that disease!',
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
            socketIO.send(SocketIOResponse(f'Please type 1 - {max_selection}',
                                           socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION).as_dictionary(), to=userId)


def handle_healthcare_location(user_input: str):
    global userId
    message = 'Please! Wait for a few seconds!'
    socketIO.send(SocketIOResponse(message,
                                   socket_io_event.EVENT_ASK_FOR_USER_LOCATION,
                                   action_code='0002').as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_LOCATION_SENT)
    def handle_location_sent(user_location: str):
        global userId
        if isinstance(user_location, dict) and len(user_location) != 0:
            lat = user_location['lat']
            lon = user_location['lon']
            healthcare_loc_client = HealthCareLocationClient(latitude=lat, longitude=lon)
            healthcare_locations = healthcare_loc_client.search_nearby_healthcare_location(user_input)

            socketIO.send(SocketIOResponse('Here are the top 5 nearest locations!').as_dictionary(), to=userId)

            count = 0
            for location in healthcare_locations:
                count += 1
                response = SocketIOResponse(str(location),
                                            socket_io_event.EVENT_MESSAGE,
                                            action_code='0003',
                                            extra_data=json.dumps(location.toJSON())).as_dictionary()
                socketIO.send(response, to=userId)
                socketIO.sleep(1)
                if count == 5:
                    break

        else:
            message = 'Sorry! I can find without your location.'
            response = SocketIOResponse(message, next_event=socket_io_event.EVENT_MESSAGE)
            socketIO.send(response.as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_NO_LOCATION_SENT)
    def handle_no_location_sent():
        print('no location sent')


def handle_covid_information():
    global userId
    socketIO.sleep(1)
    message = 'You can tap this button to view information about COVID-19'
    socketIO.send(SocketIOResponse(message,
                                   socket_io_event.EVENT_MESSAGE,
                                   action_code="0001").as_dictionary(), to=userId)


@socketIO.on(socket_io_event.EVENT_MESSAGE)
def handle_receive_message(message):
    print(f"Receive: {message}")
    result = con_model.response(message)
    response = SocketIOResponse(result['content'])
    socketIO.send(response.as_dictionary())

    user_intent = result['intent']
    if user_intent == intents.DISEASE_PREDICTION:
        handle_disease_prediction()
    elif user_intent == intents.DISEASE_INFORMATION:
        handle_disease_information(message)
    elif user_intent == intents.HEALTHCARE_LOCATION:
        handle_healthcare_location(message)
    elif user_intent == intents.COVID_INFORMATION:
        handle_covid_information()
