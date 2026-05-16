from mini_ehr.medications import build_medication_summary

def test_build_medication_summary():
    patient = {
        "patient_id": "P001",
        "visits": [
            {
                "visit_id": "V001",
                "medications": ["lisinopril", "metformin"],
            },
            {
                "visit_id": "V002",
                "medications": ["lisinopril"],
            },
        ],
    }

    summary = build_medication_summary(patient)

    assert summary["patient_id"] == "P001"
    assert summary["total_medications"] == 3
    assert summary["unique_medications"] == 2
    assert summary["medication_counts"]["lisinopril"] == 2
    assert summary["medication_counts"]["metformin"] == 1