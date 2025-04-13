# MOC transports

**Clean, modular loading of AMOC observing array datasets, with optional structured logging and metadata enrichment.**

> AMOCarray provides a unified system to access and process data from major Atlantic Meridional Overturning Circulation (AMOC) observing arrays:
> - MOVE (16°N)
> - RAPID (26°N)
> - OSNAP (Subpolar North Atlantic)
> - SAMBA (34.5°S)

The project emphasizes clarity, reproducibility, and modular design, with per-dataset logging, metadata handling, and testable utilities.

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

### Quickstart

#### Load a sample dataset
```python
from amocarray import readers

# Load RAPID sample dataset
ds = readers.load_sample_dataset("rapid")
print(ds)
```

#### Load a full dataset

```python
from amocarray import readers

datasets = readers.load_dataset("osnap")
for ds in datasets:
    print(ds)
```
A `*.log` file will be written to `logs/` by default.

Data will be cached in `~/.amocarray_data/` unless you specify a custom location.

### Project structure

```
amocarray/
│
├── readers.py               # Orchestrator for loading datasets
├── read_move.py             # MOVE reader
├── read_rapid.py            # RAPID reader
├── read_osnap.py            # OSNAP reader
├── read_samba.py            # SAMBA reader
│
├── utilities.py             # Shared utilities (downloads, parsing, etc.)
├── logger.py                # Structured logging setup
│
└── tests/                   # Unit tests
```

### Roadmap

- [] Add test coverage for utilities and readers
- [] Add dataset summary output at end of load_dataset()
- [] Optional global logging helpers (disable_logging(), enable_logging())
- [] Extend load_sample_dataset() to support all arrays
- [] Metadata enrichment (source paths, processing dates)


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



## Acknowledgements

- MOVE data: NOAA Climate Program Office and German Bundesministerium für Bildung und Forschung.
- OSNAP data: www.o-snap.org
- SAMBA data: NOAA AOML, Met Office, and associated research projects.
- RAPID data: RAPID-MOCHA-WBTS collaboration.

Dataset access and processing via [AMOCarray](https://github.com/AMOCcommunity/amocarray).
