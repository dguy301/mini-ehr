# Mini EHR Workflow System

Mini EHR is a beginner-friendly healthcare informatics project that simulates a small Electronic Health Record system.

The goal is to model basic healthcare workflows such as:

- patient records
- visit history
- diagnosis tracking
- treatment tracking
- basic healthcare data alerts

This project is designed to help demonstrate practical healthcare IT, health informatics, and clinical systems analysis skills.

## Why This Project Exists

This project connects software engineering concepts with healthcare workflows.

It is meant to show that the developer understands:

- how patient records are structured
- how healthcare data moves through a system
- how missing or abnormal data can create operational problems
- how simple software can support healthcare decision-making

## Planned Features

Initial features:

- store patient records
- list all patients
- view a single patient
- store patient visit history
- detect missing diagnosis information
- detect missing treatment information
- detect frequent emergency room visits

Future features:

- REST API using FastAPI
- SQLite database
- dashboard summary
- healthcare-style audit logging
- access monitoring for HIPAA-style security scenarios

## Tech Stack

Planned stack:

- Python
- FastAPI
- JSON data storage first
- SQLite later
- pytest for tests

## Current Status

Project scaffold created.

No application logic has been added yet.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

## Data Storage

Patient data is currently stored in:

data/patients.json

The system will read and write patient records to this file.

Initial structure:

```json
[]
```

## Repository Layer

The repository module handles data access.

Responsibilities:

- load patient data from file
- save patient data to file
- retrieve patients by ID
- list all patients

This simulates a basic healthcare data storage system.

## Data Models

The project currently defines two healthcare data models:

- `Patient`
- `Visit`

A patient can have many visits.

Each visit may include:

- visit ID
- date
- visit type
- diagnosis
- treatment
- provider

These models help validate healthcare-style data before it is saved.

## Visit Tracking

The repository can now add visits to an existing patient.

A visit may include:

- visit ID
- date
- visit type
- diagnosis
- treatment
- provider

This allows the project to model a basic patient care timeline.

## Alert Rules

The project includes basic healthcare data alerts.

Current alert rules:

- patient has no visits
- visit is missing a diagnosis
- visit is missing treatment information
- visit is missing provider information
- patient has more than 2 ER visits

These alerts simulate basic health informatics data quality checks.

## API

The project now includes a FastAPI application.

Current endpoints:

- `GET /`
- `GET /patients`
- `GET /patients/{patient_id}`
- `POST /patients`
- `POST /patients/{patient_id}/visits`
- `GET /patients/{patient_id}/alerts`

Run the API:

```bash
PYTHONPATH=src uvicorn mini_ehr.main:app --reload
```

## Testing

Run all tests with:

```bash
PYTHONPATH=src pytest
```

## API Testing

The API is tested using FastAPI's `TestClient`.

Current API tests verify:

- root endpoint works
- patient list endpoint returns a list
- missing patient returns a 404 response

## Alert API Testing

The API test suite now verifies that:

- alerts can be retrieved for a patient
- missing diagnosis information is detected
- missing treatment information is detected
- missing provider information is detected
- requesting alerts for a missing patient returns 404

## Dashboard Summary

The project includes dashboard summary logic.

Current summary metrics:

- total patients
- total visits
- total ER visits

This is the beginning of a health informatics dashboard layer.

## Dashboard API

The API now exposes a dashboard summary endpoint:

```text
GET /dashboard/summary
```

## Command-Line Helper

The project includes a small CLI helper that prints dashboard summary data.

Run it with:

```bash
PYTHONPATH=src python -m mini_ehr.cli
```

Mini EHR Dashboard Summary
--------------------------
Total patients: 0
Total visits: 0
Total ER visits: 0

## CLI Testing

The project currently tests dashboard summary behavior used by the CLI helper.

This verifies:

- expected dashboard keys exist
- empty datasets produce zero counts

## Audit Logging

The project now includes basic audit event creation.

An audit event records:

- timestamp
- actor
- action
- resource type
- resource ID

This is useful for healthcare-style access monitoring and HIPAA-inspired security scenarios.

## Audit Repository

Audit events can now be saved and listed using `AuditRepository`.

Audit data is stored separately from patient data so access/security events do not mix with clinical records.

## API Audit Logging

The API now writes an audit event when a patient record is viewed.

Current logged action:

- `VIEW_PATIENT`

