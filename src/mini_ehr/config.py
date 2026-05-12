import os

DEFAULT_PATIENT_DATA_PATH = "data/patients.json"
DEFAULT_AUDIT_DATA_PATH = "data/audit_log.json"

def get_patient_data_path() -> str:
    """
    Return the patient data path.
    This allows tests or deployments to override the default data file.
    """
    return os.getenv("MINI_EHR_PATIENT_DATA_PATH", DEFAULT_PATIENT_DATA_PATH)

def get_audit_data_path() -> str:
    """
    Return the audit log data path.
    
    This allows tests or deployments to override the default audit log file.
    """
    return os.getenv("MINI_EHR_AUDIT_DATA_PATH", DEFAULT_AUDIT_DATA_PATH)