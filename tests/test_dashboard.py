from mini_ehr.dashboard import build_dashboard_summary

def test_dashboard_summary_empty():
    summary = build_dashboard_summary([])

    assert summary["total_patients"] == 0
    assert summary["total_visits"] == 0
    assert summary["total_er_visits"] == 0

def test_dashboard_summary_counts_patients_and_visits():
    patients = [
        {
            "patient_id": "P001",
            "visits": [
                {"visit_id": "V001", "type": "ER"},
                {"visit_id": "V002", "type": "Primary Care"},
            ]
        },
        {
            "patient_id": "P002",
            "visits": [
                {"visit_id": "V003", "type": "ER"},
            ]
        }
    ]

    summary = build_dashboard_summary(patients)

    assert summary["total_patients"] == 2
    assert summary["total_visits"] == 3
    assert summary["total_er_visits"] == 2