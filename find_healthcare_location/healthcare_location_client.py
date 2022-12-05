import requests
from find_healthcare_location.healthcare_location import HealthCareLocation
from pathlib import Path
import os

folder_location = Path(__file__).absolute().parent


class HealthCareLocationClient:
    api_key = open(f'{folder_location}/api_key.txt', 'r').read()
    autocomplete_base_url = os.getenv('AUTO_COMPLETE_API')
    nearby_search_base_url = os.getenv('NEARBY_SEARCH_API')
 
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

    def search_nearby_healthcare_location(self, input: str):
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

# print(HealthCareLocationClient(latitude=10.77134, longitude=106.629766).search_nearby_healthcare_location('the nearest hospital')[0].toJSON())