import os
import pandas as pd
import xarray as xr

from amocarray import utilities

# Default file list
SAMBA_DEFAULT_FILES = [
    "Upper_Abyssal_Transport_Anomalies.txt",
    "MOC_TotalAnomaly_and_constituents.asc"
]
SAMBA_TRANSPORT_FILES = [
    "Upper_Abyssal_Transport_Anomalies.txt",
    "MOC_TotalAnomaly_and_constituents.asc"
]
# Mapping of filenames to remote URLs
SAMBA_FILE_URLS = {
    "Upper_Abyssal_Transport_Anomalies.txt": "ftp://ftp.aoml.noaa.gov/phod/pub/SAM/2020_Kersale_etal_ScienceAdvances/",
    "MOC_TotalAnomaly_and_constituents.asc": "https://www.aoml.noaa.gov/phod/SAMOC_international/documents/"
}

# Global metadata for SAMBA
SAMBA_METADATA = {
    "description": "SAMBA 34S transport estimates dataset",
    "project": "South Atlantic MOC Basin-wide Array (SAMBA)",
    "weblink": "https://www.aoml.noaa.gov/phod/SAMOC_international/",
    "comment": "Dataset accessed and processed via http://github.com/AMOCcommunity/amocarray",
    "acknowledgement": "SAMBA data were collected and made freely available by the SAMOC international project and contributing national programs.",
    # Add DOI here when available
}

# File-specific metadata placeholders
SAMBA_FILE_METADATA = {
    "Upper_Abyssal_Transport_Anomalies.txt": {
        "data_product": "Daily volume transport anomaly estimates for the upper and abyssal cells of the MOC",
        "acknowledgement": "M. Kersalé et al., Highly variable upper and abyssal overturning cells in the South Atlantic. Sci. Adv. 6, eaba7573 (2020). DOI: 10.1126/sciadv.aba7573",
    },
    "MOC_TotalAnomaly_and_constituents.asc": {
        "data_product": "Daily travel time values, calibrated to a nominal pressure of 1000 dbar, and bottom pressures from the two PIES/CPIES moorings",
        "acknowledgement": "Meinen, C. S., Speich, S., Piola, A. R., Ansorge, I., Campos, E., Kersalé, M., et al. (2018). Meridional overturning circulation transport variability at 34.5°S during 2009–2017: Baroclinic and barotropic flows and the dueling influence of the boundaries. Geophysical Research Letters, 45, 4180–4188. https://doi.org/10.1029/2018GL077408",
    },
}




def read_samba(source: str = None,
               file_list: str | list[str] = None, transport_only: bool = True) -> list[xr.Dataset]:
    """
    Load the SAMBA transport datasets from remote URL or local file path into xarray Datasets.

    Parameters
    ----------
    source : str, optional
        URL or local path to the dataset directory. If None, will use predefined URLs per file.
    file_list : str or list of str, optional
        Filename or list of filenames to process.
        Defaults to SAMBA_DEFAULT_FILES.

    Returns
    -------
    list of xr.Dataset
        List of loaded xarray datasets with basic inline and file-specific metadata.

    Raises
    ------
    ValueError
        If no source is provided for a file and no default URL mapping found.
    FileNotFoundError
        If the file cannot be downloaded or does not exist locally.
    """
    # Ensure file_list has a default
    if file_list is None:
        file_list = SAMBA_DEFAULT_FILES
    if transport_only:
        file_list = SAMBA_TRANSPORT_FILES
    if isinstance(file_list, str):
        file_list = [file_list]

    datasets = []

    for file in file_list:
        if not (file.lower().endswith(".txt") or file.lower().endswith(".asc")):
            continue

        # Determine source: use passed source or file-specific URL
        file_source = source or SAMBA_FILE_URLS.get(file)
        if not file_source:
            raise ValueError(f"No source provided for '{file}' and no default URL mapping found.")

        # Prepare file path
        if utilities._is_valid_url(file_source):
            file_url = f"{file_source.rstrip('/')}/{file}"
            dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            try:
                file_path = utilities.download_file(file_url, dest_folder)
            except Exception as e:
                raise FileNotFoundError(f"Failed to download {file_url}: {e}")
        else:
            file_path = os.path.join(file_source, file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Local file not found: {file_path}")

        # Parse ASCII file
        try:
            column_names, _ = utilities.parse_ascii_header(file_path, comment_char="%")
            df = utilities.read_ascii_file(file_path, comment_char="%")
            df.columns = column_names
        except Exception as e:
            raise FileNotFoundError(f"Failed to parse ASCII file: {file_path}: {e}")

        # Time handling
        if "Upper_Abyssal" in file:
            df["TIME"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour", "Minute"]])
            df = df.drop(columns=["Year", "Month", "Day", "Hour", "Minute"])
        else:
            df["TIME"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour"]])
            df = df.drop(columns=["Year", "Month", "Day", "Hour"])

        # Convert to xarray
        ds = df.set_index("TIME").to_xarray()

        # Attach metadata
        file_metadata = SAMBA_FILE_METADATA.get(file, {})
        utilities.safe_update_attrs(
            ds,
            {
                "source_file": file,
                "source_path": file_source,
                **SAMBA_METADATA,
                **file_metadata,
            }
        )

        datasets.append(ds)

    if not datasets:
        raise FileNotFoundError(f"No valid data files found in {file_list}")

    return datasets

