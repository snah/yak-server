
PYTHON_FILES := $(shell find yakserver -name '*.py')
PYTHON_FILES += $(shell find tests -name '*.py')
PYTHON_FILES += setup.py

NOSE_OPTIONS = 

default: functionaltest coverage lint

clean:
	find . -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .coverage htmlcov
	rm -rf docs/_build/*
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

docs: FORCE
	sphinx-build -b html docs/ docs/_build/

travis_test: FORCE
	nose2 $(NOSE_OPTIONS) -C --coverage yakserver tests

test: FORCE
	nose2 $(NOSE_OPTIONS) tests

unittest: FORCE
	nose2 $(NOSE_OPTIONS) tests.unit

functionaltest: FORCE
	nose2 $(NOSE_OPTIONS) tests.functional

coverage: FORCE
	nose2 $(NOSE_OPTIONS) tests.unit -C  --coverage yakserver --coverage-report html
	@sed -n 's/.*<span class="pc_cov">\([0-9]\?[0-9]\?[0-9]%\)<\/span>.*/\nCoverage: \1\n/ p' htmlcov/index.html

pypytest: clean FORCE
	python setup.py bdist_wheel
	twine upload dist/* -r testpypi

lint: fix-whitespace
	@pylama --options=pylama_for_tests.ini tests || true
	@pylama yakserver || true
	@pylama setup.py --ignore D100 || true

%.fixed_whitespace: %
	@if grep '^\s\+$$' --quiet $<; then sed -i 's/^\s\+$$//' $<; fi

fix-whitespace: $(addsuffix .fixed_whitespace, $(PYTHON_FILES))

venv:
	rm -rf venv
	virtualenv venv
	venv/bin/pip install nose2 cov-core pyusb pylama pylama-pylint ezvalue
	@echo -e "\033[33mDon't forget to manually activate the virtual environment:\033[0m"
	@echo "source venv/bin/activate"

FORCE:
