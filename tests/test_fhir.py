from mini_ehr.fhir import build_patient_fhir_bundle
from mini_ehr.models import Patient, Visit

def test_build_patient_fhir_bundle():
    patient = Patient(
        patient_id="P001",
        first_name="John",
        last_name="Doe",
        date_of_birth="1970-05-12",
        visits=[
            Visit(
                visit_id="V001",
                date="2026-05-04",
                type="ER",
                diagnosis="Hypertension",
                treatment="Medication review",
                provider="Dr. Smith",
            )
        ],
    )

    bundle = build_patient_fhir_bundle(patient)

    assert bundle["resourceType"] == "Bundle"

    resource_types = [
        entry["resource"]["resourceType"]
        for entry in bundle["entry"]
    ]

    assert "Patient" in resource_types
    assert "Encounter" in resource_types
    assert "Condition" in resource_types
    assert "Procedure" in resource_types