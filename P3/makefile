.PHONY: lint

add-%:
	pip install $* && pip freeze > requirements.txt

lint:
	black .
	isort .
	autoflake --in-place --remove-all-unused-imports --recursive .
	mypy . 
	pylint **/*.py

