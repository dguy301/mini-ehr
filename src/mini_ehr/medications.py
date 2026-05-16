def build_medication_summary(patient: dict) -> dict:
    """
    Build a medication summary for a patient.
    """
    medication_counts = {}

    for visit in patient.get("visits", []):
        for medication in visit.get("medications", []):
            normalized = medication.strip().lower()
            medication_counts[normalized] = medication_counts.get(normalized, 0) + 1
            
    return {
        "patient_id": patient.get("patient_id"),
        "total_medications": sum(medication_counts.values()),
        "unique_medications": len(medication_counts),
        "medication_counts": medication_counts,
    }