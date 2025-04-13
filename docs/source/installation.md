# Installation

To install the latest released version of this package from PyPI, use
```sh
python -m pip install amocarray
```
This allows you to import the package into a python file or notebook with:
```python
import amocarray
```
### Install for contributing

Or, to install a local, development version of amocarray, clone the repository, open a terminal in teh root directory (next to this readme file) and run these commands:

```sh
git clone https://github.com/AMOCcommunity/amocarray.git
cd amocarray
pip install -r requirements-dev.txt
pip install -e .
```
This installs amocarray locally.  The `-e` ensures that any edits you make in the files will be picked up by scripts that impport functions from glidertest.

You can run the example jupyter notebook by launching jupyterlab with `jupyter-lab` and navigating to the `notebooks` directory, or in VS Code or another python GUI.

All new functions should include tests.  You can run tests locally and generate a coverage reporrt with:
```sh
pytest --cov=amocarray --cov-report term-missing tests/
```

Try to ensure that all the lines of your contribution are covered in the tests.
