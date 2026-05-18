def build_dashboard_summary(patients: list[dict]) -> dict:
    """
    Build a simple dashboard summary from patient records.
    """

    total_patients = len(patients)
    total_visits = 0
    total_er_visits = 0
    total_medication_entries = 0
    patients_with_medications = 0

    for patient in patients:
        visits = patient.get("visits", [])
        patient_has_medications = False
        total_visits += len(visits)

        for visit in visits:
            if visit.get("type") == "ER":
                total_er_visits += 1
            
            medications = visit.get("medications", [])
            total_medication_entries += len(medications)

            if medications:
                patient_has_medications = True
        
        if patient_has_medications:
            patients_with_medications += 1
    
    return {
        "total_patients": total_patients,
        "total_visits": total_visits,
        "total_er_visits": total_er_visits,
        "total_medication_entries": total_medication_entries,
        "patients_with_medications": patients_with_medications,
    }