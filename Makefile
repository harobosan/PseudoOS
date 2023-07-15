ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

all: main.py
	python3 main.py

.PHONY: run
run: main.py
	python3 main.py $(RUN_ARGS)

static:
	pylint main.py modules

install: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf modules/__pycache__/
