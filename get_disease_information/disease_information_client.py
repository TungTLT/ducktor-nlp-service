import requests
from pathlib import Path
from get_disease_information.disease_information import DiseaseInformation
from get_disease_information.disease_response import DiseaseResponse

folder_location = Path(__file__).absolute().parent


def map_to_disease_response(network_response):
    return DiseaseResponse(name=network_response['name'], url=network_response['url'])


class GetDiseaseInformationClient:
    base_url = 'https://api.nhs.uk/conditions/?category=%s'
    api_key = open(f'{folder_location}/api_key.txt', 'r').read()
    headers = {
        'subscription-key': api_key
    }

    def search_for_disease_information(self, user_input):
        url = self.base_url % user_input
        response = requests.get(url=url, headers=self.headers).json()
        results = response['significantLink']
        return list(map(map_to_disease_response, results))

    def get_disease_information(self, url):
        response = requests.get(url, headers=self.headers).json()
        disease_information = DiseaseInformation.from_map(response)
        return disease_information
