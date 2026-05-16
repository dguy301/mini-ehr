def generate_alerts(patient: dict) -> list[dict]:
    """
    Generate alerts for a patient record.
    Alerts help identify missing or unusual healthcare data.
    """
    alerts = []
    visits = patient.get("visits", [])

    if not visits:
        alerts.append({
            "type": "NO_VISITS",
            "message": "Patient has no visit history.",
        })

    for visit in visits:
        if not visit.get("diagnosis"):
            alerts.append({
                "type": "MISSING_DIAGNOSIS",
                "message": f"Visit {visit.get('visit_id')} is missing a diagnosis.",
            })

        if not visit.get("treatment"):
            alerts.append({
                "type": "MISSING_TREATMENT",
                "message": f"Visit {visit.get('visit_id')} is missing treatment information.",
            })
        
        if not visit.get("provider"):
            alerts.append({
                "type": "MISSING_PROVIDER",
                "message": f"Visit {visit.get('visit_id')} is missing provider information.",
            })
        
    er_visits = [
        visit for visit in visits
        if visit.get("type") == "ER"
    ]

    if len(er_visits) > 2:
        alerts.append({
            "type": "FREQUENT_ER_VISITS",
            "message": "Patient has more than 2 ER visits recorded.",
        })

    alerts.extend(generate_vital_sign_alerts(patient))
    alerts.extend(generate_medication_alerts(patient))
    
    return alerts

def generate_vital_sign_alerts(patient: dict) -> list[dict]:
    """
    Generate alerts for abnormal vital signs.
    """
    alerts = []

    for visit in patient.get("visits", []):
        visit_id = visit.get("visit_id")

        heart_rate = visit.get("heart_rate")
        if heart_rate is not None and heart_rate > 120:
            alerts.append({
                "type": "HIGH_HEART_RATE",
                "visit_id": visit_id,
                "message": f"Heart rate {heart_rate} exceeds threshold.",
            })

        temperature = visit.get("temperature_f")
        if temperature is not None and temperature >= 100.4:
            alerts.append({
                "type": "FEVER",
                "visit_id": visit_id,
                "message": f"Temperature {temperature} indicates fever.",
            })

        systolic = visit.get("systolic_bp")
        if systolic is not None and systolic >= 140:
            alerts.append({
                "type": "HIGH_BLOOD_PRESSURE",
                "visit_id": visit_id,
                "message": f"Systolic blood pressure {systolic} is elevated.",
            })

    return alerts

def generate_medication_alerts(patient: dict) -> list[dict]:
    """
    Generate alerts for medication-related issues.
    """
    alerts = []

    for visit in patient.get("visits", []):
        visit_id = visit.get("visit_id")
        medications = visit.get("medications", [])
        normalized = [med.lower() for med in medications]

        duplicates = {
            med
            for med in normalized
            if normalized.count(med) > 1
        }

        for duplicate in duplicates:
            alerts.append({
                "type": "DUPLICATE_MEDICATION",
                "visit_id": visit_id,
                "medication": duplicate,
                "message": f"Medication {duplicate} appears more than once.",
            })
        
    return alerts