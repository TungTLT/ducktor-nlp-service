import json
from pathlib import Path
import random

folder_location = Path(__file__).absolute().parent
file_reader = open(f'{folder_location}/suggest_messages.json', 'r')


class SuggestMessageProvider:
    picked_number = 5
    suggest_messages: dict = json.load(file_reader)['suggest_messages']

    def get_conversation_messages(self) -> list[str]:
        try:
            result = set()
            while len(result) < 5:
                result.add(random.choice(self.suggest_messages['conversation']['intents']))

            return list(result)
        except KeyError:
            return []

    def get_predict_disease_enter_symptoms_messages(self) -> list[str]:
        try:
            result = set()
            suggest_symptoms = self.suggest_messages['predict_disease']['enter_symptoms']
            while len(result) < 5:
                result.add(random.choice(suggest_symptoms))

            return list(result)
        except KeyError:
            return []

    def get_predict_disease_continue_messages(self):
        try:
            return self.suggest_messages['predict_disease']['continue_predict_answer']
        except KeyError:
            return[]

