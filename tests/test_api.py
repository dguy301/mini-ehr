from fastapi.testclient import TestClient

from mini_ehr.main import app
from mini_ehr.main import set_repository
from mini_ehr.main import set_audit_repository
from mini_ehr.audit_repository import AuditRepository
from mini_ehr.repository import PatientRepository

#import os
import pytest

@pytest.fixture(autouse=True)
def use_temp_repository(tmp_path):
    file_path = tmp_path / "patients.json"
    test_repo = PatientRepository(str(file_path))
    set_repository(test_repo)

    audit_file_path = tmp_path / "audit_log.json"
    test_audit_repo = AuditRepository(str(audit_file_path))
    set_audit_repository(test_audit_repo)

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Mini EHR Workflow System"}

def test_list_patients_endpoint():
    response = client.get("/patients")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_missing_patient_returns_404():
    response = client.get("/patients/P999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"

def twst_add_patient_endpoint():
    response = client.post(
        "/patients",
        json={
            "patient_id": "P001",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1970-05-12",
            "visits": [],
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["patient_id"] == "P001"
    assert data["first_name"] == "John"

def test_add_duplicate_patient_returns_400():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }

    first_response = client.post("/patients", json=patient)
    second_response = client.post("/patients", json=patient)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert "already exists" in second_response.json()["detail"]

def test_add_visit_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
    }

    response = client.post("/patients/P99/visits", json=visit)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_patient_alerts_endpoint_for_missing_visit_fields():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "disgnosis": None,
        "treatment":None,
        "provider": None,
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/patients/P001/alerts")

    assert response.status_code == 200

    alert_types = [alert["type"] for alert in response.json()]

    assert "MISSING_DIAGNOSIS" in alert_types
    assert "MISSING_TREATMENT" in alert_types
    assert "MISSING_PROVIDER" in alert_types

def test_patient_alerts_for_missing_patient_returns_404():
    response = client.get("/patients/P999/alerts")

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"

def test_dashboard_summary_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "disgnosis": "Hypertension",
        "treatment":"Medication review",
        "provider": "Dr. Smith",
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/dashboard/summary")

    assert response.status_code == 200
    assert response.json()["total_patients"] == 1
    assert response.json()["total_visits"] == 1
    assert response.json()["total_er_visits"] == 1

def test_get_patient_writes_audit_event(tmp_path):
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    response = client.get("/patients/P001")

    assert response.status_code == 200

def test_list_audit_events_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)
    client.get("/patients/P001")

    response = client.get("/audit/events")

    assert response.status_code == 200

    events = response.json()
    actions = [event["action"] for event in events]

    assert "CREATE_PATIENT" in actions
    assert "VIEW_PATIENT" in actions

def test_add_visit_writes_audit_event():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/audit/events")
    actions = [event["action"] for event in response.json()]

    assert "ADD_VISIT" in actions

def test_audit_alerts_endpoint_detects_repeated_patient_access():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    client.get("/patients/P001")
    client.get("/patients/P001")
    client.get("/patients/P001")
    client.get("/patients/P001")

    response = client.get("/audit/alerts")

    assert response.status_code == 200

    alerts = response.json()
    assert len(alerts) == 1
    assert alerts[0]["type"] == "REPEATED_PATIENT_ACCESS"
    assert alerts[0]["resource_id"] == "P001"

def test_list_audit_events_can_filter_by_action():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)
    client.get("/patients/P001")

    response = client.get("/audit/events?action=VIEW_PATIENT")

    assert response.status_code == 200

    events = response.json()
    assert len(events) == 1
    assert events[0]["action"] == "VIEW_PATIENT"

def test_list_audit_events_can_filter_by_actor():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)
    client.get("/patients/P001")

    response = client.get("/audit/events?actor=api_user")

    assert response.status_code == 200

    events = response.json()
    assert len(events) >= 1
    assert all(event["actor"] == "api_user" for event in events)

def test_actor_header_is_recorded_in_audit_event():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }

    client.post(
        "/patients",
        json=patient,
        headers={"X-Actor": "analyst_001"},
    )

    response = client.get("/audit/events?actor=analyst_001")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["actor"] == "analyst_001"

