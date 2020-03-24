.PHONY: test docs clean
test:
	export PYTHONPATH='za_warudo'; python3 tests/test_boost_list.py

docs:
	export PYTHONPATH='za_warudo'; pdoc3 --html -o docs za_warudo --force

clean:
	rm -r za_warudo/*.pyc za_warudo/__pycache__
