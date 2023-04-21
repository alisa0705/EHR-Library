# EHR Library

This is a EHR library that helps analyze the patient and lab data. It reads two files: patient and lab data, and calculate the age of patient, the age of a patient at the time of their first lab, and whether the patient is sick or not. Data is inserted to SQLite database.


## For End Users

### Setup/Installation Instructions

1. Install python,  `pytest` and  `time`.
2. Download the `EHR.py` file and save it to local folder.
3. Ensure that the data you want to analyze is in the same folder. 

#### Input File Formats

`parse_data(patient_filename: str, lab_filename: str, db: str) -> None:`

Parses patient data and lab data files (string) and also the database. 

Columns necessary for this function:

Patient file:
PatientID,
PatientDateOfBirth,
PatientRace

Lab file:
PatientID,
LabName,
LabUnits,
LabValue,
LabDateTime

###### Classes
`Lab`: Represents a lab record including attributes such as patient ID, lab name, lab value, lab units, and lab time.

Columns necessary for this Class:

PatientID,
LabName,
LabValue,
LabUnits,
LabDateTime


`Patient`: Represents a patient including attributes such as patient ID, birth date, and race.

Columns necessary for this Class:

PatientID,
PatientDateOfBirth,
PatientRace


`age(self) -> int:`
Return the age of the patient

Columns necessary:
PatientID,
PatientDateOfBirth

`is_sick(
        self, labs: List["Lab"], lab_name: str, operator: str, value: float
    ) -> bool`




1. patient_id: a string representing the patient ID; 
2. lab_name: a string representing the lab name; 
3. operator: a string representing the comparison operator; 
4. value: a float representing the value to compare the lab result against:  returns a boolean.

Columns necessary:
PatientID,
LabName,
LabValue

`age_since_earliest_lab(self, labs: List[Lab]) -> int`

Returns the age of a patient at the time of their first lab.

Columns necessary:

PatientID,
PatientDateOfBirth,


### Examples for using  `EHR.py`


```python
from EHR import parse_data, Patient, Lab

# Parse the patient and lab data files

parse_data("patient_sample.txt", "lab_sample.txt", "EHR.db")

patient=Patient("MB2A", "test_database")

print(patient.age)

sick = patient.is_sick("URINALYSIS: RED BLOOD CELLS", "<", 10)

print(sick)


print(patient.age_since_earliest_lab)

```

## For Contributors

### Local Testing Instructions

1. Install python and `pytest`.
2. Modify the existing `test.py` file for `EHR.py`. Update the test functions
3. Run tests using the command: `pytest test.py`
