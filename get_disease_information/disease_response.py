class DiseaseResponse:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f'DiseaseResponse(name: {self.name}, url: {self.url})'
