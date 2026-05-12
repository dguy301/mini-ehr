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
    
    return alerts