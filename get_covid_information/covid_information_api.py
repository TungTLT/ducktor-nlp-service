import requests


class CovidAPI:
    base_url = 'https://api.covid19api.com/summary'
    _infected_in_day_global = None
    _total_infected_global = None
    _death_in_day_global = None
    _total_death_global = None
    _recover_in_day_global = None
    _total_recover_global = None

    _infected_in_day_vietnam = None
    _total_infected_vietnam = None
    _death_in_day_vietnam = None
    _total_death_vietnam = None
    _recover_in_day_vietnam = None
    _total_recover_vietnam = None

    # GLOBAL
    def get_infected_in_day_global(self) -> int:
        if self._infected_in_day_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'NewConfirmed' in response['Global']:
                    self._infected_in_day_global = response['Global']['NewConfirmed']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

        return self._infected_in_day_global

    def get_total_infected_global(self) -> int:
        if self._total_infected_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'TotalConfirmed' in response['Global']:
                    self._total_infected_global = response['Global']['TotalConfirmed']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

        return self._total_infected_global

    def get_death_in_day_global(self) -> int:
        if self._death_in_day_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'NewDeaths' in response['Global']:
                    self._death_in_day_global = response['Global']['NewDeaths']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

        return self._death_in_day_global

    def get_total_death_global(self) -> int:
        if self._total_death_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'TotalDeaths' in response['Global']:
                    self._total_death_global = response['Global']['TotalDeaths']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

        return self._total_death_global

    def get_recover_in_day_global(self) -> int:
        if self._recover_in_day_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'NewRecovered' in response['Global']:
                    self._recover_in_day_global = response['Global']['NewRecovered']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

        return self._recover_in_day_global

    def get_total_recover_global(self) -> int:
        if self._total_recover_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'TotalRecovered' in response['Global']:
                    self._total_recover_global = response['Global']['TotalRecovered']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

        return self._total_recover_global

    # VIETNAM
    def get_infected_in_day_vietnam(self):
        if self._infected_in_day_vietnam is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Countries' in response:
                    countries = response['Countries']
                    for country in countries:
                        if 'CountryCode' in country \
                                and 'NewConfirmed' in country:
                            if country['CountryCode'] == 'VN':
                                self._infected_in_day_vietnam = country['NewConfirmed']
                                return self._infected_in_day_vietnam
                        else:
                            raise ValueError
                    raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

    def get_total_infected_vietnam(self):
        if self._total_infected_vietnam is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Countries' in response:
                    countries = response['Countries']
                    for country in countries:
                        if 'CountryCode' in country \
                                and 'TotalConfirmed' in country:
                            if country['CountryCode'] == 'VN':
                                self._total_infected_vietnam = country['TotalConfirmed']
                                return self._total_infected_vietnam
                        else:
                            raise ValueError
                    raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

    def get_death_in_day_vietnam(self):
        if self._death_in_day_vietnam is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Countries' in response:
                    countries = response['Countries']
                    for country in countries:
                        if 'CountryCode' in country \
                                and 'NewDeaths' in country:
                            if country['CountryCode'] == 'VN':
                                self._death_in_day_vietnam = country['NewDeaths']
                                return self._death_in_day_vietnam
                        else:
                            raise ValueError
                    raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

    def get_total_death_vietnam(self):
        if self._total_death_vietnam is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Countries' in response:
                    countries = response['Countries']
                    for country in countries:
                        if 'CountryCode' in country \
                                and 'TotalDeaths' in country:
                            if country['CountryCode'] == 'VN':
                                self._total_death_vietnam = country['TotalDeaths']
                                return self._total_death_vietnam
                        else:
                            raise ValueError
                    raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

    def get_recover_in_day_vietnam(self):
        if self._recover_in_day_vietnam is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Countries' in response:
                    countries = response['Countries']
                    for country in countries:
                        if 'CountryCode' in country \
                                and 'NewRecovered' in country:
                            if country['CountryCode'] == 'VN':
                                self._recover_in_day_vietnam = country['NewRecovered']
                                return self._recover_in_day_vietnam
                        else:
                            raise ValueError
                    raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0

    def get_total_recover_vietnam(self):
        if self._total_recover_vietnam is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Countries' in response:
                    countries = response['Countries']
                    for country in countries:
                        if 'CountryCode' in country \
                                and 'TotalRecovered' in country:
                            if country['CountryCode'] == 'VN':
                                self._total_recover_vietnam = country['TotalRecovered']
                                return self._total_recover_vietnam
                        else:
                            raise ValueError
                    raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return 0
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return 0
