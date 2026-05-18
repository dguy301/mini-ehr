ROLE_PERMISSIONS = {
    "admin": {
        "CREATE_PATIENT",
        "VIEW_PATIENT",
        "ADD_VISIT",
        "VIEW_AUDIT_EVENTS",
        "VIEW_AUDIT_SUMMARY",
    },
    "clinician": {
        "CREATE_PATIENT",
        "VIEW_PATIENT",
        "ADD_VISIT",
    },
    "analyst": {
        "VIEW_PATIENT",
        "VIEW_AUDIT_SUMMARY",
    },
    "auditor": {
        "VIEW_AUDIT_EVENTS",
        "VIEW_AUDIT_SUMMARY",
    },
}

def has_permission(role: str, action: str) -> bool:
    """
    Retuen True if a role is allowed to perform an action.
    """
    permissions = ROLE_PERMISSIONS.get(role, set())
    return action in permissions