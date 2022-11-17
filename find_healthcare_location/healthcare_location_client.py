import requests


class HealthCareLocationClient:
    api_key = open('api_key.txt', 'r').read()
    autocomplete_base_url = 'https://api.tomtom.com/search/2/autocomplete/%(query_parameter)s.json?key=%(key)s&language=en-US'
    nearby_search_base_url = 'https://api.tomtom.com/search/2/nearbySearch/.json?key=%(key)s&lat=%(lat)f&lon=%(lon)f&categorySet=%(categorySets)s'

    def __init__(self, latitude: float, longitude: float):
        self.lat = latitude
        self.lon = longitude

    def get_category_set_from_user_input(self, user_input: str) -> [int]:
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
        category_sets = self.get_category_set_from_user_input(input)
        cate_list_str = ','.join([str(i) for i in category_sets])
        nearby_search_url = self.nearby_search_base_url % {'key': self.api_key,
                                                           'lat': self.lat,
                                                           'lon': self.lon,
                                                           'categorySets': cate_list_str}
        try:
            # response = requests.get(nearby_search_url).json()
            print(nearby_search_url)
        except requests.exceptions.JSONDecodeError:
            print('Json Decode Error')
            return []
        except KeyError:
            print('Key Error')
            return []

