import pathlib
import sys

import pytest

script_dir = pathlib.Path(__file__).parent.absolute()
parent_dir = script_dir.parents[0]
sys.path.append(str(parent_dir))

from amocarray import readers


def test_load_dataset_move():
    datasets = readers.load_dataset("move")
    assert isinstance(datasets, list)
    assert all(hasattr(ds, "attrs") for ds in datasets)
    assert len(datasets) > 0


def test_load_dataset_rapid():
    datasets = readers.load_dataset("rapid")
    print(type(datasets))
    assert isinstance(datasets, list)
    assert all(hasattr(ds, "attrs") for ds in datasets)
    assert len(datasets) > 0


def test_load_dataset_osnap():
    datasets = readers.load_dataset("osnap")
    assert isinstance(datasets, list)
    assert all(hasattr(ds, "attrs") for ds in datasets)
    assert len(datasets) > 0


def test_load_dataset_samba():
    datasets = readers.load_dataset("samba")
    assert isinstance(datasets, list)
    assert all(hasattr(ds, "attrs") for ds in datasets)
    assert len(datasets) > 0


def test_load_dataset_invalid_array():
    with pytest.raises(ValueError, match="No reader found for 'invalid'"):
        readers.load_dataset("invalid")
