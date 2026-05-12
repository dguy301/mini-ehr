from mini_ehr.dashboard import build_dashboard_summary

def test_dashboard_summary_contains_expected_keys():
    summary = build_dashboard_summary([])

    assert "total_patients" in summary
    assert "total_visits" in summary
    assert "total_er_visits" in summary

def test_dashboard_summary_values_are_zero_for_empty_data():
    summary = build_dashboard_summary([])

    assert summary["total_patients"] == 0
    assert summary["total_visits"] == 0
    assert summary["total_er_visits"] == 0