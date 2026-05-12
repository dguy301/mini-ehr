from mini_ehr.audit import create_audit_event, build_audit_summary
from mini_ehr.audit import detect_suspicious_audit_activity

def test_create_audit_event():
    event = create_audit_event(
        action="VIEW_PATIENT",
        resource_type="patient",
        resource_id="P001",
        actor="tester",
    )

    assert event["actor"] == "tester"
    assert event["action"] == "VIEW_PATIENT"
    assert event["resource_type"] == "patient"
    assert event["resource_id"] == "P001"
    assert "timestamp" in event

def test_repeated_patient_access_detected():
    events = [
        {"action": "VIEW_PATIENT", "resource_id": "P001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001"},
    ]

    alerts = detect_suspicious_audit_activity(events)

    assert len(alerts) == 1
    assert alerts[0]["type"] == "REPEATED_PATIENT_ACCESS"
    assert alerts[0]["resource_id"] == "P001"

def test_repeated_patient_access_not_detected_under_threshold():
    events = [
        {"action": "VIEW_PATIENT", "resource_id": "P001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001"},
    ]

    alerts = detect_suspicious_audit_activity(events)

    assert alerts == []

def test_high_volume_patient_access_by_actor_detected():
    events = [
        {"action": "VIEW_PATIENT", "resource_id": "P001", "actor": "analyst_001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001", "actor": "analyst_001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001", "actor": "analyst_001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001", "actor": "analyst_001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001", "actor": "analyst_001"},
        {"action": "VIEW_PATIENT", "resource_id": "P001", "actor": "analyst_001"},
    ]

    alerts = detect_suspicious_audit_activity(events)

    assert any(
        alert["type"] == "HIGH_VOLUME_PATIENT_ACCESS"
        for alert in alerts
    )

def test_build_audit_summary():
    events = [
        {"action": "VIEW_PATIENT", "actor": "analyst_001"},
        {"action": "VIEW_PATIENT", "actor": "analyst_001"},
        {"action": "CREATE_PATIENT", "actor": "admin_001"},
    ]

    summary = build_audit_summary(events)

    assert summary["total_events"] == 3
    assert summary["counts_by_action"]["VIEW_PATIENT"] == 2
    assert summary["counts_by_action"]["CREATE_PATIENT"] == 1
    assert summary["counts_by_actor"]["analyst_001"] == 2
    assert summary["counts_by_actor"]["admin_001"] == 1
