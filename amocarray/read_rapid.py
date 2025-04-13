import os

import xarray as xr

# Import the modules used
from amocarray import utilities
# Import the apply_defaults decorator function directly
from amocarray.utilities import apply_defaults

# Inline metadata dictionary
RAPID_METADATA = {
    "description": "RAPID 26N transport estimates dataset",
    "project": "RAPID-AMOC 26°N array",
    "web_link": "https://rapid.ac.uk/rapidmoc",
    "note": "Dataset accessed and processed via xarray",
}

RAPID_DEFAULT_SOURCE = "https://rapid.ac.uk/sites/default/files/rapid_data/"
RAPID_TRANSPORT_FILES = ["moc_transports.nc"]

# Default list of RAPID data files
RAPID_DEFAULT_FILES = [
    'moc_vertical.nc',
    'ts_gridded.nc',
    'moc_transports.nc'
]
#https://rapid.ac.uk/sites/default/files/rapid_data/ts_gridded.nc
#https://rapid.ac.uk/sites/default/files/rapid_data/moc_vertical.nc
#https://rapid.ac.uk/sites/default/files/rapid_data/moc_transports.nc
@apply_defaults(RAPID_DEFAULT_SOURCE, RAPID_DEFAULT_FILES)
def read_rapid(source: str, file_list: str | list[str], transport_only: bool = True, data_dir=None, redownload=False) -> list[xr.Dataset]:    
    """
    Load the RAPID transport dataset from a URL or local file path into an xarray.Dataset.

    Parameters
    ----------
    source : str, optional
        URL or local path to the NetCDF file(s).
        Defaults to the RAPID data repository URL.
    file_list : str or list of str, optional
        Filename or list of filenames to process.
        If None, will attempt to list files in the source directory.

    Returns
    -------
    xr.Dataset
        The loaded xarray dataset with basic inline metadata.

    Raises
    ------
    ValueError
        If the source is neither a valid URL nor a directory path.
    FileNotFoundError
        If no valid NetCDF files are found in the provided file list.
    """
    source = utilities.get_local_file(source, data_dir, redownload)
    if file_list is None:
        file_list = RAPID_DEFAULT_FILES
    if transport_only:
        file_list = RAPID_TRANSPORT_FILES
    if isinstance(file_list, str):
        file_list = [file_list]

    # Determine the list of files to process
    if utilities._is_valid_url(source):
        if file_list is None:
            file_list = utilities.list_files_in_https_server(source)
    elif utilities._is_valid_file(source) or os.path.isdir(source):
        if file_list is None:
            file_list = os.listdir(source)
    else:
        raise ValueError("Source must be a valid URL or directory path.")

    datasets = []

    for file in file_list:
        if not file.endswith(".nc"):
            continue

        # Prepare file path
        if utilities._is_valid_url(source):
            file_url = f"{source.rstrip('/')}/{file}"
            dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            file_path = utilities.download_file(file_url, dest_folder)
        else:
            file_path = os.path.join(source, file)

        # Open dataset
        ds = xr.open_dataset(file_path)

        # Attach metadata
        utilities.safe_update_attrs(
            ds,
            {
                "source_file": file,
                "source_path": source,
                **RAPID_METADATA,
            }
        )

        datasets.append(ds)

    if not datasets:
        raise FileNotFoundError(f"No valid NetCDF files found in {file_list}")

    # For now, return the first dataset (optionally merge later)
    return datasets
