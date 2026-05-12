from datetime import datetime, timezone

def create_audit_event(
        action: str,
        resource_type: str,
        resource_id: str,
        actor: str = "system",
) -> dict:
    """
    Create a simple audit event.
    
    This records who did what, to which resource and when.
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
    }

def detect_suspicious_audit_activity(events: list[dict]) -> list[dict]:
    """
    Detect simple suspicious audit patterns.
    
    Current rule:
    - more than 3 VIEW_PATIENT events for the same patient
    """
    alerts = []
    view_counts = {}
    actor_view_counts = {}

    for event in events:
        if event.get("action") != "VIEW_PATIENT":
            continue

        resource_id = event.get("resource_id")
        view_counts[resource_id] = view_counts.get(resource_id, 0) + 1

        actor = event.get("actor")
        actor_view_counts[actor] = actor_view_counts.get(actor, 0) + 1
    
    for resource_id, count in view_counts.items():
        if count > 3:
            alerts.append({
                "type": "REPEATED_PATIENT_ACCESS",
                "resource_type": "patient",
                "resource_id": resource_id,
                "message": f"Patient {resource_id} was viewed {count} times.",
            })
    
    for actor, count in actor_view_counts.items():
        if count > 5:
            alerts.append({
                "type": "HIGH_VOLUME_PATIENT_ACCESS",
                "actor": actor,
                "message": f"Actor {actor} viewed patient records {count} times",
            })
    
    return alerts

def build_audit_summary(events: list[dict]) -> dict:
    """
    Build summary counts from audit events.
    """
    counts_by_action = {}
    counts_by_actor = {}

    for event in events:
        action = event.get("action", "UNKNOWN")
        actor = event.get("actor", "UNKNOWN")

        counts_by_action[action] = counts_by_action.get(action, 0) + 1
        counts_by_actor[actor] = counts_by_actor.get(actor, 0) + 1

    return {
        "total_events": len(events),
        "counts_by_action": counts_by_action,
        "counts_by_actor": counts_by_actor,
    }