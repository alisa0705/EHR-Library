"""Updated EHR Library."""
from datetime import datetime
from typing import Dict, List, Any


def parse_file(filename: str) -> Dict[str, List[str]]:
    """Parse the file.

    Overall time complexity for parse_file: O(L*C)
    """
    # O(1): Opening file
    with open(filename, encoding="UTF-8-sig") as file:
        # O(L): Reading lines. L is the number of lines in the file
        lines = file.readlines()
    if not lines:
        return {}

    # O(C): Splitting header. C is the number of columns
    header = lines[0].strip().split("\t")
    # O(C): Initializing data dictionary
    data_dict: Dict[str, List[str]] = {col: [] for col in header}

    # O(L*C): Nested loop for parsing lines and values
    for line in lines[1:]:
        # O(C): Splitting line into values
        values = line.strip().split("\t")
        for i, value in enumerate(values):
            # O(1): Appending value to corresponding column in dictionary
            data_dict[header[i]].append(value)
    return data_dict


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Read and parse the patient and lab data files.

    Overall time complexity: O(L1*C1+L2*C2), where L1 and L2 are the number.
    of lines in patient and lab files.C1 and C2 is columns numers.
    """
    # O(L1*C): Parsing patient file
    patient_data = parse_file(patient_filename)

    # O(L2*C): Parsing lab file
    lab_data = parse_file(lab_filename)

    # O(1): Returning the tuple
    return patient_data, lab_data


def patient_age_at_first_lab(
    patient_records: Dict[str, List[str]],
    lab_records: Dict[str, List[str]],
    patient_id: str,
) -> int:
    """Return the age of patient at the time of their first lab."""
    if patient_id not in patient_records["PatientID"]:
        raise ValueError(f"Patient {patient_id} not found in the data.")

    birthdate_index = patient_records["PatientID"].index(patient_id)
    birthdate_str = patient_records["PatientDateOfBirth"][birthdate_index]
    birthdate = datetime.strptime(birthdate_str.split()[0], "%Y-%m-%d")

    lab_dates = [
        datetime.strptime(lab_records["LabDateTime"][i].split()[0], "%Y-%m-%d")
        for i, lab_patient_id in enumerate(lab_records["PatientID"])
        if lab_patient_id == patient_id
    ]

    if not lab_dates:
        raise ValueError(f"No lab records found for patient {patient_id}")

    first_lab_date = min(lab_dates)
    age_years = (
        first_lab_date.year
        - birthdate.year
        - (
            (first_lab_date.month, first_lab_date.day)
            < (birthdate.month, birthdate.day)
        )
    )

    return age_years


def patient_age(records: Dict[str, List[str]], patient_id: str) -> int:
    """Return the age in years of a given patient.

    Overall time complexity: O(N), where N is the number of patients.
    """
    try:
        # O(N): Finding the index of the patient. N is the number of patients
        birthdate_str = records["PatientDateOfBirth"][
            records["PatientID"].index(patient_id)
        ]
    except ValueError:
        raise ValueError(f"Patient {patient_id} not found in the data.")

    # O(1): Parsing the birthdate string
    birthdate = datetime.strptime(birthdate_str.split()[0], "%Y-%m-%d")

    # O(1): Getting the current date
    today = datetime.today()

    # O(1): Calculating the age
    age_years = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )

    # O(1): Returning the age
    return age_years


def patient_is_sick(
    patient_records: dict[str, list[Any]],
    lab_records: dict[str, list[Any]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return a boolean indicating whether sick or not.

    Overall time complexity: O(M), where M is the number of lab records.
    """
    if operator not in [">", "<", "="]:
        raise ValueError("Invalid comparison operator")

    # Check if the patient id is present in patient_records
    if patient_id not in patient_records["PatientID"]:
        raise ValueError("Invalid patient id")

    # O(M): Looping through lab records, where M is the number of lab records
    for i, lab in enumerate(lab_records["LabName"]):
        # O(1): Comparing lab and patient ID
        if lab == lab_name and lab_records["PatientID"][i] == patient_id:
            # O(1): Parsing lab value
            lab_value = float(lab_records["LabValue"][i])

            # O(1): Evaluating the condition based on the operator
            if (
                (operator == ">" and lab_value > value)
                or (operator == "<" and lab_value < value)
                or (operator == "=" and lab_value == value)
            ):
                # O(1): Returning True if the condition is met
                return True

    # O(1): Returning False if no matching condition is found
    return False


if __name__ == "__main__":
    patient_data, lab_data = parse_data("Patient.txt", "lab.txt")

    age = patient_age_at_first_lab(
        patient_data,
        lab_data,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
    )
    print(age)
