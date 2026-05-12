from mini_ehr.dashboard import build_dashboard_summary
from mini_ehr.repository import PatientRepository

def main():
    repo = PatientRepository("data/patients.json")
    patients = repo.list_patients()
    summary = build_dashboard_summary(patients)

    print("Mini EHR Dashboard Summary")
    print("--------------------------")
    print(f"Total patients: {summary['total_patients']}")
    print(f"Total visits: {summary['total_visits']}")
    print(f"Total ER visits: {summary['total_er_visits']}")


if __name__ == "__main__":
    main()