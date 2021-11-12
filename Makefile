.PHONY:
run:
	poetry run python main.py

.PHONY:
requirements:
	poetry export -f requirements.txt --output requirements.txt
