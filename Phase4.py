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


if __name__ == "__main__":
    patient_data, lab_data = parse_data("Patient.txt", "lab.txt")

    age = patient_age_at_first_lab(
        patient_data,
        lab_data,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
    )
    print(age)
