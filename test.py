"""Testing for EHR."""
import pytest
from EHR import (
    parse_file,
    parse_data,
    Patient,
    Lab,
)
from fake_files import fake_files
from typing import Dict, List


def test_parse_file() -> None:
    """Test parse_data() function."""
    test_data = [
        [
            "PatientID",
            "PatientDateOfBirth",
            "PatientRace",
        ],
        ["MB2A", "1960-01-01", "White"],
        ["A418", "1970-07-25", "Asian"],
        ["CB22", "1980-08-30", "Black"],
        ["HJF0", "1990-09-01", "Hispanic"],
        ["CFEAA0", "2000-10-03", "White"],
    ]

    with fake_files(test_data) as temp_files:
        data: Dict[str, List[str]] = parse_file(temp_files[0])
        assert data["PatientID"] == [
            "MB2A",
            "A418",
            "CB22",
            "HJF0",
            "CFEAA0",
        ]
        assert len(data["PatientDateOfBirth"]) == 5


def test_parse_data() -> None:
    """Test parse_data() function."""
    patient_data_list = [
        ["PatientID", "PatientDateOfBirth", "PatientRace"],
        ["MB2A", "1960-01-01", "White"],
        ["A418", "1970-07-25", "Asian"],
        ["CB22", "1980-08-30", "Black"],
        ["HJF0", "1990-09-01", "Hispanic"],
        ["CFEAA0", "2000-10-03", "White"],
    ]

    lab_data_list = [
        ["PatientID", "LabName", "LabValue", "LabUnits", "LabDateTime"],
        ["MB2A", "CBC: WBC", "10.3", "K/uL", "1990-06-01 01:02:03.456"],
        ["A418", "CBC: Hct", "45.2", "%", "1991-07-01 01:20:34.567"],
        ["CB22", "CBC: MCH", "32.1", "pg", "1992-08-01 01:23:45.678"],
        ["HJF0", "CBC: MCV", "98.5", "fL", "1993-09-01 01:24:56.789"],
        ["CFEAA0", "CBC: RDW", "12.8", "%", "1994-10-01 01:25:67.890"],
    ]

    with fake_files(patient_data_list, lab_data_list) as temp_files:
        patient_filename, lab_filename = temp_files
        patient_data, lab_data = parse_data(patient_filename, lab_filename)

        # Test patient data
        assert isinstance(patient_data, list)
        assert len(patient_data) == 5

        # Test lab data
        assert isinstance(lab_data, list)
        assert len(lab_data) == 5
        assert lab_data[0].p_id == "MB2A"


def test_age_since_earliest_lab() -> None:
    """Test age_since_earliest_lab() function."""
    patient_data_list = [
        ["PatientID", "PatientDateOfBirth", "PatientRace"],
        ["MB2A", "1960-01-01", "White"],
        ["A418", "1970-07-25", "Asian"],
        ["CFEAA0", "2000-10-03", "White"],
    ]

    lab_data_list = [
        ["PatientID", "LabName", "LabValue", "LabUnits", "LabDateTime"],
        ["MB2A", "CBC: WBC", "10.3", "K/uL", "1990-06-01 01:02:03.456"],
        ["A418", "CBC: Hct", "45.2", "%", "1991-07-01 01:20:34.567"],
        ["CB22", "CBC: MCH", "32.1", "pg", "1992-08-01 01:23:45.678"],
        ["HJF0", "CBC: MCV", "98.5", "fL", "1993-09-01 01:24:56.789"],
        ["CFEAA0", "CBC: RDW", "12.8", "%", "1994-10-01 01:25:67.890"],
    ]

    with fake_files(patient_data_list, lab_data_list) as temp_files:
        patient_filename, lab_filename = temp_files
        patients, labs = parse_data(patient_filename, lab_filename)
        patient = next((p for p in patients if p.p_id == "MB2A"), None)
        assert patient is not None
        # Test with valid patient ID
        age = patient.age_since_earliest_lab(labs)
        assert age == 30


