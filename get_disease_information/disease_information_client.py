import requests
from pathlib import Path
from get_disease_information.disease_information import DiseaseInformation
from get_disease_information.disease_response import DiseaseResponse
from config import AppConfig, ConfigType
from common.api_url import SEARCH_DISEASE_INFO_API
import os

folder_location = Path(__file__).absolute().parent


def map_to_disease_response(network_response):
    return DiseaseResponse(name=network_response['name'], url=network_response['url'])


def check_app_config_if_call_java_service():
    return True if AppConfig.service_config == ConfigType.CALL_JAVA_SERVICE else False


search_third_party_api = SEARCH_DISEASE_INFO_API
search_java_service_api = 'http://localhost:8080/ducktor/search?category=%s'
detail_java_service_api = 'http://localhost:8080/ducktor/details?url=%s'


class GetDiseaseInformationClient:
    api_key = os.getenv('DISEASE_INFO_API_KEY')
    headers = {
        'subscription-key': api_key
    }

    def search_for_disease_information(self, user_input):
        url = search_java_service_api if check_app_config_if_call_java_service() else search_third_party_api
        url = url % user_input
        response = requests.get(url=url, headers=self.headers).json()
        results = response['significantLink']
        return list(map(map_to_disease_response, results))

    def get_disease_information(self, url):
        response = requests.get(url, headers=self.headers).json()
        disease_information = DiseaseInformation.from_map(response)
        return disease_information
