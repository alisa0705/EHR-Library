"""Date time."""
from datetime import datetime
from typing import Dict, List


def parse_data(patient_f: str, lab_f: str) -> Dict[str, Dict[str, str]]:
    """Read and parses the patient and lab data files."""
    # read patient data
    with open(patient_f, "r") as f:
        header = f.readline().strip().split("\t")
        patient_data: Dict[str, Dict[str, str]] = {}
        for line in f:
            values = line.strip().split("\t")
            patient_data[values[0]] = dict(zip(header[1:], values[1:]))

    # read lab data
    with open(lab_f, "r") as f:
        header = f.readline().strip().split("\t")
        lab_data: Dict[str, List[Dict[str, str]]] = {}
        for line in f:
            values = line.strip().split("\t")
            if values[0] in lab_data:
                lab_data[values[0]].append(dict(zip(header[1:], values[1:])))
            else:
                lab_data[values[0]] = [dict(zip(header[1:], values[1:]))]

    # combine patient and lab data
    for patient_id in patient_data:
        if patient_id in lab_data:
            patient_data[patient_id]["labs"] = lab_data[patient_id]
    return patient_data


def patient_age(records: Dict[str, Dict[str, str]], patient_id: str) -> int:
    """Return the age in years of a given patient."""
    """Patient file should contain the birthdate in the format "YYYY-MM-DD."""
    birthdate_str = records[patient_id]["PatientDateOfBirth"]
    birthdate = datetime.strptime(birthdate_str.split()[0], "%Y-%m-%d")
    today = datetime.today()
    age_years = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )
    return age_years


def patient_is_sick(
    records: Dict[str, Dict[str, str]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return a boolean indicating whether sick or not."""
    if operator == ">":
        for lab in records[patient_id].get("labs", []):
            if lab["LabName"] == lab_name and float(lab["LabValue"]) > value:
                return True
        return False
    if operator == "<":
        for lab in records[patient_id].get("labs", []):
            if lab["LabName"] == lab_name and float(lab["LabValue"]) < value:
                return True
        return False
    if operator == "=":
        for lab in records[patient_id].get("labs", []):
            if lab["LabName"] == lab_name and float(lab["LabValue"]) == value:
                return True
        return False
