import requests
from find_healthcare_location.healthcare_location import HealthCareLocation
from pathlib import Path
from common.api_url import AUTO_COMPLETE_API, NEARBY_SEARCH_API, NEARBY_SEARCH_JAVA_API
import os
from config import AppConfig, ConfigType

folder_location = Path(__file__).absolute().parent


def check_app_config_if_call_java_service():
    return True if AppConfig.service_config == ConfigType.CALL_JAVA_SERVICE else False


class HealthCareLocationClient:
    api_key = os.getenv('HEALTHCARE_LOC_API_KEY')
    autocomplete_base_url = AUTO_COMPLETE_API
    nearby_search_base_url = NEARBY_SEARCH_API if not check_app_config_if_call_java_service() else NEARBY_SEARCH_JAVA_API

    def __init__(self, latitude: float, longitude: float):
        self.lat = latitude
        self.lon = longitude

    def _get_category_set_from_user_input(self, user_input: str) -> [int]:
        autocomplete_url = self.autocomplete_base_url % {'query_parameter': user_input, 'key': self.api_key}
        category_sets = []
        try:
            response = requests.get(autocomplete_url).json()
            results = response['results']
            for result in results:
                segments = result['segments']
                for segment in segments:
                    if segment['type'] == 'category':
                        category_sets.append(segment['id'])
            return category_sets

        except requests.exceptions.JSONDecodeError:
            print('Json Decode Error')
            return []
        except KeyError:
            print('Key error')
            return []

    def _search_nearby_healthcare_location_dver(self, input: str):
        category_sets = self._get_category_set_from_user_input(input)
        if len(category_sets) == 0:
            return []

        cate_list_str = ','.join([str(i) for i in category_sets])
        nearby_search_url = self.nearby_search_base_url % {'key': self.api_key,
                                                           'lat': self.lat,
                                                           'lon': self.lon,
                                                           'categorySets': cate_list_str,
                                                           'limit': 5}
        try:
            response = requests.get(nearby_search_url).json()
            results = response['results']
            healthcare_locations = []
            for result in results:
                location = HealthCareLocation.from_map(result)
                if location is not None:
                    healthcare_locations.append(location)

            return healthcare_locations
        except requests.exceptions.JSONDecodeError:
            print('Json Decode Error')
            return []
        except KeyError:
            print('Key Error')
            return []

    def _search_nearby_healthcare_location_jver(self, input: str):
        try:
            nearby_search_url = self.nearby_search_base_url % {'lat': self.lat,
                                                               'lon': self.lon,
                                                               'input': input}

            healthcare_locations = []
            response = requests.get(nearby_search_url).json()
            for result in response:
                location = HealthCareLocation.from_map_jver(result)
                if location is not None:
                    healthcare_locations.append(location)

            return healthcare_locations
        except requests.exceptions.JSONDecodeError:
            print('Json Decode Error')
            return []
        except KeyError:
            print('Key Error')
            return []

    def search_nearby_healthcare_location(self, input: str):
        if check_app_config_if_call_java_service():
            return self._search_nearby_healthcare_location_jver(input)
        else:
            return self._search_nearby_healthcare_location_dver(input)

# list = HealthCareLocationClient(latitude=10.77134, longitude=106.629766).search_nearby_healthcare_location('find nearest hospital')
#
# for e in list:
#     print(e.to_json())
