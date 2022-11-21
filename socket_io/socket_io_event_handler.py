from conversation_model import chatbot as con_model
from disease_prediction_model import chatbot_disease_prediction_v2 as disease_prediction_model
from common import intents, socket_io_event
from socket_io_response import SocketIOResponse
from named_entity_recognition_model import nltk_ner as disease_info_model
from get_disease_information.disease_information_client import GetDiseaseInformationClient
from __main__ import socketIO
from find_healthcare_location.healthcare_location_client import HealthCareLocationClient
import json
from common.suggest_message_provider import SuggestMessageProvider

sug_mes_provider = SuggestMessageProvider()


@socketIO.on(socket_io_event.EVENT_CONNECT)
def connect():
    print("A user connected!")
    message = "Hello! It's Ducktor. How can I help you?"
    suggest_messages = sug_mes_provider.get_conversation_messages()
    socketIO.send(SocketIOResponse(intent=intents.GREETING,
                                   content=message, suggest_messages=suggest_messages).as_dictionary())


@socketIO.on(socket_io_event.EVENT_DISCONNECT)
def disconnect():
    print("A user disconnected!")


@socketIO.on(socket_io_event.EVENT_DISEASE_PREDICTION)
def handle_disease_prediction():
    suggest_messages = sug_mes_provider.get_predict_disease_enter_symptoms_messages()
    response = SocketIOResponse(intents.DISEASE_PREDICTION, 'What is your disease symptoms?',
                                socket_io_event.EVENT_RECEIVE_SYMPTOMS, suggest_messages=suggest_messages)
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
        suggest_messages = sug_mes_provider.get_predict_disease_continue_messages()
        socketIO.send(SocketIOResponse(intents.DISEASE_PREDICTION,
                                       'Do you want me to continue to predict your disease?',
                                       socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT,
                                       suggest_messages=suggest_messages).as_dictionary())

    @socketIO.on(socket_io_event.EVENT_ASK_FOR_CONTINUE_PREDICT)
    def ask_for_continue_predict(message: str):
        message = message.lower()
        suggest_messages = sug_mes_provider.get_predict_disease_enter_symptoms_messages()
        if message == 'yes' or 'yes' in message or message == 'y':
            response = SocketIOResponse(intents.DISEASE_PREDICTION, 'What is your disease symptoms?',
                                        socket_io_event.EVENT_RECEIVE_SYMPTOMS,
                                        suggest_messages=suggest_messages)
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


def handle_healthcare_location(user_input: str):
    message = 'Can I have your location'
    socketIO.send(SocketIOResponse(intents.HEALTHCARE_LOCATION,
                                   message, socket_io_event.EVENT_ASK_FOR_USER_LOCATION).as_dictionary())

    @socketIO.on(socket_io_event.EVENT_ASK_FOR_USER_LOCATION)
    def handle_receive_user_location_and_return_healthcare_locations(user_location: str):
        user_location = json.loads(user_location)
        if isinstance(user_location, dict) and len(user_location) != 0:
            lat = user_location['lat']
            lon = user_location['lon']
            healthcare_loc_client = HealthCareLocationClient(latitude=lat, longitude=lon)
            healthcare_locations = healthcare_loc_client.search_nearby_healthcare_location(user_input)
            # chờ xem frontend cần gì để mở map
            print(healthcare_locations)

        else:
            message = 'Sorry! I can find without your location.'
            socketIO.send(intents.OPTIONS, message, socket_io_event.EVENT_MESSAGE)


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
    elif user_intent == intents.HEALTHCARE_LOCATION:
        handle_healthcare_location(message)
