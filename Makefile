.PHONY: test
test:
	export PYTHONPATH='src/'
	python3 tests/TestListMethods.py
