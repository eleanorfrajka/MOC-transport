import os
import xarray as xr

from amocarray import utilities

# Default file list
OSNAP_DEFAULT_FILES = [
    'OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc',
    'OSNAP_Streamfunction_201408_202006_2023.nc',
    'OSNAP_Gridded_TSV_201408_202006_2023.nc'
]
OSNAP_TRANSPORT_FILES = ["OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc"]

# Mapping of filenames to download URLs
OSNAP_FILE_URLS = {
    'README_OSNAP-MOC_202306.doc': 'https://repository.gatech.edu/bitstreams/930261ff-6cca-4cf9-81c8-d27c51a4ca49/download',
    'OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc': 'https://repository.gatech.edu/bitstreams/e039e311-dd2e-4511-a525-c2fcfb3be85a/download',
    'OSNAP_Streamfunction_201408_202006_2023.nc': 'https://repository.gatech.edu/bitstreams/5edf4cba-a28f-40a6-a4da-24d7436a42ab/download',
    'OSNAP_Gridded_TSV_201408_202006_2023.nc': 'https://repository.gatech.edu/bitstreams/598f200a-50ba-4af0-96af-bd29fe692cdc/download'
}

# General metadata (global for OSNAP)
OSNAP_METADATA = {
    "project": "Overturning in the Subpolar North Atlantic Program (OSNAP)",
    "weblink": "https://www.o-snap.org",
    "comment": "Dataset accessed and processed via http://github.com/AMOCcommunity/amocarray",
    "acknowledgement": "OSNAP data were collected and made freely available by the OSNAP (Overturning in the Subpolar North Atlantic Program) project and all the national programs that contribute to it (www.o-snap.org).",
    "doi": "https://doi.org/10.35090/gatech/70342"
}

# File-specific metadata (placeholder, ready to extend)
OSNAP_FILE_METADATA = {
    'OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc': {
        "data_product": "Time series of MOC, MHT, and MFT",
    },
    'OSNAP_Streamfunction_201408_202006_2023.nc': {
        "data_product": "Meridional overturning streamfunction",
    },
    'OSNAP_Gridded_TSV_201408_202006_2023.nc': {
        "data_product": "Gridded temperature, salinity, and velocity",
    },
}


def read_osnap(source: str, file_list: str | list[str], transport_only: bool = True,
               data_dir=None, redownload=False) -> list[xr.Dataset]:  
    """
    Load the OSNAP transport datasets from a URL or local file path into xarray Datasets.

    Parameters
    ----------
    source : str, optional
        URL or local path to the NetCDF file(s). If None, will use predefined URLs per file.
    file_list : str or list of str, optional
        Filename or list of filenames to process.
        Defaults to OSNAP_DEFAULT_FILES.

    Returns
    -------
    list of xr.Dataset
        List of loaded xarray datasets with basic inline and file-specific metadata.

    Raises
    ------
    ValueError
        If no source is provided for a file and no default URL mapping is found.
    FileNotFoundError
        If the file cannot be downloaded or does not exist locally.
    """
    source = utilities.get_local_file(source, data_dir, redownload)
    # Ensure file_list has a default
    if file_list is None:
        file_list = OSNAP_DEFAULT_FILES
    if transport_only:
        file_list = OSNAP_TRANSPORT_FILES
    if isinstance(file_list, str):
        file_list = [file_list]

    datasets = []

    for file in file_list:
        if not file.endswith(".nc"):
            continue

        # Determine source: either user-provided or from mapping
        file_source = source or OSNAP_FILE_URLS.get(file)
        if not file_source:
            raise ValueError(f"No source provided for '{file}' and no default URL mapping found.")

        # Prepare file path
        if utilities._is_valid_url(file_source):
            file_url = f"{file_source}"
            dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            try:
                file_path = utilities.download_file(file_url, dest_folder)
            except Exception as e:
                raise FileNotFoundError(f"Failed to download {file_url}: {e}")
        else:
            file_path = os.path.join(file_source, file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Local file not found: {file_path}")

        # Open dataset
        try:
            ds = xr.open_dataset(file_path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to open NetCDF file: {file_path}: {e}")

        # Attach metadata
        file_metadata = OSNAP_FILE_METADATA.get(file, {})
        utilities.safe_update_attrs(
            ds,
            {
                "source_file": file,
                "source_path": file_source,
                **OSNAP_METADATA,
                **file_metadata,
            }
        )

        datasets.append(ds)

    if not datasets:
        raise FileNotFoundError(f"No valid NetCDF files found in {file_list}")

    return datasets
