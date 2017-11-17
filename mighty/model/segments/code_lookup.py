immunization_lookup = {
    'Flu Shot': {
        'system': 'http://hl7.org/fhir/sid/cvx',
        'code': '140',
        'disease': 'Influenza (seasonal)'
    },
    'Td Booster': {
        'system': 'http://hl7.org/fhir/sid/cvx',
        'code': '113',
        'disease': 'Tetanus/diphtheria'
    },
    'Tdap Booster': {
        'system': 'http://hl7.org/fhir/sid/cvx',
        'code': '115',
        'disease': 'Tetanus/diphtheria/pertussis'
    },
    'HPV': {
        'system': 'http://hl7.org/fhir/sid/cvx',
        'code': '62',
        'disease': 'Human papilloma virus'
    },
    'Chickenpox': {
        'system': 'http://hl7.org/fhir/sid/cvx',
        'code': '21',
        'disease': 'Varicella'
    },
    'MMR': {
        'system': 'http://hl7.org/fhir/sid/cvx',
        'code': '03',
        'disease': 'Measles, Mumps, Rubella'
    },
}

health_metric_lookup = {
    'Blood Pressure': {
        'code': '55284-4'
    },
    'Systolic Blood Pressure': {
        'code': '8480-6'
    },
    'Diastolic Blood Pressure': {
        'code': '8462-4'
    },
    'Total Cholesterol': {
        'code': '2093-3'
    },
    'Glucose': {
        'code': '2339-0'
    },
    'Body Mass Index': {
        'code' : '39156-5'
    },
    'Body Height': {
        'code' : '8302-2'
    },
    'Body Weight': {
        'code' : '29463-7'
    }
}

condition_lookup = {
    'Diabetes': {
        'system': 'SNOMED-CT',
        'code': '44054006'
    },
    'Coronary Heart Disease': {
        'system': 'SNOMED-CT',
        'code': '53741008'
    }
}
