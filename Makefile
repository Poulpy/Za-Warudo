.PHONY: test
test:
	export PYTHONPATH='za_warudo'; python3 tests/test_boost_list.py

.PHONY: docs
docs:
	export PYTHONPATH='za_warudo'; pdoc3 --html -o docs za_warudo --force
