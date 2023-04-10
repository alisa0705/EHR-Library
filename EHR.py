"""Updated EHR Library."""
from datetime import datetime
from typing import Dict, List, Any


class Lab:
    """Lab class."""

    def __init__(
        self,
        p_id: str,
        lab_name: str,
        lab_value: float,
        lab_units: str,
        lab_time: str,
    ):
        """Initialize the lab class."""
        self.p_id = p_id
        self.lab_name = lab_name
        self.lab_value = float(lab_value)
        self.lab_units = lab_units
        self.lab_time = datetime.strptime(lab_time.split()[0], "%Y-%m-%d")


class Patient:
    """Patient class."""

    def __init__(self, p_id: str, birth: str, race: str):
        """Initialize the patient class."""
        self.p_id = p_id
        self.birth = datetime.strptime(birth.split()[0], "%Y-%m-%d")
        self.race = race

    @property
    def age(self) -> int:
        """Return the age of the patient."""
        today = datetime.today()
        if self.birth > today:
            raise ValueError("Invalid birth date")
        age_years = (
            today.year
            - self.birth.year
            - ((today.month, today.day) < (self.birth.month, self.birth.day))
        )
        return age_years

    def is_sick(
        self, labs: List["Lab"], lab_name: str, operator: str, value: float
    ) -> bool:
        """Return a boolean indicating whether sick or not."""
        if operator not in [">", "<", "="]:
            raise ValueError("Invalid comparison operator")

        for lab in labs:
            if lab.p_id == self.p_id and lab.lab_name == lab_name:
                lab_value = lab.lab_value
                if (
                    (operator == ">" and lab_value > value)
                    or (operator == "<" and lab_value < value)
                    or (operator == "=" and lab_value == value)
                ):
                    return True
        return False

    def age_since_earliest_lab(self, labs: List[Lab]) -> int:
        """Return the age of the patient at the time of their first lab."""
        patient_labs = [lab for lab in labs if lab.p_id == self.p_id]
        if not patient_labs:
            raise ValueError(f"No lab records found for {self.p_id}")

        fst_l = min(patient_labs, key=lambda lab: lab.lab_time).lab_time
        age_years = (
            fst_l.year
            - self.birth.year
            - ((fst_l.month, fst_l.day) < (self.birth.month, self.birth.day))
        )

        return age_years


def parse_file(filename: str) -> Dict[str, List[str]]:
    """Parse the file."""
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


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[List[Patient], List[Lab]]:
    """Read and parse the patient and lab data files."""
    patient_data = parse_file(patient_filename)
    lab_data = parse_file(lab_filename)

    patients = [
        Patient(p_id, dob, race)
        for p_id, dob, race in zip(
            patient_data["PatientID"],
            patient_data["PatientDateOfBirth"],
            patient_data["PatientRace"],
        )
    ]

    labs = [
        Lab(p_id, lab_name, float(lab_value), lab_units, lab_time)
        for p_id, lab_name, lab_value, lab_units, lab_time in zip(
            lab_data["PatientID"],
            lab_data["LabName"],
            lab_data["LabValue"],
            lab_data["LabUnits"],
            lab_data["LabDateTime"],
        )
    ]

    return patients, labs


if __name__ == "__main__":
    patients, labs = parse_data("Patient.txt", "lab.txt")

    p_id = "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    target_p = next(patient for patient in patients if patient.p_id == p_id)

    age = target_p.age
    print(age)

    sick = target_p.is_sick(labs, "URINALYSIS: RED BLOOD CELLS", "<", 10)
    print(sick)

    age_at_fst_l = target_p.age_since_earliest_lab(labs)
    print(age_at_fst_l)
