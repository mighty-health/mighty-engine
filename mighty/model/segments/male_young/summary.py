from ..common import _today, _get_patient_demographics
from ..code_lookup import immunization_lookup
from .immunizations import get_immunization_checklist
from .screenings import get_screening_checklist
from .health_metrics import get_health_metrics
from fhirclient.models.immunization import Immunization

def get_summary(patient_id, smart_client):

    reminder_list = []

    immunization_checklist = get_immunization_checklist(patient_id, smart_client)
    pending_immunizations = 0
    for item in immunization_checklist:
        if item['status'] == 'pending':
            pending_immunizations += 1
            immunization_reminder = {
                'title': item['title'],
                'type': 'Immunization',
                'due_date': item['due_date'],
            }
            reminder_list.append(immunization_reminder)

    screening_checklist = get_screening_checklist(patient_id, smart_client)
    pending_screenings = 0
    for item in screening_checklist:
        if item['status'] == 'pending':
            pending_screenings += 1
            screening_reminder = {
                'title': item['title'],
                'type': 'Screening',
                'due_date': item['due_date'],
            }
            reminder_list.append(screening_reminder)

    # health_metric_list = get_health_metrics(patient_id, smart_client)

    summary = {
        'total_immunizations': len(immunization_checklist),
        'completed_immunizations': len(immunization_checklist) - pending_immunizations,
        'total_screenings': len(screening_checklist),
        'completed_screenings': len(screening_checklist) - pending_screenings,
        'reminders': reminder_list,
    }

    return summary
