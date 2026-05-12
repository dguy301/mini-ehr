import json
from pathlib import Path

class AuditRepository:
    """
    Handles reading and writing audit events to a JSON file.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def _load(self) -> list:
        if not self.file_path.exists():
            return []
        
        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
        
    def _save(self, events: list) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

    def list_events(self) -> list:
        return self._load()
    
    def add_event(self, event: dict) -> dict:
        events = self._load()
        events.append(event)
        self._save(events)
        return event