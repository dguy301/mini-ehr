from mini_ehr.alerts import generate_alerts, generate_vital_sign_alerts

def test_patient_with_no_visits_gets_alert():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }

    alerts = generate_alerts(patient)

    assert len(alerts) == 1
    assert alerts[0]["type"] == "NO_VISITS"

def test_missing_diagnolsis_gets_alert():
    patient = {
        "patient_id": "P001",
        "visits": [
            {
                "viksit_id": "V001",
                "date": "2026-05-04",
                "type": "Primary Care",
                "diagnosis": None,
                "treatment": "Medication_review",
                "provider": "Dr. Smith",
            }
        ]
    }

    alerts = generate_alerts(patient)

    assert any(alert["type"] == "MISSING_DIAGNOSIS" for alert in alerts)

def test_missing_treatment_gets_alert():
    patient = {
        "patient_id": "P001",
        "visits": [
            {
                "viksit_id": "V001",
                "date": "2026-05-04",
                "type": "Primary Care",
                "diagnosis": "Hypertension",
                "treatment": None,
                "provider": "Dr. Smith",
            }
        ]
    }

    alerts = generate_alerts(patient)

    assert any(alert["type"] == "MISSING_TREATMENT" for alert in alerts)

def test_frequent_er_visits_gets_alert():
    patient = {
        "patient_id": "P001",
        "visits": [
            {"visit_id": "V001", "type": "ER"},
            {"visit_id": "V002", "type": "ER"},
            {"visit_id": "V003", "type": "ER"},
        ]
    }

    alerts = generate_alerts(patient)

    assert any(alert["type"] == "FREQUENT_ER_VISITS" for alert in alerts)

def test_high_heart_rate_alert():
    patient = {
        "patient_id": "P001",
        "visits": [
            {
                "visit_id": "V001",
                "heart_rate": 130,
            }
        ],
    }

    alerts = generate_vital_sign_alerts(patient)

    assert any(
        alert["type"] == "HIGH_HEART_RATE"
        for alert in alerts
    )

def test_fever_alert():
    patient = {
        "patient_id": "P001",
        "visits": [
            {
                "visit_id": "V001",
                "temperature_f": 101.2, 
            }
        ]
    }

    alerts = generate_vital_sign_alerts(patient)

    assert any(
        alert["type"] == "FEVER"
        for alert in alerts
    )

def test_high_blood_pressure_alert():
    patient = {
        "patient_id": "P001",
        "visits": [
            {
                "visit_id": "V001",
                "systolic_bp": 160,
            },
        ]
    }

    alerts = generate_vital_sign_alerts(patient)

    assert any(
        alert["type"] == "HIGH_BLOOD_PRESSURE"
        for alert in alerts
    )