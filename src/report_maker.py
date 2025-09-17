import csv
from abc import ABC, abstractmethod
from collections import defaultdict

from src.exceptions import FileStructureError, ReportTypeError


class ReportMakerInterface(ABC):
    def __init__(self) -> None:
        self._reports_map = {
            "students_perfomance": "student_name"
        }  # to add new reports by grade just extend the dict
        super().__init__()

    @abstractmethod
    def make_report(self, report_type: str) -> str:
        pass

    @abstractmethod
    def _process_data(self, files: list, field_name: str) -> dict[str, float]:
        pass


class ReportMaker(ReportMakerInterface):
    def make_report(
        self, report_type: str, files: list
    ) -> list[list[str | int | float]]:
        try:
            field_name = self._reports_map[report_type]
        except KeyError:
            raise ReportTypeError()
        result_dict = self._process_data(field_name, files)
        result_data = [
            [i + 1, key, value] for i, (key, value) in enumerate(result_dict.items())
        ]
        return result_data

    def _process_data(self, field_name: str, files: list) -> dict[str, float]:
        field_grade_map = defaultdict(float)
        field_count_map = defaultdict(int)
        res = {}
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for i, raw in enumerate(reader):
                    if i == 0:
                        try:
                            indx_field = raw.index(field_name)
                            indx_grade = raw.index("grade")
                        except ValueError:
                            raise FileStructureError()
                    else:
                        cur_field = raw[indx_field]
                        field_grade_map[cur_field] += float(raw[indx_grade])
                        field_count_map[cur_field] += 1
                        res[cur_field] = (
                            field_grade_map[cur_field] / field_count_map[cur_field]
                        )
        return field_grade_map
