run:
	python src/main.py --files data/students1.csv data/students2.csv --report students_perfomance
lint:
	ruff format .
	ruff check --fix .