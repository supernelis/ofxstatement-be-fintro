PYTHON=.venv/bin/python

all: PYTHON

PYTHON: setup.py
	virtualenv -p python3 --no-site-packages .venv
	$(PYTHON) setup.py develop
	
test:
	ofxstatement convert -t fintrobe src/tests/sample.csv test_output.ofx