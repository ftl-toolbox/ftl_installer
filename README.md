[![Build Status](https://travis-ci.org/ftl-toolbox/ftl_installer.svg?branch=master)](https://travis-ci.org/ftl-toolbox/ftl_installer)  
[![Coverage Status](https://coveralls.io/repos/github/ftl-toolbox/ftl_installer/badge.svg?branch=master)](https://coveralls.io/github/ftl-toolbox/ftl_installer?branch=master)  
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/aaa41fbdcc7c4068a67ecfd7b1dbe2b6/badge.svg)](https://www.quantifiedcode.com/app/project/aaa41fbdcc7c4068a67ecfd7b1dbe2b6)  
[![Code Climate](https://codeclimate.com/github/ftl-toolbox/ftl_installer/badges/issue_count.svg)](https://codeclimate.com/github/ftl-toolbox/ftl_installer)  
[![Stories in Ready](https://badge.waffle.io/ftl-toolbox/ftl_installer.svg?label=ready&title=Ready)](http://waffle.io/ftl-toolbox/ftl_installer)  

# ftl_installer
Ansible based installer framework.

# Hacking

## Creating a virtual environment

Run `make venv` to create a [python virtual
environment](https://virtualenv.pypa.io/en/latest/) and install
dependencies within your local checkout.

```
make venv
```

The python virtual environment created by `make venv` will use the
default system python. Providing the `FTL_PYTHON` environment variable
will override the python version used to create the virtual environment.

```
FTL_PYTHON=/usr/bin/python3.4 make venv
```

## Running the cli

Once a virtual environment has been created, `ftl_installer` will be in `PATH`.

```
ftl_installer --help
```

## Running tests

Run `make test` to run unit tests,
[pep8](http://www.python.org/dev/peps/pep-0008) style formatting
checks and [pyflakes](https://pypi.python.org/pypi/pyflakes) checks.

```
make test
```

`make test` does not operate within the virtual environment and runs
tests against local source using the default system python. Set the
`FTL_PYTHON` environment variable to override the python version used
to run tests.

```
FTL_PYTHON=/usr/bin/python3.4 make test
```

## Running CI tests

Run `make ci` to create a virtual environment and run tests within the
virtual environment.

```
make ci
```

Set the `FTL_PYTHON` environment variable to override the python
version used to run CI tests.

```
FTL_PYTHON=/usr/bin/python3.4 make ci
```
