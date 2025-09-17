class ReportTypeError(Exception):
    def __init__(self, message: str = "Unsupported report type provided") -> None:
        super().__init__(message)


class FileStructureError(Exception):
    def __init__(self, message: str = "Unsupported file structure provided") -> None:
        super().__init__(message)
