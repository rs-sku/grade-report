import argparse

from tabulate import tabulate

from src.report_maker import ReportMaker
from src.validation import ValidatePathExists


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report", choices=["students_perfomance"], help="report type"
    )  # add choices if added extra reports
    parser.add_argument(
        "--files", action=ValidatePathExists, nargs="+", help="list of files to process"
    )
    args = parser.parse_args()
    report_maker = ReportMaker()
    res = report_maker.make_report(args.report, args.files)
    print(tabulate(res))


if __name__ == "__main__":
    main()
