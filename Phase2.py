"""Date time."""
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
        values = line.strip().split("\t")
        for i, value in enumerate(values):
            data_dict[header[i]].append(value)
    return data_dict


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Read and parse the patient and lab data files.

    Overall time complexity: O((L1+L2)*C), where L1 and L2 are the number.
    of lines in patient and lab files, respectively.C is the number of columns.
    """
    # O(L1*C): Parsing patient file
    patient_data = parse_file(patient_filename)

    # O(L2*C): Parsing lab file
    lab_data = parse_file(lab_filename)

    # O(1): Returning the tuple
    return patient_data, lab_data


def patient_age(records: Dict[str, List[str]], patient_id: str) -> int:
    """Return the age in years of a given patient.

    Overall time complexity: O(N), where N is the number of patients.
    """
    # O(N): Finding the index of the patient. N is the number of patients
    birthdate_str = records["PatientDateOfBirth"][
        records["PatientID"].index(patient_id)
    ]

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

    sick = patient_is_sick(
        patient_data,
        lab_data,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "URINALYSIS: RED BLOOD CELLS",
        "<",
        10,
    )
    print(sick)

    age = patient_age(patient_data, "65A7FBE0-EA9F-49E9-9824-D8F3AD98DAC0")
    print(age)
