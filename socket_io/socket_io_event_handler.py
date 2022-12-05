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


def send_in_progress_messages(value):
    if not value:
        socketIO.sleep(1)

    socketIO.emit('in_progress', value)


def send_content_for_voice(content):
    socketIO.emit('content_for_voice', content)
    socketIO.sleep(1)


@socketIO.on(socket_io_event.EVENT_CONNECT)
def connect():
    global userId
    print("A user connected!")
    userId = request.sid

    message = "Hello! It's Ducktor. How can I help you?"
    send_content_for_voice(message)
    suggest_mes = sug_mes_provider.get_conversation_messages()
    socketIO.send(SocketIOResponse(content=message, suggest_messages=suggest_mes).as_dictionary(),
                  to=userId)


@socketIO.on(socket_io_event.EVENT_DISCONNECT)
def disconnect():
    print("A user disconnected!")


def handle_disease_prediction():
    global userId
    send_in_progress_messages(True)

    suggest_messages = sug_mes_provider.get_predict_disease_enter_symptoms_messages()
    message = 'What is your disease symptoms?'

    send_content_for_voice(message)
    response = SocketIOResponse(message, socket_io_event.EVENT_RECEIVE_SYMPTOMS, suggest_messages=suggest_messages)

    send_in_progress_messages(False)
    socketIO.send(response.as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_RECEIVE_SYMPTOMS)
    def handle_receive_symptoms(symptoms):
        global userId

        predict_disease = disease_prediction_model.predict_disease(symptoms)
        description = disease_prediction_model.get_disease_description(predict_disease)
        precaution = disease_prediction_model.get_disease_precaution(predict_disease)

        if predict_disease == '':
            predict_message = 'Sorry, I can\'t figure out your disease!'
        else:
            predict_message = f'You\'re maybe contracted to {predict_disease}'
        precaution_message = f'You should {precaution[0]}, {precaution[1]}, {precaution[2]} and {precaution[3]}'
        continue_message = 'Do you want me to continue to predict your disease?'

        voice_content = f'{predict_message}. {description}. {precaution_message}. {continue_message}'
        send_content_for_voice(voice_content)

        # predict disease
        send_in_progress_messages(True)
        predict_response = SocketIOResponse(predict_message)
        socketIO.send(predict_response.as_dictionary(), to=userId)
        socketIO.sleep(1)

        # get information about that disease
        if description != '':
            description_response = SocketIOResponse(description)
            socketIO.send(description_response.as_dictionary(), to=userId)
            socketIO.sleep(1)

        if precaution:
            precaution_response = SocketIOResponse(predict_message)
            socketIO.send(precaution_response.as_dictionary(), to=userId)
            socketIO.sleep(1)

        # ask if continue to predict
        send_in_progress_messages(False)
        suggest_messages = sug_mes_provider.get_predict_disease_continue_messages()
        socketIO.send(SocketIOResponse(continue_message,
                                       socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT,
                                       suggest_messages=suggest_messages).as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT)
    def ask_for_continue_predict(message: str):
        global userId

        message = message.lower()
        send_in_progress_messages(True)
        if message == 'yes' or 'yes' in message or message == 'y':
            suggest_messages = sug_mes_provider.get_predict_disease_enter_symptoms_messages()
            response = SocketIOResponse('What is your disease symptoms?',
                                        socket_io_event.EVENT_RECEIVE_SYMPTOMS,
                                        suggest_messages=suggest_messages)
            send_content_for_voice('What is your disease symptoms?')
            send_in_progress_messages(False)
            socketIO.send(response.as_dictionary(), to=userId)

        elif message == 'no' or 'no' in message or message == 'n':
            sug_mes = sug_mes_provider.get_conversation_messages()
            response = SocketIOResponse('What can I help you next?',
                                        socket_io_event.EVENT_MESSAGE, suggest_messages=sug_mes)
            send_content_for_voice('What can I help you next?')
            send_in_progress_messages(False)
            socketIO.send(response.as_dictionary(), to=userId)

        else:
            response = SocketIOResponse('Please answer yes or no!',
                                        socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT,
                                        suggest_messages=['Yes', "No"])
            send_content_for_voice('Please answer yes or no!')
            send_in_progress_messages(False)
            socketIO.send(response.as_dictionary(), to=userId)


