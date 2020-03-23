.PHONY: test
test:
	export PYTHONPATH='za_warudo/'
	python3 tests/test_boost_list.py
