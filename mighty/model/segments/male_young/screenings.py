import datetime
from operator import itemgetter

from ..common import _today, _get_patient_demographics
from ..code_lookup import health_metric_lookup, condition_lookup

from fhirclient.models.observation import Observation

def _get_patient_screenings(patient_id, smart):
    screenings = Observation.where(struct={'patient': patient_id}).perform_resources(smart.server)
    unique_screening_codings = set([x.code.coding[0] for x in screenings])
    screenings_list = {}
    for coding in unique_screening_codings:
        screenings_list[coding.code] = {
            'display': coding.display,
            'dates': [],
            'values': []
        }
        date_value_list = []
        for screening in screenings:
            if screening.code.coding[0].code == coding.code:
                try:
                    date_value_list.append([screening.effectiveDateTime.date,[round(screening.valueQuantity.value,3),screening.valueQuantity.unit]])
                except AttributeError:
                    date_value_list.append([screening.effectiveDateTime.date,'-','-'])
            date_value_list = sorted(date_value_list, key=itemgetter(0),reverse=True)
        screenings_list[coding.code]['dates'] = [x[0] for x in date_value_list]
        screenings_list[coding.code]['values'] = [x[1] for x in date_value_list]

    return screenings_list

def get_screening_checklist(patient_id, smart_client):

    rank_counter = 1
    checklist = []
    screening_title = 'Type-2 Diabetes Screening'
    screening_status = 'complete'
    due_date = 'MM/DD/YYYY'
    most_recent_date = 'MM/DD/YYYY'

    observation_list = []
    screening_observation = {
        'name': 'Glucose',
        'value': str(round(115, 2)),
        'unit': 'mg/dL'
    }
    observation_list.append(screening_observation)
    observation_list.append(screening_observation)

    screening_record = {
        'title': screening_title,
        'status': screening_status,
        'timing': 'Every X years',
        'due_date': due_date,
        'most_recent_date': most_recent_date,
        'observations': observation_list,
        'rank': rank_counter,
        'description': '',
    }
    checklist.append(screening_record)
    rank_counter += 1

    return checklist

