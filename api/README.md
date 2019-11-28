# pico API

This is the core of the pico platform: a [Flask](http://flask.palletsprojects.com)-based REST API that manages challenges, users,
and all other aspects of CTF-style competitions. While technically standalone, it is typically
used in conjunction with other aspects of the platform, such as the **[UI](../ui)**,
**[webshell](../webshell)**, and **[challenges](../challenges)**. pico API containers are stateless
and can be horizontally scaled and load-balanced.

## Configuration

The API requires access to [MongoDB](https://www.mongodb.com/) and [Redis](https://redis.io/) databases.
The default connection info for these can be found along with other Flask configuration settings
in **[`config/default_settings.py`](./config/default_settings.py)**.

To override these, volume a `custom_settings.py` file into the `config` directory.

## Local Development

For the purposes of local development (autocompletion, etc.), it may be useful to install
the pip dependencies: `pip install -r requirements-dev.txt`.

While possible to run the API natively using `flask run` or a WSGI server, it is recommended
to simply rebuild the API container within the existing docker-compose network
(see the **[platform README](../README.md)** for more information).

## Cache Daemon

The cache daemon is a script which continually caches the results of several statistical API calls.
All deployments of the pico platform should have a single instance of the API container with
the cache daemon script as its entrypoint, as some score/scoreboard-related API calls are
dependent on it in order to return accurate results.

## Tests

*@todo: tests are outdated and/or broken*

Integration and load tests are located within in the `tests` directory.
The integration tests run automatically against any opened pull requests.

## Code Style

- In general, follow [PEP8](https://www.python.org/dev/peps/pep-0008/) conventions
- Docstrings should adhere to [PEP 257](https://www.python.org/dev/peps/pep-0257)
  - [pydocstyle](https://pypi.org/project/pydocstyle/) is a good tool for validating this
- Use [isort](https://github.com/timothycrosley/isort#readme) to organize imports
  - There is an `.isort.cfg` file provided in the repo root, so you should just have to run `isort -rv .`
  - If using Visual Studio Code, there is a built-in "Organize Imports" command
- Use [flake8](https://pypi.python.org/pypi/flake8) for linting
  - The `.flake8` file in the repo root contains customized settings for this project
- Run the [black code formatter](https://github.com/psf/black) (`black .`) before committing code

The `requirements-dev.txt` file will automatically install `flake8`, `pydocstyle`, `isort`, and `black`.
