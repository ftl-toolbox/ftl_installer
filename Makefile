########################################################

NAME := ftl_installer

# VERSION file provides one place to update the software version.
VERSION := $(shell cat VERSION)

ifndef FTL_PYTHON
FTL_PYTHON=python
endif

PYVER=$(shell $(FTL_PYTHON) -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")

__init__.py: ftl_installer/__init__.py.in
	sed "s/%VERSION%/$(VERSION)/" $< > ftl_installer/__init__.py

setup.py: setup.py.in
	sed "s/%VERSION%/$(VERSION)/" $< > setup.py

clean:
	@find . -type f -regex ".*\.py[co]$$" -delete
	@find . -type f \( -name "*~" -or -name "#*" \) -delete
	@rm -fR venv build dist $(NAME).egg-info
	@rm -fR setup.py ftl_installer/__init__.py

venv: clean __init__.py setup.py
	@echo "#############################################"
	@echo "# Creating a python-$(PYVER) virtualenv"
	@echo "#############################################"
	virtualenv -p $(FTL_PYTHON) venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && python setup.py develop

install: __init__.py setup.py
	python setup.py install
	pip install -r test-requirements.txt
	pip install coveralls

nosetests: __init__.py setup.py
	@echo "#############################################"
	@echo "# Running Unit Tests"
	@echo "#############################################"
	$(FTL_PYTHON) setup.py nosetests

pep8: __init__.py setup.py
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests"
	@echo "#############################################"
	pep8 --max-line-length=120 --exclude="tests/*,venv/*" --ignore=E501,E121,E124 $(NAME)/

pyflakes: __init__.py setup.py
	@echo "#############################################"
	@echo "# Running Pyflakes Sanity Tests"
	@echo "# Note: most import errors may be ignored"
	@echo "#############################################"
	pyflakes $(NAME)/

ci-nosetests: __init__.py setup.py
	@echo "#############################################"
	@echo "# Running Unit Tests"
	@echo "#############################################"
	. venv/bin/activate && python setup.py nosetests

ci-pep8: __init__.py setup.py
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests"
	@echo "#############################################"
	. venv/bin/activate && pep8 --max-line-length=120 --exclude="tests/*,venv/*" --ignore=E501,E121,E124 $(NAME)/

ci-pyflakes: __init__.py setup.py
	@echo "#############################################"
	@echo "# Running Pyflakes Sanity Tests"
	@echo "# Note: most import errors may be ignored"
	@echo "#############################################"
	. venv/bin/activate && pyflakes $(NAME)/

ci: clean venv ci-nosetests ci-pep8 ci-pyflakes

test: nosetests pep8 pyflakes
