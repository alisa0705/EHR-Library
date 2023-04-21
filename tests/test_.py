"""Testing for EHR."""
from typing import Dict, List
from EHR import parse_data, Patient, Lab
from fake_files import fake_files
import pytest
import sqlite3

list_patient = [
    [
        "PatientID",
        "PatientDateOfBirth",
        "PatientRace",
    ],
    [
        "MB2A",
        "1970-08-16",
        "Asian",
    ],
]

list_lab = [
    [
        "PatientID",
        "LabName",
        "LabValue",
        "LabUnits",
        "LabDateTime",
    ],
    [
        "MB2A",
        "CBC: WBC",
        "1.8",
        "K/uL",
        "1992-07-01 01:36:17.910",
    ],
]

test_database = "EHR.db"

with fake_files(list_lab) as labs, fake_files(list_patient) as patients:
    parse_data(patients[0], labs[0], test_database)

patient = Patient("MB2A", test_database)


def test_parse_data() -> None:
    """Test parse data."""
    with fake_files(list_lab) as labb, fake_files(list_patient) as p:
        parse_data(p[0], labb[0], "EHR.db")

        con = sqlite3.connect("EHR.db")
        with con as cursor:
            patient_db = cursor.execute(
                "SELECT PatientID, PatientDateOfBirth FROM patients"
            ).fetchall()
            assert patient_db[0][0] == "MB2A"
            assert patient_db[0][1] == "1970-08-16"
            labs_db = cursor.execute(
                "SELECT PatientID, LabName, \
                    LabValue, LabUnits, LabDateTime FROM labs"
            ).fetchall()
            assert labs_db[0][0] == "MB2A"
            assert labs_db[0][1] == "CBC: WBC"
            assert labs_db[0][2] == "1.8"
            assert labs_db[0][3] == "K/uL"
            assert labs_db[0][4] == "1992-07-01 01:36:17.910"
        test_files = [("patients[0].txt", labb[0]), (p[0], "labs[0].txt")]
        for patient_file, lab_file in test_files:
            with pytest.raises(FileNotFoundError):
                parse_data(patient_file, lab_file, "EHR.db")


def test_patient_age() -> None:
    """Test patient_age() function."""
    assert patient.age == 52


def test_patient_is_sick() -> None:
    """Test patient_is_sick() function"""
    assert patient.is_sick("CBC: WBC", "<", 1.5) is False
    # Test for invalid lab operator
    with pytest.raises(ValueError):
        patient.is_sick("CBC: WBC", "?", 1.5)


def test_age_since_earliest_lab() -> None:
    """Test age_since_earliest_lab() function."""
    assert patient.age_since_earliest_lab == 21
