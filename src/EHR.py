"""Updated EHR Library."""
import os
import sqlite3
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

    def __init__(self, p_id: str, database: str) -> None:
        """Initialize patient class."""
        self.p_id = p_id
        connection = sqlite3.connect(database)
        with connection as cursor:
            self.birth = datetime.strptime(
                cursor.execute(
                    "SELECT PatientDateOfBirth FROM \
                        patients WHERE PatientID = ?",
                    (p_id,),
                ).fetchone()[0],
                "%Y-%m-%d",
            )
            other_data = cursor.execute(
                "SELECT LabName, LabValue, LabDateTime, LabUnits "
                "FROM labs WHERE PatientID = ?",
                (self.p_id,),
            ).fetchall()
            self.labs = [
                Lab(p_id, lab_name, lab_value, lab_units, lab_time)
                for lab_name, lab_value, lab_time, lab_units in other_data
            ]

    @property
    def age(self) -> int:
        """Return the age of the patient."""
        today = datetime.today()
        age_years = (
            today.year
            - self.birth.year
            - ((today.month, today.day) < (self.birth.month, self.birth.day))
        )
        return age_years

    def is_sick(self, lab_name: str, operator: str, value: float) -> bool:
        """Return a boolean indicating whether sick or not."""
        if operator not in [">", "<", "="]:
            raise ValueError("Invalid comparison operator")

        for lab in self.labs:
            if lab.lab_name == lab_name:
                lab_value = lab.lab_value
                if (
                    (operator == ">" and lab_value > value)
                    or (operator == "<" and lab_value < value)
                    or (operator == "=" and lab_value == value)
                ):
                    return True
        return False

    @property
    def age_since_earliest_lab(self) -> int:
        """Return the age of the patient at the time of their first lab."""
        patient_labs = [lab for lab in self.labs]
        if not patient_labs:
            raise ValueError(f"No lab records found for {self.p_id}")
        fst_l = min(patient_labs, key=lambda lab: lab.lab_time).lab_time
        age_years = (
            fst_l.year
            - self.birth.year
            - ((fst_l.month, fst_l.day) < (self.birth.month, self.birth.day))
        )
        return age_years


def parse_data(patient_filename: str, lab_filename: str, db: str) -> None:
    """Read and parse the patient and lab data files."""
    if os.path.exists(db):
        os.remove(db)
    file_list = [patient_filename, lab_filename]
    for file in file_list:
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} not found")

    connection = sqlite3.connect(db)
    with connection as cursor:
        table_list = ["patients", "labs"]
        for table in table_list:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS patients (
                        PatientID TEXT PRIMARY KEY,
                        PatientDateOfBirth TEXT,
                        PatientRace TEXT
                    )"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS labs (
                        LabID INTEGER PRIMARY KEY AUTOINCREMENT,
                        PatientID TEXT,
                        LabName TEXT,
                        LabValue TEXT,
                        LabUnits TEXT,
                        LabDateTime TEXT
                    )"""
        )
        enc = "utf-8-sig"
        with open(lab_filename, mode="r", encoding=enc) as lab_file, open(
            patient_filename, mode="r", encoding=enc
        ) as patient_file:
            lines = lab_file.readlines()

            line_lab = [line.strip().split("\t") for line in lines]
            line_patient = [
                line.strip().split("\t") for line in patient_file.readlines()
            ]

        cursor.executemany(
            "INSERT INTO labs(PatientID, LabName, LabValue, LabUnits,"
            "LabDateTime) VALUES (?, ?, ?, ?, ?)",
            line_lab[1:],
        )

        cursor.executemany(
            "INSERT INTO patients VALUES (?, ?, ?)",
            line_patient[1:],
        )


if __name__ == "__main__":
    parse_data("patient_sample.txt", "lab_sample.txt", "EHR.db")

    parse_data(
        "PatientCorePopulatedTable.txt",
        "LabsCorePopulatedTable.txt",
        "SampleDB.db",
    )
    patient = Patient("1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "SampleDB.db")
    print(patient.age)
    print(patient.age_since_earliest_lab)
    print(patient.is_sick("<", "URINALYSIS: RED BLOOD CELLS", 1.5))
