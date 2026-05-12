from pydantic import BaseModel, Field

class Visit(BaseModel):
    visit_id: str
    date: str
    type: str
    diagnosis: str | None = None
    treatment: str | None = None
    provider: str | None = None

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