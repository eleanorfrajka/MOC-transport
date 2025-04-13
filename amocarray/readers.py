import xarray as xr
from pathlib import Path

from typing import Union

from amocarray import logger
from amocarray.read_move import read_move
from amocarray.read_rapid import read_rapid
from amocarray.read_osnap import read_osnap
from amocarray.read_samba import read_samba

log = logger.log

# Dropbox location Public/linked_elsewhere/amocarray_data/
server = "https://www.dropbox.com/scl/fo/4bjo8slq1krn5rkhbkyds/AM-EVfSHi8ro7u2y8WAcKyw?rlkey=16nqlykhgkwfyfeodkj274xpc&dl=0"


def _get_reader(array_name: str):
    """
    Return the reader function for the given array name.

    Parameters
    ----------
    array_name : str
        The name of the observing array.

    Returns
    -------
    function
        Reader function corresponding to the given array name.

    Raises
    ------
    ValueError
        If an unknown array name is provided.
    """
    readers = {
        "move": read_move,
        "rapid": read_rapid,
        "osnap": read_osnap,
        "samba": read_samba,
    }
    try:
        return readers[array_name.lower()]
    except KeyError:
        raise ValueError(
            f"Unknown array name: {array_name}. Valid options are: {list(readers.keys())}"
        )


def load_sample_dataset(
    array_name: str = "rapid", enable_logging: bool = False
) -> xr.Dataset:
    """
    Load a sample dataset for quick testing.

    Currently supports:
    - 'rapid' : loads the 'RAPID_26N_TRANSPORT.nc' file

    Parameters
    ----------
    array_name : str, optional
        The name of the observing array to load. Default is 'rapid'.
    enable_logging : bool, optional
        If True, setup and write logs. If False, suppress logging. Default is False.

    Returns
    -------
    xr.Dataset
        A single xarray Dataset from the sample file.

    Raises
    ------
    ValueError
        If the array_name is not recognised.
    """
    if array_name.lower() == "rapid":
        sample_file = "moc_transports.nc"
        datasets = load_dataset(
            array_name=array_name,
            file_list=sample_file,
            transport_only=True,
            enable_logging=enable_logging,
        )
        if not datasets:
            raise FileNotFoundError(
                f"No datasets were loaded for sample file: {sample_file}"
            )
        return datasets[0]

    raise ValueError(
        f"Sample dataset for array '{array_name}' is not defined. "
        "Currently only 'rapid' is supported."
    )


def load_dataset(
    array_name: str,
    source: str = None,
    file_list: Union[str | list[str]] = None,
    transport_only: bool = True,
    data_dir: Union[str, Path, None] = None,
    redownload: bool = False,
    enable_logging: bool = True,
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
    transport_only : bool, optional
        If True, restrict to transport files only.
    data_dir : str, optional
        Local directory for downloaded files.
    redownload : bool, optional
        If True, force redownload of the data.

    Returns
    -------
    list of xarray.Dataset
        List of datasets loaded from the specified array.

    Raises
    ------
    ValueError
        If an unknown array name is provided.
    """
    # Set up logger for this run
    if enable_logging:
        logger.setup_logger(array_name=array_name, output_dir="logs")

    # Use logger globally
    log = logger.log
    log.info(f"Loading dataset for array: {array_name}")

    reader = _get_reader(array_name)
    datasets = reader(
        source=source,
        file_list=file_list,
        transport_only=transport_only,
        data_dir=data_dir,
        redownload=redownload,
    )

    log.info(f"Successfully loaded {len(datasets)} dataset(s) for array: {array_name}")

    return datasets
