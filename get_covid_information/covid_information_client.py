import requests
from common.api_url import COVID_API


class CovidAPI:
    base_url = COVID_API
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
    def get_summary_global(self):
        try:
            response = requests.get(url=self.base_url).json()
            return {
                'infected_in_day': response['Global']['NewConfirmed'],
                'infected_total': response['Global']['TotalConfirmed'],
                'death_in_day': response['Global']['NewDeaths'],
                'death_total': response['Global']['TotalDeaths'],
                'recovered_in_day': response['Global']['NewRecovered'],
                'recovered_total': response['Global']['TotalRecovered']
            }
        except requests.exceptions.JSONDecodeError:
            print('Json Decode Error')
            return None
        except KeyError:
            print('Key Error')
            return None

    def get_infected_in_day_global(self):
        if self._infected_in_day_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'NewConfirmed' in response['Global']:
                    self._infected_in_day_global = response['Global']['NewConfirmed']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._infected_in_day_global}

    def get_total_infected_global(self):
        if self._total_infected_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'TotalConfirmed' in response['Global']:
                    self._total_infected_global = response['Global']['TotalConfirmed']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._total_infected_global}

    def get_death_in_day_global(self):
        if self._death_in_day_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'NewDeaths' in response['Global']:
                    self._death_in_day_global = response['Global']['NewDeaths']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._death_in_day_global}

    def get_total_death_global(self):
        if self._total_death_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'TotalDeaths' in response['Global']:
                    self._total_death_global = response['Global']['TotalDeaths']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._total_death_global}

    def get_recover_in_day_global(self):
        if self._recover_in_day_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'NewRecovered' in response['Global']:
                    self._recover_in_day_global = response['Global']['NewRecovered']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._recover_in_day_global}

    def get_total_recover_global(self):
        if self._total_recover_global is None:
            try:
                response = requests.get(url=self.base_url).json()
                if 'Global' in response and 'TotalRecovered' in response['Global']:
                    self._total_recover_global = response['Global']['TotalRecovered']
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._total_recover_global}

    # VIETNAM
    def get_summary_vietnam(self):
        try:
            response = requests.get(url=self.base_url).json()
            countries = response['Countries']
            for country in countries:
                if country['CountryCode'] == 'VN':
                    return {
                        'infected_in_day': country['NewConfirmed'],
                        'infected_total': country['TotalConfirmed'],
                        'death_in_day': country['NewDeaths'],
                        'death_total': country['TotalDeaths'],
                        'recovered_in_day': country['NewRecovered'],
                        'recovered_total': country['TotalRecovered']
                    }
            return None
        except requests.exceptions.JSONDecodeError:
            print('Json Decode Error')
            return None
        except KeyError:
            print('Key Error')
            return None

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
                        else:
                            raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._infected_in_day_vietnam}

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
                        else:
                            raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._total_infected_vietnam}

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
                        else:
                            raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._death_in_day_vietnam}

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
                        else:
                            raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._total_death_vietnam}

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
                        else:
                            raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._recover_in_day_vietnam}

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
                        else:
                            raise ValueError
                else:
                    raise ValueError
            except ValueError:
                print('Value Error')
                return None
            except requests.exceptions.JSONDecodeError:
                print('Json Decode Error')
                return None

        return {'result': self._total_recover_vietnam}
