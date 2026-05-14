from pydantic import BaseModel, Field

class Visit(BaseModel):
    visit_id: str
    date: str
    type: str
    diagnosis: str | None = None
    treatment: str | None = None
    provider: str | None = None

    def to_fhir_like_encounter(self, patient_id: str) -> dict:
        """
        Convert this visit into a simplified FHIR-like Encounter resource.
        """
        return {
            "resourceType": "Encounter",
            "id": self.visit_id,
            "status": "finished",
            "class": {
                "display": self.type,
            },
            "subject": {
                "reference": f"Patient/{patient_id}",
            },
            "period": {
                "start": self.date,
            },
        }
    
    def to_fhir_like_condition(self, patient_id: str) -> dict | None:
        """
        Convert the visit diagnosis into a simplified FHIR-like Condition resource.
        
        Returns None if no diagnosis exists.
        """
        if not self.diagnosis:
            return None
        
        return {
            "resourceType": "Condition",
            "id": f"condition-{self.visit_id}",
            "subject": {
                "reference": f"Patient/{patient_id}",
            },
            "code": {
                "text": self.diagnosis,
            },
            "encounter": {
                "reference": f"Encounter/{self.visit_id}",
            },
        }
    
    def to_fhir_like_procedure(self, patient_id: str) -> dict | None:
        """
        Convert the visit treatment into a simplified FHIR-like Procedure resource.
        
        Returns None if no treatment exists.
        """
        if not self.treatment:
            return None
        
        return {
            "resourceType": "Procedure",
            "id": f"procedure-{self.visit_id}",
            "status": "completed",
            "subject": {
                "reference": f"Patient/{patient_id}",
            },
            "encounter": {
                "reference": f"Encounter/{self.visit_id}",
            },
            "code": {
                "text": self.treatment,
            },
        }

class Patient(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    visits: list[Visit] = Field(default_factory=list)

    def to_fhir_like(self) -> dict:
        """
        Convert this patient into a simplified FHIR-like Patient resource.
        """
        return {
            "resourceType": "Patient",
            "id": self.patient_id,
            "name": [
                {
                    "given": [self.first_name],
                    "family": self.last_name,
                }
            ],
            "birthDate": self.date_of_birth
        }