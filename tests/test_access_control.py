from mini_ehr.access_control import has_permission

def test_admin_can_create_patient():
    assert has_permission("admin", "CREATE_PATIENT") is True

def test_clinician_can_add_visit():
    assert has_permission("clinician", "ADD_VISIT") is True

def test_analyst_cannot_create_patient():
    assert has_permission("analyst", "CREATE_PATIENT") is False

def test_unknown_role_has_no_permissions():
    assert has_permission("unknown", "VIEW_PATIENT") is False