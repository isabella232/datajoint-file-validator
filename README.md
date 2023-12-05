# Poetry Demo

This repository contains a demonstration for how to initialize a basic Python package.

## Features

- Runs pytests on pushes to default branch
- Deployment to PyPI when a version tag (`v.*.*`) is pushed
- Pip installable from source: `pip install -e .`

## Tools Used in this Repository

- Virtual environment, package management, and PyPI deployment using [`poetry`](https://python-poetry.org/)
- Unit testing using [`pytest`](https://pytest.org) and [`tox`](https://tox.wiki/en/latest/)
- Automated testing and PyPI deployments using GitHub Actions CI/CD

## Tutorial

Initialize git and poetry interactively
```console
$ git init
Initialized empty Git repository in /home/eho/ripl/repos/poetry-demo/.git/
$ git checkout -b main
$ git branch -d master
$ poetry init                                

This command will guide you through creating your pyproject.toml config.

Package name [poetry-demo]:  
Version [0.1.0]:  
Description []:  Example PyPI package deployment using poetry
Author [Ethan Ho <eho@tacc.utexas.edu>, n to skip]:   
License []:  MIT
Compatible Python versions [^3.8]:  

Would you like to define your main dependencies interactively? (yes/no) [yes] no
Would you like to define your development dependencies interactively? (yes/no) [yes] yes
You can specify a package in the following forms:
  - A single name (requests)
  - A name and a constraint (requests@^2.23.0)
  - A git url (git+https://github.com/python-poetry/poetry.git)
  - A git url with a revision (git+https://github.com/python-poetry/poetry.git#develop)
  - A file path (../my-package/my-package.whl)
  - A directory (../my-package/)
  - A url (https://example.com/packages/my-package-0.1.0.tar.gz)

Search for package to add (or leave blank to continue): pytest
Found 20 packages matching pytest

Enter package # to add, or the complete package name if it is not listed: 
 [0] pytest
 [1] pytest123
 [2] 131228_pytest_1
 [3] pytest-black
 [4] pytest-libnotify
 [5] pytest-automation
 [6] pytest-ringo
 [7] pytest-integration
 [8] pytest-enhancements
 [9] pytest-mercurial
 > 0
Enter the version constraint to require (or leave blank to use the latest version):      
Using version ^7.0.1 for pytest

Add a package: pytest-dotenv
Found 20 packages matching pytest-dotenv

Enter package # to add, or the complete package name if it is not listed: 
 [0] pytest-dotenv
 [1] pytest-django-dotenv
 [2] dotenv
 [3] dotenv-config
 [4] typed-dotenv
 [5] py-dotenv
 [6] dotenv-cli
 [7] django-dotenv
 [8] pythonsite-dotenv
 [9] firstclass-dotenv
 > 0
Enter the version constraint to require (or leave blank to use the latest version): 
Using version ^0.5.2 for pytest-dotenv

Add a package: 

Generated file

[tool.poetry]
name = "poetry-demo"
version = "0.1.0"
description = "Example PyPI package deployment using poetry"
authors = ["Ethan Ho <eho@tacc.utexas.edu>"]
license = "MIT"

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.dev-dependencies]
pytest = "^7.0.1"
pytest-dotenv = "^0.5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"


Do you confirm generation? (yes/no) [yes] 
```

We then install the dependencies that we defined in the above `pyproject.toml` file:

```console
$ poetry install
Creating virtualenv poetry-demo-rPLVa0Kh-py3.8 in /home/eho/.cache/pypoetry/virtualenvs
Updating dependencies
Resolving dependencies... (5.9s)

Writing lock file

Package operations: 10 installs, 0 updates, 0 removals

  • Installing pyparsing (3.0.7)
  • Installing attrs (21.4.0)
  • Installing iniconfig (1.1.1)
  • Installing packaging (21.3)
  • Installing pluggy (1.0.0)
  • Installing py (1.11.0)
  • Installing tomli (2.0.1)
  • Installing pytest (7.0.1)
  • Installing python-dotenv (0.19.2)
  • Installing pytest-dotenv (0.5.2)
```

We can now add our package source code to a subdirectory named `poetry_demo`. Note that the module directory should be snake_cased.

```
$ mkdir poetry_demo
$ touch poetry_demo/__init__.py poetry_demo/__main__.py
$ echo 'import pandas as pd' > poetry_demo/__init__.py
```

Note that we're importing `pandas` in our package. Poetry makes it easy to add package dependencies:

```console
$ poetry add pandas
Using version ^1.4.1 for pandas

Updating dependencies
Resolving dependencies... (17.2s)

Writing lock file

Package operations: 5 installs, 0 updates, 0 removals

  • Installing six (1.16.0)
  • Installing numpy (1.22.2)
  • Installing python-dateutil (2.8.2)
  • Installing pytz (2021.3)
  • Installing pandas (1.4.1)
```

Let's set up testing for this package. We will do this by following the canonical file structure for [pytest](https://docs.pytest.org/en/7.0.x/explanation/goodpractices.html#choosing-a-test-layout-import-rules). 

```console
$ mkdir tests
$ echo 'import poetry_demo' > tests/test_import.py      
```

We can install `pytest` as a development dependency. This means that it will be installed when a developer (or CI workflow) runs `poetry install` from the repository root, but it will not be included in the build. We'll also install `pytest-dotenv` so that environment vars in a `.env` file will be available in pytests.

```console
$ poetry add --dev pytest pytest-dotenv
$ echo 'ENV_USED_IN_PYTESTS=0' > .env
```

Prefixing commands with `poetry run` runs them in the poetry-managed virtual environment. Let's run our test suite:

```console
$ poetry run pytest 
======================================= test session starts ========================================
platform linux -- Python 3.8.10, pytest-7.0.1, pluggy-1.0.0
rootdir: /home/eho/ripl/repos/poetry-demo
plugins: dotenv-0.5.2
collected 0 items                                                                                  

====================================== no tests ran in 0.36s =======================================
```

Similarly, we can invoke `.py` scripts, open an interactive `ipython` session, or open an interactive shell environment (similar to `source my_virtual_env/bin/activate`):

```console
$ poetry run python3 poetry_demo/__main__.py
$ poetry run ipython                        
/home/eho/.local/lib/python3.8/site-packages/IPython/core/interactiveshell.py:802: UserWarning: Attempting to work in a virtualenv. If you encounter problems, please install IPython inside the virtualenv.
  warn(
Python 3.8.10 (default, Nov 26 2021, 20:14:08) 
Type 'copyright', 'credits' or 'license' for more information
IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.

[ins] In [1]: from poetry_demo import *

[ins] In [2]:                                                                                       
Do you really want to exit ([y]/n)? y
$ poetry shell       
Spawning shell within /home/eho/.cache/pypoetry/virtualenvs/poetry-demo-rPLVa0Kh-py3.8
$ deactivate   
```

We can use poetry to build and publish the package to PyPI. All we need are our PyPI credentials:

```console
$ poetry build         
Building poetry-demo (0.1.0)
  - Building sdist
  - Built poetry-demo-0.1.0.tar.gz
  - Building wheel
  - Built poetry_demo-0.1.0-py3-none-any.whl
$ poetry publish

No suitable keyring backends were found
Using a plaintext file to store and retrieve credentials
Username: ^C%                                                                                       
```

We can automate PyPI deployment using GitHub Actions continuous integration and deployment (CI/CD). The deployment will trigger when we push git tags that match the glob query `v.*.*`.
```console
$ mkdir -p .github/workflows                             
$ touch .github/workflows/pypi.yaml                      
$ code .github/workflows/pypi.yaml
$ cat .github/workflows/pypi.yaml
name: PyPI

on:
  push:
    tags:
      # run whenever a version tag is pushed, e.g. v1.1.0
      - "v*.*.*"
    paths-ignore:
      # don't run when docs are pushed
      - '**.md'
      - 'docs/**'
      - 'docsrc/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Publish GH release
        uses: softprops/action-gh-release@v1
      - name: Build using poetry and publish to PyPi
        uses: JRubics/poetry-publish@v1.8
        with:
          pypi_token: ${{ secrets.PYPI_TOKEN }}% 
```

Note that we would need to enter a valid [PyPI API token](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/?highlight=access%20token#saving-credentials-on-github) in GitHub secrets under the name `PYPI_TOKEN`.

Also note that as of writing, GitHub Actions offers unlimited Actions executions free of charge for public repositories.

Let's do some more work on our testing environment. [`tox`](https://tox.wiki/en/latest/) allows us to test our package against multiple Python versions, and it integrates with `poetry` and GitHub Actions. All we need is to install `tox` (`pip install tox`) and write a `tox.ini` file at the repository root:
```console
$ touch tox.ini                      
$ code tox.ini  
$ cat tox.ini
[tox]
isolated_build = true
envlist = py38

[testenv]
allowlist_externals = 
    poetry
commands =
    poetry install 
	; Check that the package is importable
    poetry run python -c 'import poetry_demo'
    poetry run pytest %                                                                                
$ tox          
.package create: /home/eho/ripl/repos/poetry-demo/.tox/.package
.package installdeps: poetry-core>=1.0.0
py38 create: /home/eho/ripl/repos/poetry-demo/.tox/py38
py38 inst: /home/eho/ripl/repos/poetry-demo/.tox/.tmp/package/1/poetry-demo-0.1.0.tar.gz
py38 installed: numpy==1.22.2,pandas==1.4.1,poetry-demo @ file:///home/eho/ripl/repos/poetry-demo/.tox/.tmp/package/1/poetry-demo-0.1.0.tar.gz,python-dateutil==2.8.2,pytz==2021.3,six==1.16.0
py38 run-test-pre: PYTHONHASHSEED='618313639'
py38 run-test: commands[0] | poetry install
Installing dependencies from lock file

Package operations: 10 installs, 0 updates, 0 removals

  • Installing pyparsing (3.0.7)
  • Installing attrs (21.4.0)
  • Installing iniconfig (1.1.1)
  • Installing packaging (21.3)
  • Installing pluggy (1.0.0)
  • Installing py (1.11.0)
  • Installing tomli (2.0.1)
  • Installing pytest (7.0.1)
  • Installing python-dotenv (0.19.2)
  • Installing pytest-dotenv (0.5.2)

Installing the current project: poetry-demo (0.1.0)
py38 run-test: commands[1] | poetry run python -c 'import poetry_demo'
py38 run-test: commands[2] | poetry run pytest
========================================= test session starts =========================================
platform linux -- Python 3.8.10, pytest-7.0.1, pluggy-1.0.0
cachedir: .tox/py38/.pytest_cache
rootdir: /home/eho/ripl/repos/poetry-demo
plugins: dotenv-0.5.2
collected 0 items                                                                                     

======================================== no tests ran in 0.29s ========================================
ERROR: InvocationError for command /home/eho/.poetry/bin/poetry run pytest (exited with code 5)
_______________________________________________ summary _______________________________________________
ERROR:   py38: commands failed
```

Tox reports failure because we don't have any real pytests (functions named like `test_*`) in the directory `./tests`.
We can set up a GitHub Actions workflow that automatically runs tox on pushes to pull requests or the `main` branch:

```console
$ touch .github/workflows/tox.yaml
$ code .github/workflows/tox.yaml
$ cat .github/workflows/tox.yaml
name: Tox

on:
  push:
    branches:
      - main
    paths-ignore:
      - '**.md'
      - 'docs/**'
      - 'docsrc/**'

  pull_request:
    branches:
      - main
    paths-ignore:
      - '**.md'
      - 'docs/**'
      - 'docsrc/**'

jobs:
  test:
    name: Run unit tests in tox
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.7
        uses: actions/setup-python@v2
        with:
          python-version: '3.7'
      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install Python dependencies
        run: python -m pip install -q poetry tox
      - name: Run all tox tests
        if: github.event_name != 'pull_request'
        run: tox --
      - name: Run tox tests (fast only)
```

We'll add a standard Python `.gitignore` file:

```console
$ wget https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore 
--2022-02-28 15:00:34--  https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.111.133, 185.199.108.133, 185.199.109.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2762 (2.7K) [text/plain]
Saving to: ‘Python.gitignore’

Python.gitignore         100%[==================================>]   2.70K  --.-KB/s    in 0.001s  

2022-02-28 15:00:35 (2.12 MB/s) - ‘Python.gitignore’ saved [2762/2762]
FINISHED --2022-02-28 15:00:35--
Total wall clock time: 0.1s
Downloaded: 1 files, 2.7K in 0.001s (2.12 MB/s)
$ mv Python.gitignore .gitignore
```

Finally, we create our first git commit and push our changes to a new GitHub repository using the [GitHub CLI](https://cli.github.com/).

```console
$ git add .
$ git commit -m 'Initial commit'
❯ gh repo create                  
? What would you like to do? Push an existing local repository to GitHub
? Path to local repository .
? Repository name poetry-demo
? Description Example Python package using poetry, tox, and GitHub Actions
? Visibility Public
✓ Created repository ethho/poetry-demo on GitHub
? Add a remote? Yes
? What should the new remote be called? origin
✓ Added remote git@github.com:ethho/poetry-demo.git
? Would you like to push commits from the current branch to the "origin"? Yes
✓ Pushed commits to git@github.com:ethho/poetry-demo.git
$ gh repo view --web
```