# def get_screening_checklist(patient_id, smart_client):
#
#     demographics = _get_patient_demographics(patient_id, smart_client)
#     past_screenings = _get_patient_screenings(patient_id, smart_client)
#     rank_counter = 1
#     checklist = []
#     # ==================================================================================
#     # Blood Pressure
#     # ==================================================================================
#     screening_title = 'Blood Pressure'
#     lookup = health_metric_lookup[screening_title]
#     classification = 'recommended'
#     if (lookup['code'] in past_screenings.keys()) and \
#         (health_metric_lookup['Diastolic Blood Pressure']['code'] in past_screenings.keys()) and \
#         (health_metric_lookup['Systolic Blood Pressure']['code'] in past_screenings.keys()):
#         prior_dates = [x.date().strftime('%m/%d/%Y') for x in past_screenings[lookup['code']]['dates']]
#         most_recent_date = past_screenings[lookup['code']]['dates'][0]
#         systolic_value = past_screenings[health_metric_lookup['Systolic Blood Pressure']['code']]['values'][0][0]
#         diastolic_value = past_screenings[health_metric_lookup['Diastolic Blood Pressure']['code']]['values'][0][0]
#
#         if (systolic_value>140) or (diastolic_value>90):
#             due_date = 'ASAP'
#             status = 'pending'
#         elif (systolic_value>120) or (diastolic_value>80): # ignoring risk factors for now
#             if int((_today-most_recent_date.date())/365)<1:
#                 due_date = most_recent_date.replace(most_recent_date.year+3).strftime('%m/%d/%Y')
#                 status = 'complete'
#             else:
#                 due_date = 'ASAP'
#                 status = 'pending'
#         elif int((_today-most_recent_date.date())/365)<3:
#             due_date = most_recent_date.replace(most_recent_date.year+3).strftime('%m/%d/%Y')
#             status = 'complete'
#         else:
#             due_date = 'ASAP'
#             status = 'pending'
#     else:
#         prior_dates = None
#         due_date = 'ASAP'
#         status = 'pending'
#
#     obs_vals = []
#     try:
#         obs_vals.append([past_screenings[lookup['code']]])
#     except KeyError:
#         pass
#
#     date_val = ''
#     try:
#         prior_dates[0]
#     except TypeError:
#         pass
#
#
#     if classification != 'remove':
#         blood_pressure_record = {
#             'title': screening_title,
#             'status': status,
#             'rank': rank_counter,
#             'timing': 'Typically every 3-5 years',
#             'due_date': due_date,
#             'most_recent_date': date_val,
#             'observations': obs_vals,
#             'description': '',
#         }
#         checklist.append(blood_pressure_record)
#         rank_counter += 1
#     # ==================================================================================
#     # Cholesterol
#     # ==================================================================================
#     screening_title = 'Total Cholesterol'
#     lookup = health_metric_lookup[screening_title]
#     classification = 'recommended'
#     if (lookup['code'] in past_screenings.keys()):
#         prior_dates = [x.date().strftime('%m/%d/%Y') for x in past_screenings[lookup['code']]['dates']]
#         most_recent_date = past_screenings[lookup['code']]['dates'][0]
#
#         if demographics['age']<=35:
#             classification = 'remove'
#         elif int((_today-most_recent_date.date())/365)<5: # ignoring risk factors for now
#             due_date = most_recent_date.replace(most_recent_date.year+5).strftime('%m/%d/%Y')
#             status = 'complete'
#         else:
#             due_date = 'ASAP'
#             status = 'pending'
#     else:
#         if demographics['age']<=35:
#             classification = 'remove'
#         else:
#             prior_dates = None
#             due_date = 'ASAP'
#             status = 'pending'
#
#     obs_vals = []
#     try:
#         obs_vals.append([past_screenings[lookup['code']]])
#     except KeyError:
#         pass
#
#     date_val = ''
#     try:
#         prior_dates[0]
#     except TypeError:
#         pass
#
#     if classification != 'remove':
#         cholesterol_record = {
#             'title': screening_title,
#             'status': status,
#             'rank': rank_counter,
#             'timing': 'typically every 5 years',
#             'due_date': due_date,
#             'most_recent_date': date_val,
#             'observations': obs_vals,
#             'description': '',
#         }
#         checklist.append(cholesterol_record)
#         rank_counter += 1
#     # ==================================================================================
#     # Glucose
#     # ==================================================================================
#     screening_title = 'Glucose'
#     lookup = health_metric_lookup[screening_title]
#     classification = 'recommended'
#
#     if health_metric_lookup['Body Mass Index']['code'] in past_screenings.keys():
#         BMI_value = past_screenings[health_metric_lookup['Body Mass Index']['code']]['values'][0][0]
#     else:
#         BMI_value = 0
#
#     if (lookup['code'] in past_screenings.keys()):
#         prior_dates = [x.date().strftime('%m/%d/%Y') for x in past_screenings[lookup['code']]['dates']]
#         most_recent_date = past_screenings[lookup['code']]['dates'][0]
#
#         if (BMI_value)>25:
#             if int((_today-most_recent_date.date())/365)<1:
#                 due_date = most_recent_date.replace(most_recent_date.year+1).strftime('%m/%d/%Y')
#                 status = 'complete'
#             else:
#                 due_date = 'ASAP'
#                 status = 'pending'
#     elif (BMI_value)>25:
#         due_date = 'ASAP'
#         status = 'pending'
#     else:
#         classification = 'remove'
#
#     obs_vals = []
#     try:
#         obs_vals.append([past_screenings[lookup['code']]])
#     except KeyError:
#         pass
#
#     date_val = ''
#     try:
#         prior_dates[0]
#     except TypeError:
#         pass
#
#     if classification != 'remove':
#         glucose_record = {
#             'title': screening_title+'_Diabetes',
#             'status': status,
#             'rank': rank_counter,
#             'timing': 'Every year if relevant',
#             'due_date': due_date,
#             'most_recent_date': date_val,
#             'observations': obs_vals,
#             'description': '',
#         }
#         checklist.append(glucose_record)
#         rank_counter += 1
#     # ==================================================================================
#     # Physical
#     # ==================================================================================
#     screening_title = 'Physical'
#     lookup_set = [health_metric_lookup['Body Height'],health_metric_lookup['Body Weight'],health_metric_lookup['Blood Pressure']]
#     classification = 'recommended'
#
#     metric_ct = 0
#     earliest_most_recent_date = ''
#     for lookup in lookup_set:
#         if (lookup['code'] in past_screenings.keys()):
#             metric_ct +=1
#             prior_dates = [x.date().strftime('%m/%d/%Y') for x in past_screenings[lookup['code']]['dates']]
#             most_recent_date = past_screenings[lookup['code']]['dates'][0]
#             if earliest_most_recent_date=='':
#                 earliest_most_recent_date = most_recent_date
#             elif most_recent_date.date()<earliest_most_recent_date.date():
#                 earliest_most_recent_date = most_recent_date
#
#     if metric_ct == 3:
#         if int((_today-earliest_most_recent_date.date()).days/365)<1:
#             due_date = earliest_most_recent_date.replace(most_recent_date.year+1).strftime('%m/%d/%Y')
#             status = 'complete'
#         else:
#             due_date = 'ASAP'
#             status = 'pending'
#     prior_dates = []
#
# #     for i in lookup_set:
# #         try:
# #             prior_dates.append(past_screenings[i]['dates'])
# #         except KeyError:
# #             prior_dates.append([])
#
#     obs_vals = []
#     for i in lookup_set:
#         try:
#             obs_vals.append(past_screenings[i['code']])
#         except KeyError:
#             obs_vals.append([])
#
#     if classification != 'remove':
#         physical_record = {
#             'title': screening_title,
#             'status': status,
#             'rank': rank_counter,
#             'timing': 'Once per year',
#             'due_date': due_date,
#             'most_recent_date': earliest_most_recent_date,
#             'observations': obs_vals,
#             'description': '',
#         }
#         checklist.append(physical_record)
#         rank_counter += 1
#
#     return checklist
