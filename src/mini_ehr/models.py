from pydantic import BaseModel, Field

class Visit(BaseModel):
    visit_id: str
    date: str
    type: str
    diagnosis: str | None = None
    treatment: str | None = None
    provider: str | None = None
    heart_rate: int | None = None
    temperature_f: float | None = None
    systolic_bp: int | None = None
    diastolic_bp: int | None = None

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
    
    def to_fhir_like_observations(self, patient_id: str) -> list[dict]:
        """
        Convert visit vitals into simplified FHIR-like Observation resources.
        """
        observations = []

        if self.heart_rate is not None:
            observations.append({
                "resourceType": "Observation",
                "id": f"observation-{self.visit_id}-heart-rate",
                "status": "final",
                "subject": {"reference": f"Patient/{patient_id}"},
                "encounter": {"reference": f"Encounter/{self.visit_id}"},
                "code": {"text": "Heart rate"},
                "valueQuality": {
                    "value": self.heart_rate,
                    "unit": "beats/minute",
                },
            })

        if self.temperature_f is not None:
            observations.append({
                "resourceType": "Observation",
                "id": f"observation-{self.visit_id}-temperature",
                "status": "final",
                "subject": {"reference": f"Patient/{patient_id}"},
                "encounter": {"reference": f"Encounter/{self.visit_id}"},
                "code": {"text": "Body temperature"},
                "valueQuantity": {
                    "value": self.temperature_f,
                    "unit": "degrees Fahrenheit",
                },
            })

        if self.systolic_bp is not None and self.diastolic_bp is not None:
            observations.append({
                "resourceType": "Observation",
                "id": f"observation-{self.visit_id}-blood-pressure",
                "status": "final",
                "subject": {"reference": f"Patient/{patient_id}"},
                "encounter": {"reference": f"Encounter/{self.visit_id}"},
                "code": {"text": "Blood pressure"},
                "component": [
                    {
                        "code": {"text": "Systolic blood pressure"},
                        "valueQuantity": {
                            "value": self.systolic_bp,
                            "unit": "mmHg",
                        },
                    },
                    {
                        "code": {"text": "Diastolic blood pressure"},
                        "valueQuantity": {
                            "value": self.diastolic_bp,
                            "unit": "mmHg",
                        },
                    },
                ],
            })

        return observations

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