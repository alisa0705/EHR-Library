"""Date time."""
from datetime import datetime
from typing import Dict, List, Any


def parse_data(filename: str) -> Dict[str, List[str]]:
    """Read and parse the patient and lab data files."""
    with open(filename, encoding="UTF-8-sig") as file:
        lines = file.readlines()
    if not lines:
        return {}

    header = lines[0].strip().split("\t")
    data_dict: Dict[str, List[str]] = {col: [] for col in header}

    for line in lines[1:]:
        values = line.strip().split("\t")
        for i, value in enumerate(values):
            data_dict[header[i]].append(value)

    return data_dict


def patient_age(records: Dict[str, List[str]], patient_id: str) -> int:
    """Return the age in years of a given patient."""
    """Patient file should contain the birthdate in the format "YYYY-MM-DD."""
    birthdate_str = records["PatientDateOfBirth"][
        records["PatientID"].index(patient_id)
    ]
    birthdate = datetime.strptime(birthdate_str.split()[0], "%Y-%m-%d")
    today = datetime.today()
    age_years = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )
    return age_years


def patient_is_sick(
    patient_records: dict[str, list[Any]],
    lab_records: dict[str, list[Any]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return a boolean indicating whether sick or not."""
    patient_index = patient_records["PatientID"].index(patient_id)

    for i, lab in enumerate(lab_records["LabName"]):
        if lab == lab_name and lab_records["PatientID"][i] == patient_id:
            lab_value = float(lab_records["LabValue"][i])
            if (
                (operator == ">" and lab_value > value)
                or (operator == "<" and lab_value < value)
                or (operator == "=" and lab_value == value)
            ):
                return True
    return False


if __name__ == "__main__":
    patient_data = parse_data("Patient.txt")
    lab_data = parse_data("lab.txt")

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
