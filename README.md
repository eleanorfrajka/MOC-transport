# MOC transports

Amocarray is a python package for reading AMOC transport data from transport mooring arrays.  It does not modify, fix or grid data.  Functionality currently includes:

- loading data from the RAPID 26°N array, OSNAP array, MOVE 16°N array and SAMBA 34.5°S array.

This is a work in progress, all contributions welcome!

### Install

Install from PyPI with
```sh
python -m pip install amocarray
```

### Documentation

Documentation is available at [https://amoccommunity.github.io/amocarray](https://amoccommunity.github.io/amocarray/).

Check out the demo notebook `notebooks/demo.ipynb` for example functionality.

As input, amocarray downloads data from the observing arrays.

### Contributing

All contributions are welcome!  See [contributing](CONTRIBUTING.md) for more details.

To install a local, development version of amocarray, clone the repository, open a terminal in teh root directory (next to this readme file) and run these commands:

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

### Initial plans


The **initial plan** for this repository is to simply load the volume transports as published by different AMOC observing arrays and replicate (update) the figure from Frajka-Williams et al. (2019) [10.3389/fmars.2019.00260](https://doi.org/10.3389/fmars.2019.00260).

<img width="358" alt="image" src="https://github.com/user-attachments/assets/fb35a276-a41e-4cef-b78f-9c3c46710466" />