This models healthcare-style access tracking, where viewing patient records should be traceable.

## Audit API

The API exposes audit events through:

```text
```
GET /audit/events

## Current Audit Actions

The API currently logs:

- `CREATE_PATIENT`
- `VIEW_PATIENT`
- `ADD_VISIT`

These actions help demonstrate healthcare-style traceability for patient data access and modification.

## Suspicious Audit Detection

The project now includes simple suspicious access detection.

Current rule:

- more than 3 `VIEW_PATIENT` events for the same patient triggers `REPEATED_PATIENT_ACCESS`

This connects the project to healthcare cybersecurity and HIPAA-style access monitoring.

## Audit Alerts API

The API exposes suspicious audit activity through:

```text
```
GET /audit/alerts

## Audit Event Filtering

Audit events can be filtered by action.

Examples:

```text
```
GET /audit/events
GET /audit/events?action=VIEW_PATIENT
GET /audit/events?action=CREATE_PATIENT
GET /audit/events?action=ADD_VISIT

## Audit Event Actor Filtering

Audit events can also be filtered by actor.

Example:

```text
```
GET /audit/events?actor=api_user

## Audit Helper

The API uses a helper function to record audit events consistently.

This keeps audit logging behavior centralized and easier to maintain.

## Actor Tracking

API callers can identify themselves using the `X-Actor` request header.

Example:

```text
```
X-Actor: analyst_001

## High-Volume Actor Detection

The audit alert system now detects actors who view more than 5 patient records.

Current rule:

- more than 5 `VIEW_PATIENT` events by the same actor triggers `HIGH_VOLUME_PATIENT_ACCESS`

This models a basic healthcare access monitoring scenario.

## Audit Summary

The audit module can summarize audit activity.

Current summary metrics:

- total audit events
- counts by action
- counts by actor

This helps show who is using the system and what actions are being performed.

## Audit Summary API

The API exposes audit summary data through:

```text
```
GET /audit/summary

## Healthcare Informatics Notes

Additional documentation is available in:

```text
```
docs/HEALTHCARE_INFORMATICS_NOTES.md

## Current Project Status

Current capabilities:

### Patient Management

- create patient records
- retrieve patient records
- track patient visits

### Clinical Data Validation

- validate patient and visit structures using Pydantic
- detect missing diagnosis information
- detect missing treatment information
- detect missing provider information

### Dashboard Analytics

- total patient count
- total visit count
- ER visit count

### Audit Logging

- audit patient access
- audit patient creation
- audit visit creation
- filter audit events by action
- filter audit events by actor

### Suspicious Activity Detection

- repeated patient access detection
- high-volume patient access detection

### API Features

- FastAPI REST API
- interactive Swagger documentation
- automated API testing

### Testing

The project currently includes:

- repository tests
- audit tests
- alert tests
- dashboard tests
- API tests

## Future Enhancements

Possible future enhancements:

- SQLite database support
- role-based access control
- authentication
- React frontend dashboard
- FHIR-compatible patient models
- HL7 integration
- exportable audit reports
- anomaly scoring
- SIEM integration

## Educational Purpose

This project is intended for learning healthcare informatics, healthcare analytics, audit logging, and healthcare cybersecurity concepts.

It is not intended for real clinical use.

## FHIR-Like Patient Resource

The project now includes a simplified FHIR-like representation of a patient.

The internal `Patient` model can be converted into a structure containing:

- `resourceType`
- `id`
- `name`
- `birthDate`

This begins aligning the project with healthcare interoperability concepts.

## FHIR-Like API Endpoint

The API exposes a simplified FHIR-like patient resource:

```text
```
GET /patients/{patient_id}/fhir

## FHIR-Like Encounter Resource

The internal `Visit` model can now be converted into a simplified FHIR-like `Encounter` resource.

This maps project visits to healthcare interoperability concepts.

A visit becomes an encounter with:

- `resourceType`
- `id`
- `status`
- `class`
- `subject`
- `period`

## FHIR-Like Encounter API

The API exposes simplified FHIR-like encounters through:

```text
```
GET /patients/{patient_id}/fhir/encounters

## FHIR-Like Condition Resource

Visit diagnoses can now be converted into simplified FHIR-like `Condition` resources.

Each condition references:

- the patient
- the related encounter

This demonstrates how healthcare resources are linked together in interoperability systems.