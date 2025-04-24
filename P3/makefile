.PHONY: lint

lint:
	black .
	isort .
	autoflake --in-place --remove-all-unused-imports --recursive .
	mypy . 
	pylint **/*.py

