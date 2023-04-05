"""Testing for EHR."""
import pytest
from EHR import parse_file, parse_data, patient_age, patient_is_sick


def test_parse_file():
    """Test parse_data() function."""
    data = parse_file("Test_Patient.txt")
    assert data["PatientID"] == [
        "MB2ABB23",
        "A4182B95",
        "CB22A4D9",
        "HJF0D84D",
        "CFEAA0",
    ]
    assert len(data["PatientGender"]) == 5
    assert len(data["PatientDateOfBirth"]) == 5
    assert len(data["PatientRace"]) == 5
    assert len(data["PatientMaritalStatus"]) == 5
    assert len(data["PatientLanguage"]) == 5
    assert len(data["PatientPopulationPercentageBelowPoverty"]) == 5


def test_parse_data():
    """Test parse_data() function."""
    # Test patient data
    patient_filename = "Test_Patient.txt"
    lab_filename = "TestData_Lab.txt"
    patient_data, lab_data = parse_data(patient_filename, lab_filename)

    # Test patient data
    assert isinstance(patient_data, dict)
    assert isinstance(patient_data["PatientID"], list)
    assert len(patient_data["PatientID"]) == 5
    assert patient_data["PatientDateOfBirth"][2] == "1970-07-25 13:04:20.717"
    assert patient_data["PatientRace"][3] == "White"
    assert patient_data["PatientMaritalStatus"][4] == "Married"
    assert patient_data["PatientLanguage"][0] == "Icelandic"
    assert patient_data["PatientPopulationPercentageBelowPoverty"][2] == "6.67"

    # Test lab data
    assert isinstance(lab_data, dict)
    assert isinstance(lab_data["PatientID"], list)
    assert lab_data["PatientID"][0] == "MB2ABB23"
    assert lab_data["AdmissionID"][1] == "1"
    assert lab_data["LabName"][2] == "CBC: MCH"
    assert lab_data["LabValue"][3] == "8.9"
    assert lab_data["LabUnits"][4] == "m/cumm"
    assert lab_data["LabDateTime"][5] == "1992-07-01 01:25:54.887"


def test_patient_age():
    """Test patient_age() function."""
    patient_data_test, _ = parse_data("Test_Patient.txt", "TestData_Lab.txt")
    assert patient_age(patient_data_test, "MB2ABB23") == 75
    assert patient_age(patient_data_test, "A4182B95") == 71
    assert patient_age(patient_data_test, "CB22A4D9") == 52
    assert patient_age(patient_data_test, "HJF0D84D") == 44
    assert patient_age(patient_data_test, "CFEAA0") == 101
    with pytest.raises(ValueError):
        patient_age(patient_data_test, "abcd")


def test_patient_is_sick():
    """Test patient_is_sick() function."""
    patient_data_test, lab_data_test = parse_data(
        "Test_Patient.txt", "TestData_Lab.txt"
    )

    assert isinstance(
        patient_is_sick(
            patient_data_test,
            lab_data_test,
            "MB2ABB23",
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
            "MB2ABB23",
            "METABOLIC: GLUCOSE",
            ">",
            100,
        )
        is True
    )
    assert not patient_is_sick(
        patient_data_test,
        lab_data_test,
        "MB2ABB23",
        "METABOLIC: GLUCOSE",
        "<",
        100,
    )
    assert (
        patient_is_sick(
            patient_data_test,
            lab_data_test,
            "A4182B95",
            "METABOLIC: CALCIUM",
            "=",
            8.9,
        )
        is True
    )
    assert not patient_is_sick(
        patient_data_test,
        lab_data_test,
        "A4182B95",
        "METABOLIC: CALCIUM",
        ">",
        9,
    )
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
    pytest.main(["-v", "onlytest.py"])
