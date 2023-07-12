all: main.py
	python3 main.py

clean:
	rm -rf modules/__pycache__/

static:
	pylint main.py modules

install: requirements.txt
	pip install -r requirements.txt
