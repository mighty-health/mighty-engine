import datetime
from fhirclient.models.patient import Patient

_today = datetime.date.today()

def _get_patient_demographics(patient_id, smart_client):
    patient = Patient.read(patient_id, smart_client.server)
    demographics = {}
    demographics['gender'] = patient.gender
    demographics['age'] = int((_today-patient.birthDate.date).days/365)
    demographics['birthDate'] = patient.birthDate.date
    if (demographics['age'] <= 17):
        age_classification = 'child'
    elif (demographics['age'] >= 18) and (demographics['age'] <= 39):
        age_classification = 'young'
    elif (demographics['age'] >= 40) and (demographics['age'] <= 64):
        age_classification = 'middle'
    elif (demographics['age'] >= 65):
        age_classification = 'old'
    demographics['segment'] = '{}_{}'.format(demographics['gender'], age_classification)

    return demographics
