from pathlib import Path
from typing import Union

import xarray as xr

from amocarray import utilities, logger
from amocarray.utilities import apply_defaults

log = logger.log  # ✅ use the global logger

# Default source and file list
MOVE_DEFAULT_SOURCE = "https://mooring.ucsd.edu/move/nc/"
MOVE_DEFAULT_FILES = ["OS_MOVE_TRANSPORTS.nc"]
MOVE_TRANSPORT_FILES = ["OS_MOVE_TRANSPORTS.nc"]

# Global metadata for MOVE
MOVE_METADATA = {
    "description": "MOVE transport estimates dataset from UCSD mooring project",
    "project": "Meridional Overturning Variability Experiment (MOVE)",
    "weblink": "https://mooring.ucsd.edu/move/",
    "comment": "Dataset accessed and processed via http://github.com/AMOCcommunity/amocarray",
    # DOI can be added here when available
    "acknowledgement": "The MOVE project is made possible with funding from the NOAA Climate Program Office. Initial funding came from the German Bundesministerium fuer Bildung und Forschung.",
}

# File-specific metadata placeholder
MOVE_FILE_METADATA = {
    "OS_MOVE_TRANSPORTS.nc": {
        "data_product": "MOVE transport time series",
        # Add specific acknowledgments here if needed in future
    },
}


@apply_defaults(MOVE_DEFAULT_SOURCE, MOVE_DEFAULT_FILES)
def read_move(
    source: str,
    file_list: str | list[str],
    transport_only: bool = True,
    data_dir: Union[str, Path, None] = None,
    redownload: bool = False,
) -> list[xr.Dataset]:
    """
    Load the MOVE transport dataset from a URL or local file path into xarray Datasets.

    Parameters
    ----------
    source : str, optional
        URL or local path to the NetCDF file(s).
        Defaults to the MOVE data repository URL.
    file_list : str or list of str, optional
        Filename or list of filenames to process.
        Defaults to MOVE_DEFAULT_FILES.
    transport_only : bool, optional
        If True, restrict to transport files only.
    data_dir : str, Path or None, optional
        Optional local data directory.
    redownload : bool, optional
        If True, force redownload of the data.

    Returns
    -------
    list of xr.Dataset
        List of loaded xarray datasets with basic inline and file-specific metadata.

    Raises
    ------
    ValueError
        If the source is neither a valid URL nor a directory path.
    FileNotFoundError
        If the file cannot be downloaded or does not exist locally.
    """
    log.info("Starting to read MOVE dataset")

    if transport_only:
        file_list = MOVE_TRANSPORT_FILES
    if isinstance(file_list, str):
        file_list = [file_list]

    local_data_dir = Path(data_dir) if data_dir else utilities.get_default_data_dir()
    local_data_dir.mkdir(parents=True, exist_ok=True)

    datasets = []

    for file in file_list:
        if not file.lower().endswith(".nc"):
            log.warning("Skipping non-NetCDF file: %s", file)
            continue

        download_url = (
            f"{source.rstrip('/')}/{file}" if utilities._is_valid_url(source) else None
        )

        file_path = utilities.resolve_file_path(
            file_name=file,
            source=source,
            download_url=download_url,
            local_data_dir=local_data_dir,
            redownload=redownload,
        )

        # Open dataset
        try:
            log.info("Opening MOVE dataset: %s", file_path)
            ds = xr.open_dataset(file_path)
        except Exception as e:
            log.error("Failed to open NetCDF file: %s: %s", file_path, e)
            raise FileNotFoundError(f"Failed to open NetCDF file: {file_path}: {e}")

        # Attach metadata
        file_metadata = MOVE_FILE_METADATA.get(file, {})
        log.info("Attaching metadata to dataset from file: %s", file)
        utilities.safe_update_attrs(
            ds,
            {
                "source_file": file,
                "source_path": str(file_path),
                **MOVE_METADATA,
                **file_metadata,
            },
        )

        datasets.append(ds)

    if not datasets:
        log.error("No valid NetCDF files found in %s", file_list)
        raise FileNotFoundError(f"No valid NetCDF files found in {file_list}")

    log.info("Successfully loaded %d MOVE dataset(s)", len(datasets))
    return datasets
