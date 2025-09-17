from contextlib import nullcontext
from io import StringIO

import pytest

from src.exceptions import FileStructureError, ReportTypeError
from src.report_maker import ReportMaker


@pytest.fixture
def valid_csv():
    return (
        "student_name,subject,teacher_name,date,grade\n"
        "Семенова Елена,Английский язык,Ковалева Анна,2023-10-10,5\n"
        "Титов Владислав,География,Орлов Сергей,2023-10-12,4\n"
        "Власова Алина,Биология,Ткаченко Наталья,2023-10-15,5\n"
    )


@pytest.mark.parametrize(
    "field_name, expected_result, expected_exception",
    [
        (
            "student_name",
            {"Семенова Елена": 5, "Титов Владислав": 4, "Власова Алина": 5},
            nullcontext(),
        ),
        (
            "student",
            None,
            pytest.raises(
                FileStructureError, match="Unsupported file structure provided"
            ),
        ),
    ],
)
def test_process_data(
    monkeypatch, valid_csv, field_name, expected_result, expected_exception
):
    def mock_open(*args, **kwargs):
        return StringIO(valid_csv)

    monkeypatch.setattr("builtins.open", mock_open)
    rm = ReportMaker()

    with expected_exception:
        res = rm._process_data(field_name, ["fake_csv"])
        assert res == expected_result


@pytest.mark.parametrize(
    "report_type, expected_result, expected_exception",
    [
        (
            "students_perfomance",
            [
                [1, "Семенова Елена", 5],
                [2, "Титов Владислав", 4],
                [3, "Власова Алина", 5],
            ],
            nullcontext(),
        ),
        (
            "student",
            None,
            pytest.raises(ReportTypeError, match="Unsupported report type provided"),
        ),
    ],
)
def test_make_report(
    monkeypatch, valid_csv, report_type, expected_result, expected_exception
):
    def mock_open(*args, **kwargs):
        return StringIO(valid_csv)

    monkeypatch.setattr("builtins.open", mock_open)
    rm = ReportMaker()

    with expected_exception:
        res = rm.make_report(report_type, ["fake_csv"])
        assert res == expected_result
