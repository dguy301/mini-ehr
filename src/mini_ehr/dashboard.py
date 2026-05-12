def build_dashboard_summary(patients: list[dict]) -> dict:
    """
    Build a simple dashboard summary from patient records.
    """

    total_patients = len(patients)
    total_visits = 0
    total_er_visits = 0

    for patient in patients:
        visits = patient.get("visits", [])
        total_visits += len(visits)

        for visit in visits:
            if visit.get("type") == "ER":
                total_er_visits += 1
    
    return {
        "total_patients": total_patients,
        "total_visits": total_visits,
        "total_er_visits": total_er_visits
    }