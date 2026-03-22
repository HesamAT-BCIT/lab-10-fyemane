import pytest

from utils.validation import normalize_profile_data, validate_profile_data


@pytest.mark.parametrize(
    "first_name,last_name,student_id,expected",
    [
        ("John", "Doe", "12345678", None),
        ("Jane", "Smith", 12345678, None),
        ("", "Doe", "12345678", "All fields are required."),
        ("John", "", "12345678", "All fields are required."),
        ("John", "Doe", "", "All fields are required."),
        (None, "Doe", "12345678", "All fields are required."),
        ("John", None, "12345678", "All fields are required."),
        ("John", "Doe", None, "All fields are required."),
        ("   ", "Doe", "12345678", "All fields are required."),
        ("John", "   ", "12345678", "All fields are required."),
        ("John", "Doe", "   ", "All fields are required."),
        ("   ", "   ", "   ", "All fields are required."),
    ],
)
def test_validate_profile_data(first_name, last_name, student_id, expected):
    assert validate_profile_data(first_name, last_name, student_id) == expected


@pytest.mark.parametrize(
    "first_name,last_name,student_id,expected",
    [
        (
            " John ",
            " Doe ",
            12345678,
            {"first_name": "John", "last_name": "Doe", "student_id": "12345678"},
        ),
        (
            "  Alice  ",
            "  Wong  ",
            "  A00123456  ",
            {"first_name": "Alice", "last_name": "Wong", "student_id": "A00123456"},
        ),
        (
            None,
            None,
            None,
            {"first_name": "", "last_name": "", "student_id": ""},
        ),
        (
            "",
            "",
            "",
            {"first_name": "", "last_name": "", "student_id": ""},
        ),
        (
            " Bob",
            "Lee ",
            " 00012345 ",
            {"first_name": "Bob", "last_name": "Lee", "student_id": "00012345"},
        ),
    ],
)
def test_normalize_profile_data(first_name, last_name, student_id, expected):
    assert normalize_profile_data(first_name, last_name, student_id) == expected