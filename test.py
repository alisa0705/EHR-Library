"""Testing for EHR."""
import pytest
from EHR import (
    parse_file,
    parse_data,
    patient_age,
    patient_is_sick,
    patient_age_at_first_lab,
)
from fake_files import fake_files
from typing import Dict, List


def test_parse_file() -> None:
    """Test parse_data() function."""
    test_data = [
        [
            "PatientID",
            "PatientGender",
            "PatientDateOfBirth",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
        ],
        ["MB2A", "M", "1960-01-01", "White", "Single", "English", "10.23"],
        ["A418", "F", "1970-07-25", "Asian", "Married", "Chinese", "12.34"],
        ["CB22", "M", "1980-08-30", "Black", "Divorced", "English", "6.67"],
        ["HJF0", "F", "1990-09-01", "Hispanic", "Married", "Spanish", "8.12"],
        ["CFEAA0", "F", "2000-10-03", "White", "Single", "English", "20.45"],
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
        assert len(data["PatientMaritalStatus"]) == 5


def test_parse_data() -> None:
    """Test parse_data() function."""
    patient_data_list = [
        ["PatientID", "PatientDateOfBirth"],
        ["MB2A", "1960-01-01"],
        ["A418", "1970-07-25"],
        ["CB22", "1980-08-30"],
        ["HJF0", "1990-09-01"],
        ["CFEAA0", "2000-10-03"],
    ]

    lab_data_list = [
        ["PatientID", "AdmissionID", "LabName", "LabValue", "LabUnit", "Time"],
        ["MB2A", "1", "CBC: WBC", "10.3", "K/uL", "1990-06-01 01:02:03.456"],
        ["A418", "1", "CBC: Hct", "45.2", "%", "1991-07-01 01:20:34.567"],
        ["CB22", "1", "CBC: MCH", "32.1", "pg", "1992-08-01 01:23:45.678"],
        ["HJF0", "1", "CBC: MCV", "98.5", "fL", "1993-09-01 01:24:56.789"],
        ["CFEAA0", "1", "CBC: RDW", "12.8", "%", "1994-10-01 01:25:67.890"],
    ]

    with fake_files(patient_data_list, lab_data_list) as temp_files:
        patient_filename, lab_filename = temp_files
        patient_data, lab_data = parse_data(patient_filename, lab_filename)

        # Test patient data
        assert isinstance(patient_data["PatientID"], list)
        assert len(patient_data["PatientID"]) == 5
        assert patient_data["PatientDateOfBirth"][3] == "1990-09-01"

        # Test lab data
        assert isinstance(lab_data, dict)
        assert isinstance(lab_data["PatientID"], list)
        assert lab_data["PatientID"][0] == "MB2A"


def test_patient_age_at_first_lab() -> None:
    """Test patient_age_at_first_lab() function."""
    patient_data_list = [
        ["PatientID", "PatientDateOfBirth"],
        ["MB2A", "1960-01-01"],
        ["A418", "1970-07-25"],
        ["CFEAA0", "2000-10-03"],
    ]

    lab_data_list = [
        ["PatientID", "AdmissionID", "LabName", "LabValue", "LabDateTime"],
        ["MB2A", "1", "CBC: WBC", "10.3", "1990-06-01 01:02:03.456"],
        ["A418", "1", "CBC: Hct", "45.2", "1991-07-01 01:20:34.567"],
        ["CFEAA0", "1", "CBC: RDW", "12.8", "1994-10-01 01:25:67.890"],
    ]

    with fake_files(patient_data_list, lab_data_list) as temp_files:
        patient_filename, lab_filename = temp_files
        patient_data, lab_data = parse_data(patient_filename, lab_filename)
        # Test with valid patient ID
        age = patient_age_at_first_lab(patient_data, lab_data, "MB2A")
        assert age == 30


def test_patient_age_at_first_lab_value_error() -> None:
    """Test patient_age_at_first_lab() function with invalid patient ID."""
    patient_data_list = [
        ["PatientID", "PatientDateOfBirth"],
        ["MB2A", "1960-01-01"],
        ["CFEAA0", "2000-10-03"],
    ]

    lab_data_list = [
        ["PatientID", "AdmissionID", "LabName", "LabUnit", "LabDateTime"],
        ["MB2A", "1", "CBC: WBC", "10.3", "1990-06-01 01:02:03.456"],
        ["CFEAA0", "1", "CBC: RDW", "12.8", "123"],
    ]

    with fake_files(patient_data_list, lab_data_list) as temp_files:
        patient_filename, lab_filename = temp_files
        patient_data, lab_data = parse_data(patient_filename, lab_filename)

        # Test with invalid patient ID
        with pytest.raises(ValueError, match="Patient x not found in data."):
            age = patient_age_at_first_lab(patient_data, lab_data, "x")
        # Test with no lab records for patient ID
        with pytest.raises(ValueError):
            age = patient_age_at_first_lab(patient_data, lab_data, "CFEAA0")


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

    assert patient_age(patient_data_test, "MB2A") == 63
    assert patient_age(patient_data_test, "A418") == 52
    assert patient_age(patient_data_test, "CFEAA0") == 22


def test_patient_age_value_error() -> None:
    """Test ValueError for patient_age() function."""
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

    with pytest.raises(ValueError):
        patient_age(patient_data_test, "abcd")


def test_patient_is_sick_greater_than() -> None:
    """Test patient_is_sick() function with the '>' operator."""
    # Hardcoded patient and lab data
    patient_data_test = {
        "PatientID": ["MB2A", "A418"],
    }

    lab_data_test = {
        "PatientID": ["MB2A"],
        "LabName": ["METABOLIC: GLUCOSE"],
        "LabValue": ["150"],
    }

    assert isinstance(
        patient_is_sick(
            patient_data_test,
            lab_data_test,
            "MB2A",
            "METABOLIC: GLUCOSE",
            ">",
            100,
        ),
        bool,
    )

    assert (
        patient_is_sick(
            patient_data_test,
            lab_data_test,
            "MB2A",
            "METABOLIC: GLUCOSE",
            ">",
            100,
        )
        is True
    )


def test_patient_is_sick_less_than() -> None:
    """Test patient_is_sick() function with the '<' operator."""
    # Hardcoded patient and lab data
    patient_data_test = {
        "PatientID": ["MB2A", "A418"],
    }

    lab_data_test = {
        "PatientID": ["MB2A"],
        "LabName": ["METABOLIC: GLUCOSE"],
        "LabValue": ["150"],
    }

    assert not patient_is_sick(
        patient_data_test,
        lab_data_test,
        "MB2A",
        "METABOLIC: GLUCOSE",
        "<",
        100,
    )


def test_patient_is_sick_equal_to() -> None:
    """Test patient_is_sick() function with the '=' operator."""
    # Hardcoded patient and lab data
    patient_data_test = {
        "PatientID": ["MB2A", "A418"],
    }

    lab_data_test = {
        "PatientID": ["A418"],
        "LabName": ["METABOLIC: CALCIUM"],
        "LabValue": ["8.9"],
    }

    assert (
        patient_is_sick(
            patient_data_test,
            lab_data_test,
            "A418",
            "METABOLIC: CALCIUM",
            "=",
            8.9,
        )
        is True
    )


def test_patient_is_sick_value_error() -> None:
    """Test ValueError for patient_is_sick function."""
    patient_data_test = {
        "PatientID": ["MB2A", "A418"],
        "PatientDateOfBirth": ["1960-01-01", "1970-07-25"],
    }

    lab_data_test = {
        "PatientID": ["MB2A", "A418"],
        "AdmissionID": ["1", "1"],
        "LabName": ["METABOLIC: GLUCOSE", "METABOLIC: CALCIUM"],
    }
    with pytest.raises(ValueError):
        patient_is_sick(
            patient_data_test,
            lab_data_test,
            "CFEAA0",
            "METABOLIC: ALK PHOS",
            "WRONG",
            60,
        )
        patient_is_sick(
            patient_data_test,
            lab_data_test,
            "hiaewhgu",
            "METABOLIC: ALK PHOS",
            "wrong input",
            60,
        )


if __name__ == "__main__":
    pytest.main(["-v", "test.py"])
