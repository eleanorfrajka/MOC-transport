# Developer Guide for `amocarray`

<!-- omit in toc -->

Welcome to the `amocarray` Developer Guide!

This guide will help you set up your local development environment, understand the project structure, and contribute effectively to the project. Whether you're fixing bugs, adding new readers, or improving documentation, this guide is your starting point.

**Related resources:**

- [Coding conventions](https://amoccommunity.github.io/amocarray/conventions.html)
- [Housekeeping checklist](https://amoccommunity.github.io/amocarray/housekeeping.html)
- [Git collaboration](https://amoccommunity.github.io/amocarray/gitcollab.html)
- [Project actions](https://amoccommunity.github.io/amocarray/actions.html)

---

## Table of Contents

1. [Quickstart: First Contribution](#1-quickstart-first-contribution)
2. [Project Overview](#2-project-overview)
3. [Project Structure](#3-project-structure)
4. [Setting Up Development Environment](#4-setting-up-development-environment)
5. [Development Workflow](#5-development-workflow)
6. [Ignoring Local Files: ](#6-ignoring-local-files-gitignore-vs-gitinfoexclude)[`.gitignore`](#6-ignoring-local-files-gitignore-vs-gitinfoexclude)[ vs ](#6-ignoring-local-files-gitignore-vs-gitinfoexclude)[`.git/info/exclude`](#6-ignoring-local-files-gitignore-vs-gitinfoexclude)
7. [Commit Message Style Guide](#7-commit-message-style-guide)
8. [Logging and Debugging](#8-logging-and-debugging)
9. [Troubleshooting](#9-troubleshooting)
10. [Further Resources](#10-further-resources)

---

## 1. Quickstart: First Contribution

1. Fork the repository
2. Clone the upstream repository:

```bash
git clone https://github.com/AMOCcommunity/amocarray.git
cd amocarray
```

3. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Make your changes (update a doc, fix a function!)
5. Run tests and pre-commit checks:

```bash
pytest
pre-commit run --all-files
```

6. Push to your fork
7. Open a pull request 🚀

---

## 2. Project Overview

`amocarray` is a Python package to process and analyse data from AMOC observing arrays.\
It is designed to support researchers and data users by providing tools to read, standardise, and work with multiple datasets.

**Core goals:**

- Consistent handling of multiple AMOC arrays
- Easy integration of new data sources
- High code quality and reproducibility

---

## 3. Project Structure

```bash
amocarray/
├── amocarray/               # Core modules (readers, utilities, standardisation)
│   ├── readers.py           # High-level interface for loading datasets
│   ├── read_move.py         # Reader for MOVE data
│   ├── read_rapid.py        # Reader for RAPID data
│   ├── read_osnap.py        # Reader for OSNAP data
│   ├── read_samba.py        # Reader for SAMBA data
│   ├── utilities.py         # Helper functions (file handling, downloads, etc.)
│   ├── tools.py             # Unit conversions and data cleaning
│   ├── standardise.py       # Functions for dataset standardisation
│   ├── plotters.py          # Plotting utilities
│   ├── writers.py           # Data writing utilities
│   └── logger.py            # Project-wide structured logging
├── tests/                   # Unit tests
├── data/                    # Local data storage (downloads etc.)
├── docs/                    # Documentation sources (built with Sphinx)
├── notebooks/               # Jupyter notebooks for exploration and demos
├── .github/                 # GitHub workflows and actions
├── pyproject.toml           # Project metadata and build system config
├── CITATION.cff             # Citation file for this project
├── CONTRIBUTING.md          # Contribution guidelines
├── README.md                # Project overview and installation instructions
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Development dependencies
└── .pre-commit-config.yaml  # Pre-commit hooks configuration
```

### Project Management and Configuration Files

- `pyproject.toml`: Project metadata and build system configuration.
- `CITATION.cff`: Citation information for the project.
- `CONTRIBUTING.md`: Guidelines for contributors.
- `README.md`: Project overview, installation, and usage instructions.
- `.pre-commit-config.yaml`: Pre-commit hook configurations.

### Core Modules

- `readers.py`: Clean, high-level interface for loading datasets.
- `read_move.py`, `read_rapid.py`, etc.: Specific reader modules for MOVE, RAPID, OSNAP, SAMBA.
- `utilities.py`: Shared helper functions.
- `tools.py`: Unit conversions and data cleaning.
- `standardise.py`: Dataset standardisation functions.
- `logger.py`: Project-wide structured logging.
- `plotters.py`: Plotting utilities.
- `writers.py`: Data writing utilities.

---

## 4. Setting Up Development Environment

### Step 1: Clone the repository

```bash
git clone https://github.com/AMOCcommunity/amocarray.git
cd amocarray
```

### Step 2: Set up a virtual environment

In a terminal window, at the root of the repository (next to the `LICENSE` file), run
```bash
python3 -m venv venv
source venv/bin/activate && micromamba deactivate
```
Note the addition to the line `source venv/bin/activate`: the part `&& micromamba deactivate` is a safeguard in case you sometimes use micromamba.  It will ensure that you've deactivated any micromamba environments in this terminal.

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
If you have added or changed these, and want to make sure you have a clean install, you can do a
```bash
pip install -r requirements-dev.txt --force-reinstall
```
which will reinstall the packages at the newest version available.

### Step 4: (Optional) Install pre-commit hooks manually

We recommend running pre-commits to fix formatting and run tests, prior to making a pull request (or even prior to committing).  These will help you fix any problems you might otherwise encounter when the GitHub actions run the tests on your PR.

You can run pre-commit manually:

```bash
pre-commit run --all-files
```

Advanced (optional): If you know how to get these running, then to install hooks

```bash
pre-commit install
```

### Step 5: Build the documentation (optional)

```bash
cd docs
make html
```

---

## 5. Development Workflow

### Branching Model

- Work on feature branches from `main`.
- No enforced naming convention, but commonly we use: `Eleanor-patch-X`, where X increments for each patch.

### Fork & Pull Requests

- Fork the repository on GitHub.
- Push your changes to your fork.
- Open a pull request to `AMOCcommunity/amocarray`.

**See:** [Git collaboration guide](https://amoccommunity.github.io/amocarray/gitcollab.html)

### Keeping Your Fork Up To Date

```bash
git remote add upstream https://github.com/AMOCcommunity/amocarray.git
git fetch upstream
git merge upstream/main
```

---

## 6. Ignoring Local Files: `.gitignore` vs `.git/info/exclude`

When working with local files that should not be tracked by Git, you have two main options:

### `.gitignore`

- Lives in the root of the repository.
- Changes are **shared** with all contributors.
- Best for files or patterns that should be ignored project-wide (e.g., temporary build files, virtual environments).

Example entries:

```
__pycache__/
venv/
data/
```

### `.git/info/exclude`

- Personal, local ignores **specific to your environment**.
- Behaves like `.gitignore` but is **never committed**.
- Use for local files you want to ignore without affecting the shared project settings.

Example usage:

```
my_temp_outputs/
notes.txt
```

You can edit `.git/info/exclude` manually at any time.

### Best Practice

- Use `.gitignore` for project-wide ignores.
- Use `.git/info/exclude` for personal, local excludes — no risk of accidentally committing changes to shared ignore patterns!

---

## 7. Commit Message Style Guide

We use clear, consistent commit messages to make our history readable and to support changelog automation in the future.

### Format

```
[type] short description of the change
```

- Use **lowercase** for the description (except proper nouns).
- Keep it concise but descriptive (ideally under 72 characters).
- Use the imperative mood: "fix bug" not "fixed bug" or "fixes bug".

### Types

| Tag         | Purpose                                    |
|-------------|--------------------------------------------|
| `feat`      | New feature                                |
| `fix`       | Bug fix                                    |
| `docs`      | Documentation only changes                 |
| `style`     | Code style changes (formatting, no logic) |
| `refactor`  | Code improvements without behavior change |
| `test`      | Adding or improving tests                  |
| `ci`        | Changes to CI/CD pipelines                 |
| `chore`     | Maintenance or auxiliary tooling changes   |
| `cleanup`   | Removing old code or housekeeping          |

### Examples

```
fix osnap reader dimension handling
feat add metadata support for samba reader
docs update README with installation steps
test add coverage for utilities module
ci add pre-commit config for linting
cleanup remove deprecated functions from tools.py
```

### Why this matters

- ✅ Easier to read history
- ✅ Easier changelog generation (future automation-ready!)
- ✅ Helps reviewers quickly understand the purpose of commits

When in doubt, keep your commits small and focused!

---

## 8. Logging and Debugging

With PR #25, structured logging has been introduced to `amocarray`.

Logs track steps during data reading and, in the future, will also report changes during dataset standardisation.

### How logging works

Logging is handled in `logger.py` using:

```python
setup_logger(array_name, output_dir="logs")
```

- Creates a log file per array (MOVE, RAPID, OSNAP, etc.)
- Timestamped as: `YYYYMMDDTHH`
- Currently appends the string "read" — this may evolve to include other processes like standardisation.

### Enabling and disabling logging

Logging is controlled by the global variable `LOGGING_ENABLED` in `logger.py`.

You can toggle logging dynamically:

```python
from amocarray import logger
logger.enable_logging()
logger.disable_logging()
```

### Writing logs in modules

We wrap standard Python logging calls to allow toggling:

```python
from amocarray.logger import log_info, log_warning, log_error, log_debug
```

Then, in your code:

```python
log_info("Dataset successfully loaded.")
log_warning("Missing metadata detected.")
log_error("File not found.")
log_debug("Variable dimensions: %s", dims)
```

> **Note:** This departs from typical imports (`from amocarray import logger`) to keep calls clean and familiar: `log_info(...)` rather than `logger.log.info(...)`.

### Log levels

We use standard Python logging levels, with our most common being:

- `log_error`: Critical failures or exceptions.
- `log_warning`: Potential issues that do not stop execution.
- `log_info`: Useful process steps and confirmations.
- `log_debug`: Detailed diagnostic output.

All levels are currently captured:

```python
log.setLevel(logging.DEBUG)  # capture everything; handlers filter later
```

### Best practices

- ✅ Use logging to track important steps in your code.
- ✅ Log warnings for unusual but non-breaking behaviour.
- ✅ Use `log_debug` for rich details useful in debugging.
- ✅ Avoid excessive logging inside tight loops.

As `amocarray` expands, logs will play an increasing role in transparency and reproducibility.

---

## 9. Troubleshooting

### Pre-commit not running?
> Run manually:
> `pre-commit run --all-files`

### VSCode virtualenv not recognised?
> Ensure VSCode Python interpreter is set to `./venv/bin/python`.

### Tests failing due to missing data?
> Check your data directory is correctly set.

### Pre-commit `pytest` hook fails but `pytest` passes manually?
> Ensure your virtual environment is activated in your VSCode terminal settings.

### My commits are blocked by pre-commit errors?
> Fix all reported issues (linting, formatting, etc.) then try committing again.

---

## 10. Further Resources

- [amocarray User Documentation](https://amoccommunity.github.io/amocarray/)
- [OceanGliders Metadata Standards](https://github.com/OceanGlidersCommunity/ocean-gliders)
- [AMOC Community Project](https://www.amoccommunity.org/)

---

*This developer guide was prepared based on interactions with callumGPT and with ChatGPT to help structure and clarify.*

---

