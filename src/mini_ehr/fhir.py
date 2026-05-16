from mini_ehr.models import Patient

def build_patient_fhir_bundle(patient: Patient) -> dict:
    """
    Build a simplified FHIR-like bundle for a patient.
    """
    resources = [patient.to_fhir_like()]

    resources.extend([
        visit.to_fhir_like_encounter(patient_id=patient.patient_id)
        for visit in patient.visits
    ])

    for visit in patient.visits:
        resources.extend(
            visit.to_fhir_like_observations(
                patient_id=patient.patient_id
            )
        )

    resources.extend([
        condition
        for visit in patient.visits
        if (
            condition := visit.to_fhir_like_condition(
                patient_id=patient.patient_id
            )
        ) is not None
    ])

    resources.extend([
        procedure
        for visit in patient.visits
        if (
            procedure := visit.to_fhir_like_procedure(
                patient_id=patient.patient_id
            )
        ) is not None
    ])

    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {"resource": resource}
            for resource in resources
        ],
    }