import os
from pathlib import Path
from typing import Union

import xarray as xr

from amocarray.read_move import read_move
from amocarray.read_osnap import read_osnap
from amocarray.read_rapid import read_rapid
from amocarray.read_samba import read_samba

# Dropbox location Public/linked_elsewhere/amocarray_data/
server = "https://www.dropbox.com/scl/fo/4bjo8slq1krn5rkhbkyds/AM-EVfSHi8ro7u2y8WAcKyw?rlkey=16nqlykhgkwfyfeodkj274xpc&dl=0"

# Registry of available readers
_READERS = {
    "move": read_move,
    "rapid": read_rapid,
    "osnap": read_osnap,
    "samba": read_samba,
}


def load_sample_dataset(
    dataset_name: str = "moc_transports.nc", data_dir: str = "../data"
) -> xr.Dataset:
    """
    Load a sample dataset from the local data directory.

    Parameters
    ----------
    dataset_name : str, optional
        The name of the dataset file. Default is "moc_transports.nc".
    data_dir : str, optional
        The local directory where the dataset is stored. Default is "../data".

    Returns
    -------
    xarray.Dataset
        The loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the specified dataset file does not exist in the given directory.
    """
    file_path = os.path.join(data_dir, dataset_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"{dataset_name} not found in the {data_dir} directory."
        )

    return xr.open_dataset(file_path)


def load_dataset(
    array_name: str,
    source: str = None,
    file_list: Union[str | list[str]] = None,
    transport_only: bool = True,
    data_dir: Union[str, Path, None] = None,
    redownload: bool = False,
) -> list[xr.Dataset]:
    """
    Load raw datasets from a selected AMOC observing array.

    Parameters
    ----------
    array_name : str
        The name of the observing array to load. Options are:
        - 'move' : MOVE 16N array
        - 'rapid' : RAPID 26N array
        - 'osnap' : OSNAP array
        - 'samba' : SAMBA 34S array
    source : str, optional
        URL or local path to the data source.
        If None, the reader-specific default source will be used.
    file_list : str or list of str, optional
        Filename or list of filenames to process.
        If None, the reader-specific default files will be used.

    Returns
    -------
    list of xarray.Dataset
        List of datasets loaded from the specified array.

    Raises
    ------
    ValueError
        If an unknown array name is provided.
    """
    reader = _get_reader(array_name)
    return reader(
        source=source,
        file_list=file_list,
        transport_only=transport_only,
        data_dir=data_dir,
        redownload=redownload,
    )


def _get_reader(array_name: str) -> callable:
    """
    Retrieve the reader function for a given observing array.

    Parameters
    ----------
    array_name : str
        Name of the observing array.

    Returns
    -------
    callable
        The reader function corresponding to the requested array.

    Raises
    ------
    ValueError
        If no reader is registered for the given array name.
    """
    try:
        return _READERS[array_name.lower()]
    except KeyError:
        raise ValueError(
            f"No reader found for '{array_name}'. Available options: {list(_READERS.keys())}"
        )