def test_age_since_earliest_lab_value_error() -> None:
    """Test age_since_earliest_lab() function with invalid patient ID."""
    patient_data_list = [
        ["PatientID", "PatientDateOfBirth", "PatientRace"],
        ["MB2A", "1960-01-01", "White"],
        ["A418", "1970-07-25", "Asian"],
        ["CFEAA0", "2000-10-03", "White"],
    ]

    lab_data_list = [
        ["PatientID", "LabName", "LabValue", "LabUnits", "LabDateTime"],
        ["MB2A", "CBC: WBC", "10.3", "K/uL", "1990-06-01 01:02:03.456"],
        ["A418", "CBC: Hct", "45.2", "%", "1991-07-01 01:20:34.567"],
        ["CB22", "CBC: MCH", "32.1", "pg", "1992-08-01 01:23:45.678"],
        ["HJF0", "CBC: MCV", "98.5", "fL", "1993-09-01 01:24:56.789"],
        ["CFEAA0", "CBC: RDW", "12.8", "%", "1994-10-01 01:25:67.890"],
    ]
    with fake_files(patient_data_list, lab_data_list) as temp_files:
        patient_filename, lab_filename = temp_files
        patients, labs = parse_data(patient_filename, lab_filename)
        # Test with invalid patient ID
        with pytest.raises(ValueError, match="No lab records found for x"):
            invalid_patient = Patient("x", "2000-01-01", "Unknown")
            age = invalid_patient.age_since_earliest_lab(labs)


def test_patient_age() -> None:
    """Test patient_age() function."""
    patient_data_test = {
        "PatientID": ["MB2A", "A418", "CB22", "HJF0", "CFEAA0"],
        "PatientDateOfBirth": [
            "1960-01-01",
            "1970-07-25",
            "1980-08-30",
            "1990-09-01",
            "2000-10-03",
        ],
    }
    patient = Patient("MB2A", "1960-01-01", "White")
    assert patient.age == 63


def test_patient_age_value_error() -> None:
    """Test ValueError for patient_age() function."""
    patient = Patient("abcd", "2100-01-01", "Unknown")

    with pytest.raises(ValueError):
        age = patient.age


def test_patient_is_sick_greater_than() -> None:
    """Test patient_is_sick() function with the '>' operator."""
    # Create Patient and Lab instances
    patient = Patient("MB2A", "1960-01-01", "White")
    lab = Lab("MB2A", "GLUCOSE", 150, "mg/dL", "1990-06-01")

    # Test '>' operator
    assert isinstance(patient.is_sick([lab], "GLUCOSE", ">", 100), bool)
    assert patient.is_sick([lab], "GLUCOSE", ">", 100) is True


def test_patient_is_sick_less_than() -> None:
    """Test patient_is_sick() function with the '<' operator."""
    # Create Patient and Lab instances
    patient = Patient("MB2A", "1960-01-01", "White")
    lab = Lab("MB2A", "GLUCOSE", 150, "mg/dL", "1990-06-01")

    # Test '<' operator
    assert not patient.is_sick([lab], "GLUCOSE", "<", 100)


def test_patient_is_sick_equal_to() -> None:
    """Test patient_is_sick() function with the '=' operator."""
    # Create Patient and Lab instances
    patient = Patient("A418", "1970-07-25", "Asian")
    lab = Lab("A418", "METABOLIC: CALCIUM", 8.9, "mg/dL", "1991-07-01")

    # Test '=' operator
    assert patient.is_sick([lab], "METABOLIC: CALCIUM", "=", 8.9) is True


def test_patient_is_sick_value_error() -> None:
    """Test ValueError for patient_is_sick function."""
    patient1 = Patient("MB2A", "1960-01-01", "White")

    lab1 = Lab("MB2A", "GLUCOSE", 150, "mg/dL", "1990-06-01")
    lab2 = Lab("A418", "METABOLIC: CALCIUM", 8.9, "mg/dL", "1991-07-01")

    with pytest.raises(ValueError):
        patient1.is_sick([lab1, lab2], "METABOLIC: ALK PHOS", "WRONG", 60)


if __name__ == "__main__":
    pytest.main(["-v", "test.py"])