@socketIO.on(socket_io_event.EVENT_DISEASE_INFORMATION)
def handle_disease_information(user_input):
    global userId

    def handle_send_disease_info_message(disease_info):
        global userId
        if disease_info.is_not_valid():
            message = 'Unluckily! I found nothing about that disease.'
            send_content_for_voice(message)
            send_in_progress_messages(False)
            sug_mes = sug_mes_provider.get_conversation_messages()
            socketIO.send(SocketIOResponse(message,
                                           socket_io_event.EVENT_MESSAGE,
                                           suggest_messages=sug_mes).as_dictionary(), to=userId)
            return

        intro_message = f'I found these information about {disease_info.name}'
        name_message = f'{disease_info.name.upper()}'
        voice_content = f'{intro_message}. {name_message}.'

        if disease_info.overview != '':
            voice_content += 'Overview: ' + disease_info.overview + '.'
        if disease_info.diagnosis != '':
            voice_content += 'Diagnosis: ' + disease_info.diagnosis + '.'
        if disease_info.prevention != '':
            voice_content += 'Prevention: ' + disease_info.prevention + '.'
        if disease_info.treatment != '':
            voice_content += 'Treatment: ' + disease_info.treatment + '.'
        voice_content += 'That is all I know. What can I help you next?'
        send_content_for_voice(voice_content)

        socketIO.send(SocketIOResponse(intro_message).as_dictionary(), to=userId)
        socketIO.sleep(1)

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

        send_in_progress_messages(False)
        sug_mes = sug_mes_provider.get_conversation_messages()
        socketIO.send(SocketIOResponse('That is all I know. What can I help you next?',
                                       socket_io_event.EVENT_MESSAGE,
                                       suggest_messages=sug_mes).as_dictionary(), to=userId)

    send_in_progress_messages(True)
    searching_disease = disease_info_model.get_disease_tagger_words(user_input)

    client = GetDiseaseInformationClient()
    response_list = client.search_for_disease_information(searching_disease)
    response_len = len(response_list)
    max_selection = 5 if response_len > 5 else response_len

    if response_len > 1:
        voice_content = ''
        for index, disease in enumerate(response_list):
            if index < max_selection:
                voice_content += f'{index + 1}: {disease.name}.'
                socketIO.send(SocketIOResponse(f'{index + 1}: {disease.name}', '').as_dictionary(), to=userId)
                socketIO.sleep(1)
            else:
                break

        voice_content += f'Which disease do you want to know? (type 1 - {max_selection})'
        send_content_for_voice(voice_content)
        send_in_progress_messages(False)
        socketIO.send(SocketIOResponse(f'Which disease do you want to know? (type 1 - {max_selection})',
                                       socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION).as_dictionary(), to=userId)

    elif response_len == 1:
        disease_info = client.get_disease_information(response_list[0].url)
        handle_send_disease_info_message(disease_info)

    else:
        send_in_progress_messages(False)
        sug_mes = sug_mes_provider.get_conversation_messages()
        send_content_for_voice('Sorry! I found nothing about that disease.')
        socketIO.send(SocketIOResponse('Sorry! I found nothing about that disease.',
                                       socket_io_event.EVENT_MESSAGE,
                                       suggest_messages=sug_mes).as_dictionary())

    @socketIO.on(socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION)
    def ask_for_selection(user_selection: str):
        try:
            user_number_selection = int(user_selection)
            if 1 <= user_number_selection <= max_selection:
                send_in_progress_messages(True)
                disease_info = client.get_disease_information(response_list[user_number_selection - 1].url)
                handle_send_disease_info_message(disease_info)
            else:
                raise ValueError
        except ValueError:
            send_content_for_voice(f'Please type 1 - {max_selection}')
            send_in_progress_messages(False)
            socketIO.send(SocketIOResponse(f'Please type 1 - {max_selection}',
                                           socket_io_event.EVENT_ASK_FOR_DISEASE_SELECTION).as_dictionary(), to=userId)


