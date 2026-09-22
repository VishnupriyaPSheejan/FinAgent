install:
	python -m pip install -r requirements.txt

train:
	python scripts/train.py

predict:
	python scripts/predict.py

test:
	pytest

lint:
	ruff check .

run:
	uvicorn finagent.api.main:app --reload
