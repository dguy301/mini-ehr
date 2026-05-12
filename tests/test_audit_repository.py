from mini_ehr.audit import create_audit_event
from mini_ehr.audit_repository import AuditRepository

def test_list_events_empty(tmp_path):
    file_path = tmp_path / "audits.json"
    repo = AuditRepository(str(file_path))

    assert repo.list_events() == []

def test_ass_audit_event(tmp_path):
    file_path = tmp_path / "audit.json"
    repo = AuditRepository(str(file_path))

    event = create_audit_event(
        action="VIEW_PATIENT",
        resource_type="patient",
        resource_id="P001",
        actor="tester",
    )

    saved = repo.add_event(event)

    assert saved["action"] == "VIEW_PATIENT"

    events = repo.list_events()
    assert len(events) == 1
    assert events[0]["resource_id"] == "P001"