def handle_healthcare_location(user_input: str):
    global userId
    send_in_progress_messages(True)
    message = 'Please, wait for a few seconds!'
    send_content_for_voice(message)
    socketIO.send(SocketIOResponse(message, action_code='0002').as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_LOCATION_SENT)
    def handle_location_sent(user_location: str):
        global userId

        send_in_progress_messages(True)
        if isinstance(user_location, dict) and len(user_location) != 0:
            lat = user_location['lat']
            lon = user_location['lon']
            healthcare_loc_client = HealthCareLocationClient(latitude=lat, longitude=lon)
            healthcare_locations = healthcare_loc_client.search_nearby_healthcare_location(user_input)
            if len(healthcare_locations) == 0:
                send_in_progress_messages(False)
                message = 'Sorry! I can\'t find anything, please try again.'
                send_content_for_voice(message)
                socketIO.send(SocketIOResponse(message, next_event=socket_io_event.EVENT_MESSAGE).as_dictionary(),
                              to=userId)
                return

            send_content_for_voice('Here are the top 5 nearest locations!')
            socketIO.send(SocketIOResponse('Here are the top 5 nearest locations!').as_dictionary(), to=userId)

            for location in healthcare_locations:
                extra_data = json.dumps(location.to_json())
                response = SocketIOResponse(str(location),
                                            socket_io_event.EVENT_MESSAGE,
                                            action_code='0003',
                                            extra_data=extra_data).as_dictionary()
                socketIO.send(response, to=userId)
                socketIO.sleep(1)

            send_in_progress_messages(False)

        else:
            send_in_progress_messages(False)
            message = 'Sorry! I can\'t find without your location.'
            send_content_for_voice(message)
            sug_mes = sug_mes_provider.get_conversation_messages()
            response = SocketIOResponse(message, next_event=socket_io_event.EVENT_MESSAGE,
                                        suggest_messages=sug_mes)
            socketIO.send(response.as_dictionary(), to=userId)

    @socketIO.on(socket_io_event.EVENT_NO_LOCATION_SENT)
    def handle_no_location_sent():
        print('no location sent')
        send_in_progress_messages(True)
        send_in_progress_messages(False)
        send_content_for_voice('Sorry! I can\'t find without your location.Ducktor need your location permission. '
                               'Please grant it then try again!')
        message = 'Sorry! I can\'t find without your location.'
        response = SocketIOResponse(message)
        socketIO.send(response.as_dictionary(), to=userId)

        message = 'Ducktor need your location permission. Please grant it then try again!'
        sug_mes = sug_mes_provider.get_conversation_messages()
        response = SocketIOResponse(message, next_event=socket_io_event.EVENT_MESSAGE,
                                    suggest_messages=sug_mes, action_code='0004')
        socketIO.send(response.as_dictionary(), to=userId)


def handle_covid_information():
    global userId
    send_in_progress_messages(True)
    send_in_progress_messages(False)
    message = 'You can tap this button to view information about COVID-19'
    send_content_for_voice(message)
    sug_mes = sug_mes_provider.get_conversation_messages()
    socketIO.send(SocketIOResponse(message,
                                   socket_io_event.EVENT_MESSAGE,
                                   action_code="0001",
                                   suggest_messages=sug_mes).as_dictionary(), to=userId)


@socketIO.on(socket_io_event.EVENT_MESSAGE)
def handle_receive_message(message):
    print(f"Receive: {message}")
    send_in_progress_messages(True)
    result = con_model.response(message)
    sug_mes = sug_mes_provider.get_conversation_messages()
    response = SocketIOResponse(result['content'], suggest_messages=sug_mes)
    send_in_progress_messages(False)
    send_content_for_voice(result['content'])
    socketIO.send(response.as_dictionary())
    socketIO.sleep(1)

    user_intent = result['intent']
    if user_intent == intents.DISEASE_PREDICTION:
        handle_disease_prediction()
    elif user_intent == intents.DISEASE_INFORMATION:
        handle_disease_information(message)
    elif user_intent == intents.HEALTHCARE_LOCATION:
        handle_healthcare_location(message)
    elif user_intent == intents.COVID_INFORMATION:
        handle_covid_information()
