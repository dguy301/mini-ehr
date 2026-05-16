from fastapi import FastAPI, HTTPException, Header

from mini_ehr.audit import (
    build_audit_summary, 
    create_audit_event, 
    detect_suspicious_audit_activity,
)
from mini_ehr.audit_repository import AuditRepository
from mini_ehr.alerts import generate_alerts
from mini_ehr.config import get_audit_data_path
from mini_ehr.dashboard import build_dashboard_summary
from mini_ehr.models import Patient, Visit
from mini_ehr.repository import PatientRepository
from mini_ehr.config import get_patient_data_path
from mini_ehr.fhir import build_patient_fhir_bundle

app = FastAPI(title="Mini EHR Workflow System")

repo=PatientRepository(get_patient_data_path())
audit_repo = AuditRepository(get_audit_data_path())

def set_repository(test_repo: PatientRepository) -> None:
    """
    Replace the active repository.
    
    This is mainly used by tests so they can use temporary data files.
    """
    global repo
    repo = test_repo

def set_audit_repository(test_audit_repo: AuditRepository) -> None:
    """
    Replace the active audit repository.
    
    This is mainly used by tests so they can use temporary audit files.
    """
    global audit_repo
    audit_repo = test_audit_repo

def record_audit_event(
        action: str,
        resource_type: str,
        resource_id: str,
        actor: str = "api_user",
) -> dict:
    """
    Create and save an audit event.
    """
    audit_event = create_audit_event(
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        actor=actor,
    )
    audit_repo.add_event(audit_event)
    return audit_event

@app.get("/")
def root():
    return {"message": "Mini EHR Workflow System"}

@app.get("/patients")
def list_patients():
    return repo.list_patients()

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str, x_actor: str = Header(default="api_user")):
    patient = repo.get_patient(patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    record_audit_event(
        action="VIEW_PATIENT",
        resource_type="patient",
        resource_id=patient_id,
        actor=x_actor,
    )
    
    return patient

@app.post("/patients")
def add_patient(patient: Patient, x_actor: str = Header(default="api_user")):
    try:
        saved_patient = repo.add_patient(patient)

        record_audit_event(
            action="CREATE_PATIENT",
            resource_type="patient",
            resource_id=patient.patient_id,
            actor=x_actor,
        )

        return saved_patient
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@app.post("/patients/{patient_id}/visits")
def add_visit(patient_id: str, visit: Visit, x_actor: str = Header(default="api_user")):
    try:
        saved_visit = repo.add_visit(patient_id, visit)

        record_audit_event(
            action="ADD_VISIT",
            resource_type="visit",
            resource_id=visit.visit_id,
            actor=x_actor,
        )

        return saved_visit
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    
@app.get("/patients/{patient_id}/alerts")
def get_patient_alerts(patient_id: str):
    patient = repo.get_patient(patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return generate_alerts(patient)

@app.get("/patients/{patient_id}/fhir")
def get_patient_fhir(patient_id: str):
    patient_data = repo.get_patient(patient_id)

    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = Patient(**patient_data)

    record_audit_event(
        action="VIEW_PATIENT_FHIR",
        resource_type="patient",
        resource_id=patient_id,
    )

    return patient.to_fhir_like()

@app.get("/patients/{patient_id}/fhir/encounters")
def get_patient_fhir_encounters(patient_id: str):
    patient_data = repo.get_patient(patient_id)

    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = Patient(**patient_data)

    record_audit_event(
        action="VIEW_PATIENT_FHIR_ENCOUNTERS",
        resource_type="patient",
        resource_id=patient_id,
    )

    return [
        visit.to_fhir_like_encounter(patient_id=patient_id)
        for visit in patient.visits
    ]

@app.get("/patients/{patient_id}/fhir/conditions")
def get_patient_fhir_conditions(patient_id: str):
    patient_data = repo.get_patient(patient_id)

    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = Patient(**patient_data)

    record_audit_event(
        action="VIEW_PATIENT_FHIR_CONDITIONS",
        resource_type="patient",
        resource_id=patient_id,
    )

    conditions = [
        visit.to_fhir_like_condition(patient_id=patient_id)
        for visit in patient.visits
    ]

    return [
        condition
        for condition in conditions
        if condition is not None
    ]

@app.get("/patients/{patient_id}/fhir/bundle")
def get_patient_fhir_bundle(patient_id: str):
    patient_data = repo.get_patient(patient_id)

    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = Patient(**patient_data)

    record_audit_event(
        action="VIEW_PATIENT_FHIR_BUNDLE",
        resource_type="patient",
        resource_id=patient_id,
    )

    return build_patient_fhir_bundle(patient)

@app.get("/patients/{patient_id}/fhir/observations")
def get_patient_fhir_observations(patient_id: str):
    patient_data = repo.get_patient(patient_id)

    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = Patient(**patient_data)

    record_audit_event(
        action="VIEW_PATIENT_FHIR_OBSERVATIONS",
        resource_type="patient",
        resource_id=patient_id,
    )

    observations = []

    for visit in patient.visits:
        observations.extend(
            visit.to_fhir_like_observations(patient_id=patient_id)
        )
    
    return observations

@app.get("/patients/{patient_id}/fhir/medications")
def get_patient_fhir_medications(patient_id: str):
    patient_data = repo.get_patient(patient_id)

    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = Patient(**patient_data)

    record_audit_event(
        action="VIEW_PATIENT_FHIR_MEDICATIONS",
        resource_type="patient",
        resource_id=patient_id,
    )

    medications = []

    for visit in patient.visits:
        medications.extend(
            visit.to_fhir_like_medication_statements(
                patient_id=patient_id
            )
        )

    return medications

@app.get("/dashboard/summary")
def get_dashboard_summary():
    patients = repo.list_patients()
    return build_dashboard_summary(patients)

@app.get("/audit/events")
def list_audit_events(action: str | None = None, actor: str | None = None):
    events = audit_repo.list_events()

    if action:
        events = [
            event for event in events
            if event.get("action") == action
        ]
    
    if actor:
        events = [
            event for event in events
            if event.get("actor") == actor
        ]
    
    return events

@app.get("/audit/alerts")
def list_audit_alerts():
    events = audit_repo.list_events()
    return detect_suspicious_audit_activity(events)

@app.get("/audit/summary")
def get_audit_summary():
    events = audit_repo.list_events()
    return build_audit_summary(events)