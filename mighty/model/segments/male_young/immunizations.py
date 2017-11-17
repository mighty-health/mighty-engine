import datetime

from ..common import _today, _get_patient_demographics
from ..code_lookup import immunization_lookup

from fhirclient.models.immunization import Immunization

def _get_patient_immunizations(patient_id, smart_client):

    immunizations = Immunization.where(struct={'patient': patient_id}).perform_resources(smart_client.server)
    unique_immunization_codings = set([x.vaccineCode.coding[0] for x in immunizations])
    immunizations_list = {}
    for coding in unique_immunization_codings:
        immunizations_list[coding.code] = {
            'display': coding.display,
            'dates': [],
        }
        for immunization in immunizations:
            if immunization.vaccineCode.coding[0].code == coding.code:
                immunizations_list[coding.code]['dates'].append(immunization.date.date)
        immunizations_list[coding.code]['dates'].sort(reverse=True)

    return immunizations_list


def get_immunization_checklist(patient_id, smart_client):

    demographics = _get_patient_demographics(patient_id, smart_client)
    past_immunizations = _get_patient_immunizations(patient_id, smart_client)
    rank_counter = 1
    checklist = []
    # ==================================================================================
    # Flu Shot
    # ==================================================================================
    immunization_title = 'Flu Shot'
    lookup = immunization_lookup[immunization_title]
    season_months = [8, 9, 10, 11, 12]
    classification = 'recommended'
    if lookup['code'] in past_immunizations.keys():
        prior_dates = [x.date().isoformat() for x in past_immunizations[lookup['code']]['dates']]
        most_recent_date = past_immunizations[lookup['code']]['dates'][0]
        if (most_recent_date.month in season_months) and (most_recent_date.year == _today.year):
            due_date = '-'
            status = 'complete'
        elif (_today.month in season_months):
            due_date = 'ASAP'
            status = 'pending'
        else:
            due_date = '-'
            status = 'complete'
    else:
        prior_dates = None
        due_date = 'ASAP'
        status = 'pending'
    flu_record = {
        'title': immunization_title,
        'subtitle': lookup['disease'],
        'timing': 'Once a year',
        'due_date': due_date,
        'prior_dates': prior_dates,
        'status': status,
        'classification': classification,
        'rank': rank_counter,
        'description': '',
    }
    checklist.append(flu_record)
    rank_counter += 1
    # ==================================================================================
    # Td Booster
    # ==================================================================================
    immunization_title = 'Td Booster'
    lookup = immunization_lookup[immunization_title]
    classification = 'recommended'
    if lookup['code'] in past_immunizations.keys():
        prior_dates = [x.date().isoformat() for x in past_immunizations[lookup['code']]['dates']]
        most_recent_date = past_immunizations[lookup['code']]['dates'][0]
        months_since_last_dose = int((_today-most_recent_date.date()).days/30)
        if months_since_last_dose > (12*10):
            due_date = 'ASAP'
            status = 'pending'
        else:
            due_date = most_recent_date.replace(most_recent_date.year+10).isoformat()
            status = 'complete'
    elif demographics['age'] >= 19:
        prior_dates = None
        due_date = 'ASAP'
        status = 'pending'
    else:
        classification = 'remove'

    if classification != 'remove':
        td_record = {
            'title': immunization_title,
            'subtitle': lookup['disease'],
            'timing': 'Once every 10 years',
            'due_date': due_date,
            'prior_dates': prior_dates,
            'status': status,
            'classification': classification,
            'rank': rank_counter,
            'description': '',
        }
        checklist.append(td_record)
        rank_counter += 1

    # Return result
    return checklist
