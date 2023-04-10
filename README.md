# EHR Library

This is a EHR library that helps analyze the patient and lab data. It reads two files: patient and lab data, and calculate the age of patient, the age of a patient at the time of their first lab, and whether the patient is sick or not.


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
from EHR import parse_file, parse_data, Patient, Lab

# Parse the patient and lab data files
patient_data, lab_data = parse_data("Patient.txt", "lab.txt")

    patients, labs = parse_data("Patient.txt", "lab.txt")

    p_id = "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    target_p = next(patient for patient in patients if patient.p_id == p_id)

    age = target_p.age
    print(age)

    sick = target_p.is_sick(labs, "URINALYSIS: RED BLOOD CELLS", "<", 10)
    print(sick)

    age_at_fst_l = target_p.age_since_earliest_lab(labs)
    print(age_at_fst_l)
```

## For Contributors

### Local Testing Instructions

1. Install python and `pytest`.
2. Modify the existing `test.py` file for `EHR.py`. Update the test functions
3. Run tests using the command: `pytest test.py`
