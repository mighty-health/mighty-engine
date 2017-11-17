import datetime

from ..common import _today, _get_patient_demographics
from ..code_lookup import immunization_lookup

from fhirclient.models.immunization import Immunization


def get_health_metrics(patient_id, smart_client):

    rank_counter = 1
    metric_list = []
    metric_title = 'Body Mass Index'
    metric_category = 'Vital Signs'
    metric_status = 'normal'
    readings_list = []
    metric_reading = {
        'date': 'MM/DD/YYYY',
        'value': str(round(34.45660564235176, 2)),
        'unit': 'kg/m2'
    }
    readings_list.append(metric_reading)
    readings_list.append(metric_reading)

    health_metric_record = {
        'title': metric_title,
        'status': metric_status,
        'category': metric_category,
        'readings': readings_list,
        'rank': rank_counter,
        'description': '',
    }
    metric_list.append(health_metric_record)
    rank_counter += 1

    return metric_list
