# EHR Library

This is a EHR library that helps analyze the patient and lab data. It reads two files: patient and lab data, and calculate the age of patient and whether the patient is sick or not. 


## For End Users

### Setup/Installation Instructions

1. Install python,  `pytest` and  `time`.
2. Download the `EHR.py` file and save it to local folder.
3. Ensure that the data you want to analyze is in the same folder. 

#### Input File Formats

`parse_file(filename: str) -> Dict[str, List[str]]`

Parses a tab-delimited file and returns a dictionary. 


`parse_data(patient_filename: str, lab_filename: str) -> tuple[Dict[str, List[str]], Dict[str, List[str]]]`

Parses patient data and lab data files (string) and returns a tuple of dictionaries. 

Columns necessary for this function:

Patient file:
PatientID,
PatientDateOfBirth

Lab file:
PatientID,
LabName,
LabValue

`patient_age_at_first_lab(patient_records: Dict[str, List[str]], lab_records: Dict[str, List[str]], patient_id: str) -> int`

Returns the age of a patient at the time of their first lab.
Columns necessary for this function:

Patient file:

PatientID
PatientDateOfBirth

Lab file:
PatientID
LabDateTime


`patient_age(records: Dict[str, List[str]], patient_id: str) -> int`
1. patient_records: a dictionary with column names as keys and lists of values as values for patient data; 
2. patient_id: a string representing the patient ID; 

Columns necessary for this function:
PatientID,
PatientDateOfBirth

`patient_is_sick(patient_records: dict[str, list[Any]], lab_records: dict[str, list[Any]], patient_id: str, lab_name: str, operator: str, value: float) -> bool`

1. patient_records: a dictionary with column names as keys and lists of values as values for patient data; 
2. lab_records: a dictionary: same format for lab data; 
3. patient_id: a string representing the patient ID; 
4. lab_name: a string representing the lab name; 
5. operator: a string representing the comparison operator; 
6. value: a float representing the value to compare the lab result against:  returns a boolean.

Columns necessary for this function:
PatientID,
LabName,
LabValue


### Examples for using  `EHR.py`


```python
from EHR import parse_file, parse_data, patient_age, patient_is_sick, patient_age_at_first_lab

# Parse the patient and lab data files
patient_data, lab_data = parse_data("Patient.txt", "lab.txt")

# Get the age of a patient
age = patient_age(patient_data, "65A7FBE0-EA9F-49E9-9824-D8F3AD98DAC0")
print(age)

# Check if a patient is sick based on a lab test result
sick = patient_is_sick(
    patient_data,
    lab_data,
    "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
    "URINALYSIS: RED BLOOD CELLS",
    "<",
    10,
)
print(sick)
```

## For Contributors

### Local Testing Instructions

1. Install python and `pytest`.
2. Modify the existing `test.py` file for `EHR.py`. Update the test functions
3. Run tests using the command: `pytest test.py`
