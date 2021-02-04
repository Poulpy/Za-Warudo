LOG_DIR=log

.PHONY: test docs clean install
install:
	sudo apt install python3-tk
	pip3 install -r requirements.txt
	pip3 install --upgrade pip
	pip3 install --upgrade pillow
	mkdir -p $(LOG_DIR)
	python3 za_warudo/seed.py seed

run:
	mkdir -p $(LOG_DIR)
	python3 za_warudo


test:
	export PYTHONPATH='za_warudo'; python3 tests/test_boost_list.py

docs:
	export PYTHONPATH='za_warudo'; pdoc3 --html -o docs za_warudo --force

clean:
	rm -r za_warudo/__pycache__ za_warudo/*/__pycache__
	rm $(LOG_DIR)/*
