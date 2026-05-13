import pytest

from mini_ehr.repository import PatientRepository
from mini_ehr.models import Patient, Visit


def test_list_patients_empty():
    repo = PatientRepository("data/patients.json")
    patients = repo.list_patients()

    assert isinstance(patients, list)

def test_add_patient(tmp_path):
    file_path = tmp_path / "patients.json"
    repo = PatientRepository(str(file_path))

    patient = Patient(
        patient_id="P001",
        first_name="John",
        last_name="Doe",
        date_of_birth="1970-05-12",
    )

    saved = repo.add_patient(patient)

    assert saved["patient_id"] == "P001"
    assert saved["first_name"] == "John"

    all_patients = repo.list_patients()
    assert len(all_patients) == 1

def test_add_duplicate_patient_fails(tmp_path):
    file_path = tmp_path / "patients.json"
    repo = PatientRepository(str(file_path))

    patient = Patient(
        patient_id="P001",
        first_name="John",
        last_name="Doe",
        date_of_birth="1970-05-12",
    )

    repo.add_patient(patient)

    with pytest.raises(ValueError):
        repo.add_patient(patient)

def test_add_visit_to_patient(tmp_path):
    file_path = tmp_path / "patients.json"
    repo = PatientRepository(str(file_path))

    patient = Patient(
        patient_id="P001",
        first_name="John",
        last_name="Doe",
        date_of_birth="1970-05-12",
    )

    repo.add_patient(patient)

    visit = Visit(
        visit_id="V001",
        date="2026-05-04",
        type="Primary Care",
        diagnosis="Hypertension",
        treatment="Medication review",
        provider="Dr. Smith",
    )

    saved_visit = repo.add_visit("P001", visit)

    assert saved_visit["visit_id"] == "V001"

    saved_patient = repo.get_patient("P001")
    assert len(saved_patient["visits"]) == 1
    assert saved_patient["visits"][0]["diagnosis"] == "Hypertension"

def test_add_visit_to_missing_patient_fails(tmp_path):
    file_path = tmp_path / "patients.json"
    repo = PatientRepository(str(file_path))

    visit = Visit(
        visit_id="V001",
        date="2026-05-04",
        type="ER",
    )

    with pytest.raises(ValueError):
        repo.add_visit("P999", visit)

def test_patient_can_convert_to_fhir_like_resource():
    patient = Patient(
        patient_id="P001",
        first_name="John",
        last_name="Doe",
        date_of_birth="1970-05-12",
    )

    resource = patient.to_fhir_like()

    assert resource["resourceType"] == "Patient"
    assert resource["id"] == "P001"
    assert resource["name"][0]["given"] == ["John"]
    assert resource["name"][0]["family"] == "Doe"
    assert resource["birthDate"] == "1970-05-12"

def test_visit_can_convert_to_fhir_like_encounter():
    visit = Visit(
        visit_id="V001",
        date="2026-05-04",
        type="ER",
        diagnosis="Hypertension",
        treatment="Medication review",
        provider="Dr. Smith",
    )

    resource = visit.to_fhir_like_encounter(patient_id="P001")

    assert resource["resourceType"] == "Encounter"
    assert resource["id"] == "V001"
    assert resource["status"] == "finished"
    assert resource["class"]["display"] == "ER"
    assert resource["subject"]["reference"] == "Patient/P001"
    assert resource["period"]["start"] == "2026-05-04"

def test_visit_can_convert_to_fhir_like_condition():
    visit = Visit(
        visit_id="V001",
        date="2026-05-04",
        type="ER",
        diagnosis="Hypertension",
        treatment="Medication review",
        provider="Dr. Smith",
    )

    resource = visit.to_fhir_like_condition(patient_id="P001")

    assert resource["resourceType"] == "Condition"
    assert resource["id"] == "condition-V001"
    assert resource["subject"]["reference"] == "Patient/P001"
    assert resource["code"]["text"] == "Hypertension"
    assert resource["encounter"]["reference"] == "Encounter/V001"

def test_visit_without_diagnosis_returns_no_condition():
    visit = Visit(
        visit_id="V001",
        date="2026-05-04",
        type="ER",
    )

    resource = visit.to_fhir_like_condition(patient_id="P001")

    assert resource is None