def test_audit_summary_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post(
        "/patients",
        json=patient,
        headers={"X-Actor": "admin_001"},
    )

    client.get(
        "/patients/P001",
        headers={"X-Actor": "analyst_001"},
    )

    response = client.get("/audit/summary")

    assert response.status_code == 200

    summary = response.json()
    assert summary["total_events"] == 2
    assert summary["counts_by_action"]["CREATE_PATIENT"] == 1
    assert summary["counts_by_action"]["VIEW_PATIENT"] == 1
    assert summary["counts_by_actor"]["admin_001"] == 1
    assert summary["counts_by_actor"]["analyst_001"] == 1

def test_get_patient_fhir_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }

    client.post("/patients", json=patient)

    response = client.get("/patients/P001/fhir")

    assert response.status_code == 200

    resource = response.json()

    assert resource["resourceType"] == "Patient"
    assert resource["id"] == "P001"
    assert resource["name"][0]["given"] == ["John"]
    assert resource["name"][0]["family"] == "Doe"

def test_get_patient_fhir_encounters_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/patients/P001/fhir/encounters")

    assert response.status_code == 200

    resources = response.json()
    assert len(resources) == 1
    assert resources[0]["resourceType"] == "Encounter"
    assert resources[0]["id"] == "V001"
    assert resources[0]["subject"]["reference"] == "Patient/P001"

def test_get_patient_fhir_conditions_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/patients/P001/fhir/conditions")

    assert response.status_code == 200

    resources = response.json()
    assert len(resources) == 1
    assert resources[0]["resourceType"] == "Condition"
    assert resources[0]["code"]["text"] == "Hypertension"
    assert resources[0]["subject"]["reference"] == "Patient/P001"
    assert resources[0]["encounter"]["reference"] == "Encounter/V001"

def test_get_patient_fhir_bundle_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/patients/P001/fhir/bundle")

    assert response.status_code == 200

    bundle = response.json()
    
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"

    resource_types = [
        entry["resource"]["resourceType"]
        for entry in bundle["entry"]
    ]

    assert "Patient" in resource_types
    assert "Encounter" in resource_types
    assert "Condition" in resource_types
    assert "Procedure" in resource_types

def test_get_patient_fhir_observations_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "ER",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
        "heart_rate": 88,
        "temperature_f": 98.6,
        "systolic_bp": 130,
        "diastolic_bp": 84,
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/patients/P001/fhir/observations")

    assert response.status_code == 200

    resources = response.json()
    assert len(resources) == 3

    codes = [
        resource["code"]["text"]
        for resource in resources
    ]

    assert "Heart rate" in codes
    assert "Body temperature" in codes
    assert "Blood pressure" in codes

def test_get_patient_fhir_medications_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "Primary Care",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
        "medications": ["Lisinopril", "Metformin"],
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/patients/P001/fhir/medications")

    assert response.status_code == 200

    resources = response.json()
    assert len(resources) == 2
    assert resources[0]["resourceType"] == "MedicationStatement"
    assert resources[0]["medicationCodeableConcept"]["text"] == "Lisinopril"
    assert resources[1]["medicationCodeableConcept"]["text"] == "Metformin"
    assert resources[0]["subject"]["reference"] == "Patient/P001"

def test_get_patient_medication_summary_endpoint():
    patient = {
        "patient_id": "P001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-05-12",
        "visits": [],
    }
    client.post("/patients", json=patient)

    visit = {
        "visit_id": "V001",
        "date": "2026-05-04",
        "type": "Primary Care",
        "diagnosis": "Hypertension",
        "treatment": "Medication review",
        "provider": "Dr. Smith",
        "medications": ["Lisinopril", "Metformin", "lisinopril"],
    }
    client.post("/patients/P001/visits", json=visit)

    response = client.get("/patients/P001/medications/summary")

    assert response.status_code == 200

    summary = response.json()
    assert summary["patient_id"] == "P001"
    assert summary["total_medications"] == 3
    assert summary["unique_medications"] == 2
    assert summary["medication_counts"]["lisinopril"] == 2
    assert summary["medication_counts"]["metformin"] == 1