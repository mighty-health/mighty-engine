import importlib
from . import segments
from .. import settings
from fhirclient import client
from fhirclient.models.patient import Patient

smart_settings = {
    'app_id': settings.FHIR_SERVER_APP_ID,
    'api_base': settings.FHIR_SERVER_API_BASE
}
smart = client.FHIRClient(settings=smart_settings)

def _valid_patient_id(patient_id):
    try:
        Patient.read(patient_id, smart.server)
        return True
    except client.FHIRNotFoundException:
        return False

def _get_segment_model(patient_id):
    # demographics = segments.common._get_patient_demographics(
    #     patient_id=patient_id,
    #     smart_client=smart
    #     )
    # **** TEMPORARILY STUBBED ****
    # target_segment = demographics['segment']
    target_segment = 'male_young'
    segment_model = importlib.import_module(
        '.segments.{}'.format(target_segment),
        __package__
        )
    return segment_model

def get_summary(patient_id):
    if _valid_patient_id(patient_id=patient_id):
        segment_model = _get_segment_model(patient_id=patient_id)
        return segment_model.get_summary(
            patient_id=patient_id,
            smart_client=smart
            )
    else:
        return None

def get_immunization_checklist(patient_id):
    if _valid_patient_id(patient_id=patient_id):
        segment_model = _get_segment_model(patient_id=patient_id)
        return segment_model.get_immunization_checklist(
            patient_id=patient_id,
            smart_client=smart
            )
    else:
        return None

def get_screening_checklist(patient_id):
    if _valid_patient_id(patient_id=patient_id):
        segment_model = _get_segment_model(patient_id=patient_id)
        return segment_model.get_screening_checklist(
            patient_id=patient_id,
            smart_client=smart
            )
    else:
        return None

def get_health_metrics(patient_id):
    if _valid_patient_id(patient_id=patient_id):
        segment_model = _get_segment_model(patient_id=patient_id)
        return segment_model.get_health_metrics(
            patient_id=patient_id,
            smart_client=smart
            )
    else:
        return None
