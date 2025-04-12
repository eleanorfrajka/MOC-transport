import os
import xarray as xr

from amocarray import utilities
from amocarray.utilities import apply_defaults

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
    # Acknowledgement and DOI can be added here when available
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
def read_move(source: str, file_list: str | list[str], transport_only: bool = True) -> list[xr.Dataset]:    
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
    if transport_only:
        file_list = MOVE_TRANSPORT_FILES
    if isinstance(file_list, str):
        file_list = [file_list]
    datasets = []

    for file in file_list:
        if not file.lower().endswith(".nc"):
            continue

        # Validate source
        if utilities._is_valid_url(source):
            file_url = f"{source.rstrip('/')}/{file}"
            dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            try:
                file_path = utilities.download_file(file_url, dest_folder)
            except Exception as e:
                raise FileNotFoundError(f"Failed to download {file_url}: {e}")
        elif os.path.isdir(source):
            file_path = os.path.join(source, file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Local file not found: {file_path}")
        else:
            raise ValueError("Source must be a valid URL or directory path.")

        # Open dataset
        try:
            ds = xr.open_dataset(file_path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to open NetCDF file: {file_path}: {e}")

        # Attach metadata
        file_metadata = MOVE_FILE_METADATA.get(file, {})
        utilities.safe_update_attrs(
            ds, {
                "source_file": file,
                "source_path": source,
                **MOVE_METADATA,
                **file_metadata,
            })


        datasets.append(ds)

    if not datasets:
        raise FileNotFoundError(f"No valid NetCDF files found in {file_list}")

    return datasets