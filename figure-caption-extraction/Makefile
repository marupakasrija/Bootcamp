.PHONY: build run test clean

build:
	docker build -t figure-caption-extraction .

run:
	docker run -p 8000:8000 -p 8501:8501 figure-caption-extraction

test:
	pytest tests/

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	Find . -type f -name "*.pyc" -delete