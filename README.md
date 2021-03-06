# playwbot
[Playwright-python](https://github.com/microsoft/playwright-python) wrapper for [RobotFramework](https://robotframework.org/).

## Installation

### From the repository

- clone the repo
- easiest way is to use [poetry](https://python-poetry.org/) and run `poetry install` and then `poetry shell`
- to be able to run the tests, install the package for the development by `python setup.py develop`
- RF tests are run by standard command `robot <path>`

### From the Pypi

- if using poetry, run `poetry add playwbot` and then `poetry install`
- if using pip, run `pip install playwbot`

### Download the playwright browser binaries

This project is using [poetry](https://python-poetry.org/) as package management tool. One drawback of that is,
that is does not support post-install scripts.

Therefore, once you install the library, do not forget to execute the command:

```
python -m playwright install
```

This will download binaries of all supported browsers.

## Importing module into the RF suite

- if you have the file directly accesible, just point directly to the location, like this

```
Library    /some/path/to/the/library/Playwbot.py    browser=<chromium|firefox|webkit>
```

- if you installed it from Pypi, then import it like this

```
Library    playwbot.Playwbot    browser=<chromium|firefox|webkit>
```

## RobotFramework-style documentation

Is available here https://radekbednarik.github.io/playwbot/

