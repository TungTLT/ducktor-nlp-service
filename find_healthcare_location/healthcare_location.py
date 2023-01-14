import json


class Location:
    def __init__(self, lat: float = 0.0, lon: float = 0.0):
        self.lat = lat
        self.lon = lon

    @staticmethod
    def from_map(response: dict):
        try:
            return Location(response['position']['lat'], response['position']['lon'])
        except KeyError:
            return None

    @staticmethod
    def from_map_jver(response: dict):
        try:
            return Location(response['location']['lat'], response['location']['lon'])
        except KeyError:
            return None


class Address:
    def __init__(self, street_number: str, street_name: str, district: str, city: str):
        self.street_number = street_number
        self.street_name = street_name
        self.district = district
        self.city = city

    def __str__(self):
        return f'{self.street_number} {self.street_name}, {self.district}, {self.city}'

    @staticmethod
    def from_map(response: dict):
        address = response['address']
        try:
            return Address(address['streetNumber'], address['streetName'], address['municipalitySubdivision'],
                           address['municipality'])
        except KeyError:
            return None

    @staticmethod
    def from_map_jver(response: dict):
        address = response['address']
        try:
            return Address(address['streetNumber'], address['streetName'], address['district'],
                           address['city'])
        except KeyError:
            return None


class HealthCareLocation:
    def __init__(self, name: str, address: Address, location: Location):
        self.name = name
        self.address = address
        self.location = location

    def __str__(self):
        address_value = str(self.address) if self.address is not None else '(Not found address)'
        return f'{self.name}\n{address_value}'

    @staticmethod
    def from_map(response: dict):
        try:
            address = Address.from_map(response)
            location = Location.from_map(response)
            return HealthCareLocation(name=response['poi']['name'], address=address, location=location)
        except KeyError:
            return None

    @staticmethod
    def from_map_jver(response: dict):
        try:
            address = Address.from_map_jver(response)
            location = Location.from_map_jver(response)
            return HealthCareLocation(name=response['name'], address=address, location=location)
        except KeyError:
            return None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

# print(json.dumps(HealthCareLocation('a', Address('65', 'a', 'd', 'b'), Location(1, 1)).toJSON()))
