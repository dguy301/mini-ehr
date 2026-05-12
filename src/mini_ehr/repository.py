import json
from pathlib import Path

from mini_ehr.models import Patient, Visit

class PatientRepository:
    """
    Handles reading and writing patient data to a JSON file.
    This simulates a very simple persistence layer (like a database).
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def _load(self) -> list:
        """load all patients from file."""
        if not self.file_path.exists():
            return []
        
        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
        
    def _save(self, patients: list) -> None:
        """Save all patients to file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(patients, f, indent=2)

    def list_patients(self) -> list:
        """Return all patients."""
        return self._load()
    
    def get_patient(self, patient_id: str) -> dict | None:
        """Return a single patient by ID."""
        patients = self._load()

        for patient in patients:
            if patient["patient_id"] == patient_id:
                return patient
        
        return None   
    
    def add_patient(self, patient: Patient):
        """
        Add a new patient.

        Raises:
            ValueError: if patient_id already exists.
        """
        patients = self._load()

        if self.get_patient(patient.patient_id):
            raise ValueError(f"Patient {patient.patient_id} already exists")
        
        patient_dict = patient.model_dump()
        patients.append(patient_dict)
        self._save(patients)

        return patient_dict
    
    def add_visit(self, patient_id: str, visit: Visit) -> dict:
        """
        Add a visit to an existing patient.
        
        Raises:
            ValueError: if patient does not exist.
        """
        patients = self._load()

        for patient in patients:
            if patient["patient_id"] == patient_id:
                visit_dict = visit.model_dump()
                patient.setdefault("visits", [])
                patient["visits"].append(visit_dict)
                self._save(patients)

                return visit_dict
        
        raise ValueError(f"Patient {patient_id} not found")