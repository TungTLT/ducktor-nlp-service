class DiseaseInformation:
    _overview_path = "http://schema.org/OverviewHealthAspect"
    _symptoms_path = "http://schema.org/SymptomsHealthAspect"
    _prevention_path = "http://schema.org/PreventionHealthAspect"
    _diagnosis_path = "http://schema.org/DiagnosisHealthAspect"
    _treatment_path = "http://schema.org/TreatmentsHealthAspect"

    def __init__(self, name: str, overview='', symptoms='', prevention='', diagnosis='', treatment=''):
        self.name = name
        self.overview = overview
        self.symptoms = symptoms
        self.prevention = prevention
        self.diagnosis = diagnosis
        self.treatment = treatment

    @staticmethod
    def from_map(response):
        name = response['name']
        disease_information = DiseaseInformation(name=name)
        has_part = response['hasPart']
        for part in has_part:
            has_health_aspect = part['hasHealthAspect']
            if has_health_aspect == DiseaseInformation._overview_path:
                disease_information.overview = part['description']
                continue

            if has_health_aspect == DiseaseInformation._symptoms_path:
                disease_information.symptoms = part['description']
                continue

            if has_health_aspect == DiseaseInformation._treatment_path:
                disease_information.treatment = part['description']
                continue

            if has_health_aspect == DiseaseInformation._diagnosis_path:
                disease_information.diagnosis = part['description']
                continue

            if has_health_aspect == DiseaseInformation._prevention_path:
                disease_information.prevention = part['description']
                continue

        return disease_information

    def to_map(self):
        return {
            'name': self.name,
            'overview': self.overview,
            'symptoms': self.symptoms,
            'treatment': self.treatment,
            'diagnosis': self.diagnosis,
            'prevention': self.prevention
        }

    def is_not_valid(self) -> bool:
        return self.overview == '' \
               and self.symptoms == '' \
               and self.treatment == '' \
               and self.diagnosis == '' \
               and self.prevention == ''
