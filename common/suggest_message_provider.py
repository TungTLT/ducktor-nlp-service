import json
from pathlib import Path

folder_location = Path(__file__).absolute().parent
file_reader = open(f'{folder_location}/suggest_messages.json', 'r')


class SuggestMessageProvider:
    suggest_messages: dict = json.load(file_reader)['suggest_messages']

    def get_conversation_messages(self) -> list[str]:
        try:
            return self.suggest_messages['conversation']['intents']
        except KeyError:
            return []

    def get_predict_disease_enter_symptoms_messages(self) -> list[str]:
        try:
            return self.suggest_messages['predict_disease']['enter_symptoms']
        except KeyError:
            return[]

    def get_predict_disease_continue_messages(self):
        try:
            return self.suggest_messages['predict_disease']['continue_predict_answer']
        except KeyError:
            return[]


print(SuggestMessageProvider().get_predict_disease_continue_messages())