import xarray as xr
import os
from bs4 import BeautifulSoup
import requests
from pathlib import Path
from urllib.parse import urlparse
from ftplib import FTP
import pandas as pd

from amocarray import utilities
# Dropbox location Public/linked_elsewhere/amocarray_data/
server = "https://www.dropbox.com/scl/fo/4bjo8slq1krn5rkhbkyds/AM-EVfSHi8ro7u2y8WAcKyw?rlkey=16nqlykhgkwfyfeodkj274xpc&dl=0"

def download_file(url, dest_folder):
    """
    Download a file from HTTP(S) or FTP to the specified destination folder.

    Parameters:
        url (str): The URL of the file to download.
        dest_folder (str): Local folder to save the downloaded file.

    Returns:
        str: The full path to the downloaded file.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    local_filename = os.path.join(dest_folder, os.path.basename(url))
    print(local_filename)
    parsed_url = urlparse(url)

    if parsed_url.scheme in ("http", "https"):
        # HTTP(S) download
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    elif parsed_url.scheme == "ftp":
        # FTP download
        ftp = FTP(parsed_url.netloc)
        ftp.login()  # anonymous login
        with open(local_filename, 'wb') as f:
            ftp.retrbinary(f"RETR {parsed_url.path}", f.write)
        ftp.quit()

    else:
        raise ValueError(f"Unsupported URL scheme in {url}")

    return local_filename

def load_sample_dataset(dataset_name="moc_transports.nc", data_dir="../data"):
    """
    Load a sample dataset from the local data directory.

    Parameters:
    dataset_name (str): The name of the dataset file.
    data_dir (str): The local directory where the dataset is stored.

    Returns:
    xarray.Dataset: The loaded dataset.
    """
    file_path = os.path.join(data_dir, dataset_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{dataset_name} not found in the {data_dir} directory.")

    return xr.open_dataset(file_path)

def read_ascii_file(file_path, comment_char="#"):
    """
    Read an ASCII file into a pandas DataFrame, skipping lines starting with a specified comment character.

    Parameters:
        file_path (str): Path to the ASCII file.
        comment_char (str): Character denoting comment lines. Defaults to '#'.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    return pd.read_csv(file_path, sep=r"\s+", comment=comment_char, on_bad_lines="skip")


def download_ftp_file(url: str, dest_folder: str = "data"):
    """
    Download a file from an FTP URL and save it to the destination folder.

    Parameters:
        url (str): The full FTP URL to the file.
        dest_folder (str): Local folder to save the downloaded file.

    Returns:
        str: Path to the downloaded file.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    ftp_host = parsed_url.netloc
    ftp_file_path = parsed_url.path

    # Ensure destination folder exists
    os.makedirs(dest_folder, exist_ok=True)

    # Local filename
    local_filename = os.path.join(dest_folder, os.path.basename(ftp_file_path))

    print(f"Connecting to FTP host: {ftp_host}")
    with FTP(ftp_host) as ftp:
        ftp.login()  # anonymous guest login
        print(f"Downloading {ftp_file_path} to {local_filename}")
        with open(local_filename, 'wb') as f:
            ftp.retrbinary(f"RETR {ftp_file_path}", f.write)

    print(f"Download complete: {local_filename}")
    return local_filename

def parse_ascii_header(file_path: str, comment_char: str = "%") -> tuple[list, int]:
    """
    Parse the header of an ASCII file to extract column names and number of header lines.

    Header lines are identified by the given comment character (default: '%').
    Columns are defined in lines like:
    '<comment_char> Column 1: <column_name>'

    Parameters:
        file_path (str): Path to the ASCII file.
        comment_char (str): Character used to identify header lines.

    Returns:
        tuple: (list of column names, number of header lines to skip)
    """
    column_names = []
    header_line_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            header_line_count += 1
            if line.startswith(comment_char):
                if "Column" in line and ":" in line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        column_name = parts[1].strip()
                        column_names.append(column_name)
            else:
                # Stop when first non-header line is found
                break

    return column_names, header_line_count

def read_26N(source=None, file_list=None):
    """
    Load datasets from either an online source or a local directory.

    Parameters:
    source (str): The URL to the directory containing the NetCDF files or the path to the local directory.

    Returns:
    A list of xarray.Dataset objects loaded from the filtered NetCDF files.
    """
    if source is None:
        source = 'https://rapid.ac.uk/sites/default/files/rapid_data/'
        file_list = ['moc_vertical.nc', 'ts_gridded.nc', 'moc_transports.nc']
    elif source.startswith("http://") or source.startswith("https://"):
        if file_list is None:
            file_list = list_files_in_https_server(source)
    elif os.path.isdir(source):
        if file_list is None:
            file_list = os.listdir(source)
    else:
        raise ValueError("Source must be a valid URL or directory path.")

    datasets = []

    for file in file_list:
        if source.startswith("http://") or source.startswith("https://"):
            file_url = f"{source}/{file}"
            dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            file_path = download_file(file_url, dest_folder)
            ds = xr.open_dataset(file_path)
            
        else:
            ds = xr.open_dataset(os.path.join(source, file))
        # Add attributes
        ds.attrs["source_file"] = file
        ds.attrs["source_path"] = source
        ds.attrs["description"] = "RAPID transport estimates"
        ds.attrs["note"] = "Dataset accessed and processed via xarray"
        datasets.append(ds)

    return datasets

def read_16N(source="https://mooring.ucsd.edu/move/nc/", file_list="OS_MOVE_TRANSPORTS.nc") -> xr.Dataset:
    """
    Load the MOVE transport dataset from a URL or local file path into an xarray.Dataset.
    
    Parameters:
        source (str): URL or local path to the .nc file. Defaults to the UCSD MOVE dataset URL.
    
    Returns:
        xr.Dataset: The loaded xarray dataset with added attributes.
    
    Raises:
        ValueError: If the source is neither a valid URL nor a local file.
    """
    # Determine source type
    if source is None:
        source = 'https://mooring.ucsd.edu/move/nc/'
        file_list = ['OS_MOVE_TRANSPORTS.nc']
    elif utilities._is_valid_url(source):
        if file_list is None:
            file_list = list_files_in_https_server(source)
    elif utilities._is_valid_file(source):
        if file_list is None:
            file_list = os.listdir(source)
    else:
        raise ValueError("Source must be a valid URL or directory path.")
    
    datasets = []

    if isinstance(file_list, str):
        file_list = [file_list]

    for file in file_list:
        print(file)
        if not file.endswith(".nc"):
            continue
        print(file)
        if source.startswith("http://") or source.startswith("https://"):
            file_url = f"{source}/{file}"
            print(file_url)
            dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            file_path = download_file(file_url, dest_folder)
            ds = xr.open_dataset(file_path)
        else:
            ds = xr.open_dataset(os.path.join(source, file))
            

        # Add attributes
        ds.attrs["source_file"] = file
        ds.attrs["source_path"] = source
        ds.attrs["description"] = "MOVE transport estimates dataset from UCSD mooring project"
        ds.attrs["note"] = "Dataset accessed and processed via xarray"
    
        datasets.append(ds)

    return ds    

def read_osnap(source=None, file_list=['OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc']) -> xr.Dataset:
    """
    Load the OSNAP transport dataset from a URL or local file path into an xarray.Dataset.

    Parameters:
        source (str): URL or local path to the .nc file.
        file_list (str or list of str): Filename or list of filenames to process.

    Returns:
        xr.Dataset: The loaded xarray dataset with added attributes.

    Raises:
        ValueError: If the source is neither a valid URL nor a local file.
    """
    # Match the file with the filename
    fileloc = {
        'OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc':'https://repository.gatech.edu/bitstreams/e039e311-dd2e-4511-a525-c2fcfb3be85a/download',
        'OSNAP_Streamfunction_201408_202006_2023.nc': 'https://repository.gatech.edu/bitstreams/5edf4cba-a28f-40a6-a4da-24d7436a42ab/download',
        'OSNAP_Gridded_TSV_201408_202006_2023.nc': 'https://repository.gatech.edu/bitstreams/598f200a-50ba-4af0-96af-bd29fe692cdc/download'
        }

    # Ensure file_list is a list
    if isinstance(file_list, str):
        file_list = [file_list]

    datasets = []

    for file in file_list:
        if not file.endswith(".nc"):
            continue

        if file in fileloc:
            source = fileloc[file]

        if source.startswith("http://") or source.startswith("https://"):
            # Download the file
            file_url = f"{source}"#.rstrip('/')}/{file}"
            dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            file_path = download_file(file_url, dest_folder)
        else:
            # Local file path
            file_path = os.path.join(source, file)

        # Open dataset
        ds = xr.open_dataset(file_path)

        # Add attributes
        ds.attrs["source_file"] = file
        ds.attrs["source_path"] = source
        ds.attrs["description"] = "OSNAP transport estimates dataset"
        ds.attrs["note"] = "Dataset accessed and processed via xarray"

        datasets.append(ds)

    # For now, return the last dataset loaded (to match read_16N behaviour)
    return datasets[-1] if datasets else None

def read_34S(source: str = None,
             file_list: list = ["Upper_Abyssal_Transport_Anomalies.txt", "MOC_TotalAnomaly_and_constituents.asc"],
             data_path="../data/") -> list:
    """
    Load the 34S transport datasets into a list of xarray Datasets.

    Parameters:
        source (str): URL or local path to the first dataset.
        file_list (str): Filename or list of filenames for the first dataset.

    Returns:
        list: List containing two xarray Datasets:
            [upper_abyssal_transport_anomalies, total_moc_anomalies]

    Raises:
        ValueError: If the source is neither a valid URL nor a local file.
    """
    # Match the file with the filename
    fileloc = {
    'Upper_Abyssal_Transport_Anomalies.txt': 'ftp://ftp.aoml.noaa.gov/phod/pub/SAM/2020_Kersale_etal_ScienceAdvances/',
    'MOC_TotalAnomaly_and_constituents.asc': 'https://www.aoml.noaa.gov/phod/SAMOC_international/documents/'
    }
    datasets = []

    # Ensure file_list is a list
    if isinstance(file_list, str):
        file_list = [file_list]

    for file in file_list:
        if not (file.endswith(".txt") or file.endswith(".asc")):
            continue

        if file in fileloc:
            source = fileloc[file]
        if file=="Upper_Abyssal_Transport_Anomalies.txt":
            ds = read_34S_Kersale2020(source, file_list, data_path)
            datasets.append(ds)
        elif file=="MOC_TotalAnomaly_and_constituents.asc":
            ds = read_34S_Meinen2018(source, file, data_path)
            datasets.append(ds)
    return datasets

def read_34S_Kersale2020(source="ftp://ftp.aoml.noaa.gov/phod/pub/SAM/2020_Kersale_etal_ScienceAdvances/", 
                         file_list: str = "Upper_Abyssal_Transport_Anomalies.txt", 
                         data_path="../data/") -> list:
    """
    Load the 34S transport datasets into a list of xarray Datasets.

    Parameters:
        source (str): URL or local path to the first dataset.
        file_list (str): Filename or list of filenames for the first dataset.

    Returns:
        list: List containing two xarray Datasets:
            [upper_abyssal_transport_anomalies, total_moc_anomalies]

    Raises:
        ValueError: If the source is neither a valid URL nor a local file.
    """
    # === First dataset: Upper Abyssal Transport Anomalies ===

    if utilities._is_valid_url(source):
        if not file_list:
            raise ValueError("file_list must be specified when reading from URL.")
    elif utilities._is_valid_file(source) or Path(source).is_dir():
        if not file_list:
            file_list = os.listdir(source)
    else:
        raise ValueError("Source must be a valid URL or directory path.")

    for file in file_list:
        if not file.endswith(".txt"):
            continue

        if source.startswith(("http://", "https://", "ftp://")):
            file_url = f"{source.rstrip('/')}/{file}"
            if data_path:
                dest_folder = os.path.join(data_path)
            else:
                dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
            file_path = download_file(file_url, dest_folder)
        else:
            file_path = os.path.join(source, file)

        col_names, _ = parse_ascii_header(file_path, '%')
        df = read_ascii_file(file_path, '%')
        df.columns = col_names
        df["TIME"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour", "Minute"]])
        df = df.drop(columns=["Year", "Month", "Day", "Hour", "Minute"])
        ds = df.set_index("TIME").to_xarray()
        newname = 'UPPER_TRANSPORT'
        ds = ds.rename({"Upper-cell volume transport anomaly (relative to record-length average of 17.3 Sv)": newname}) 
        ds[newname].attrs["description"] = "Upper-cell volume transport anomaly (relative to record-length average of 17.3 Sv)"
        ds[newname].attrs["units"] = "Sv"
        ds[newname].attrs["long_name"] = "Upper-cell volume transport anomaly"
        ds[newname].attrs["standard_name"] = "Transport Anomaly"
        newname = 'ABYSSAL_TRANSPORT'
        ds = ds.rename({"Abyssal-cell volume transport anomaly (relative to record-length average of 7.8 Sv)": newname})
        ds[newname].attrs["description"] = "Abyssal-cell volume transport anomaly (relative to record-length average of 7.8 Sv)"
        ds[newname].attrs["units"] = "Sv"
        ds[newname].attrs["long_name"] = "Abyssal-cell volume transport anomaly"
        ds[newname].attrs["standard_name"] = "Transport Anomaly"

        ds.attrs["source_file"] = file
        ds.attrs["source_path"] = source
        ds.attrs["description"] = "34S Upper Abyssal Transport Anomalies dataset"
        ds.attrs["note"] = "Dataset accessed and processed via pandas and xarray"

    return ds

def read_34S_Meinen2018(source, fname="MOC_TotalAnomaly_and_constituents.asc", dest_folder="../data"):
    """
    Reads and processes the 34S Total MOC Anomaly and Constituents dataset 
    from the given URL, returning it as an xarray Dataset.
    Parameters:
    -----------
    moc_url : str
        The URL to the ASCII file containing the MOC dataset.
    dest_folder : str, optional
        The destination folder where the file will be downloaded. If not 
        provided, the default folder will be used.
    Returns:
    --------
    xarray.Dataset
        An xarray Dataset containing the processed MOC data with renamed 
        variables and attributes. The dataset includes the following variables:
        - MOC: Total MOC anomaly (relative to record-length average of 17.3 Sv)
        - RELATIVE_MOC: Relative (density gradient) contribution to the MOC anomaly
        - BAROTROPIC_MOC: Reference (bottom pressure gradient) contribution to the MOC anomaly
        - EKMAN: Ekman (wind) contribution to the MOC anomaly
        - WESTERN_DENSITY: Western density contribution to the MOC anomaly
        - EASTERN_DENSITY: Eastern density contribution to the MOC anomaly
        - WESTERN_BOT_PRESSURE: Western bottom pressure contribution to the MOC anomaly
        - EASTERN_BOT_PRESSURE: Eastern bottom pressure contribution to the MOC anomaly
    Dataset Attributes:
    -------------------
    - source_file: Name of the source file.
    - source_path: URL of the source file.
    - description: Description of the dataset.
    - note: Notes about the dataset processing.
    Notes:
    ------
    - The dataset is accessed and processed using pandas and xarray.
    - The time information is parsed and converted to a datetime index.
    - Units for all variables are in Sverdrups (Sv).
    """

    #dest_folder = os.path.join(os.path.expanduser("~"), ".amocarray_data")
    file_url = f"{source.rstrip('/')}/{fname}"
    moc_file_path = download_file(file_url, dest_folder)
    col_names, _ = parse_ascii_header(moc_file_path, '%')
    moc_df = read_ascii_file(moc_file_path, '%')
    moc_df.columns = col_names
    moc_df["TIME"] = pd.to_datetime(moc_df[["Year", "Month", "Day", "Hour"]])
    moc_df = moc_df.drop(columns=["Year", "Month", "Day", "Hour"])
    moc_ds = moc_df.set_index("TIME").to_xarray()
    newname = 'MOC'
    moc_ds = moc_ds.rename({"Total MOC anomaly (relative to record-length average of 14.7 Sv)": newname})
    moc_ds[newname].attrs["description"] = "MOC Total Anomaly (relative to record-length average of 17.3 Sv)"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "MOC Total Anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"
    newname = 'RELATIVE_MOC'
    moc_ds = moc_ds.rename({"Relative (density gradient) contribution to the MOC anomaly": newname})
    moc_ds[newname].attrs["description"] = "Relative (density gradient) contribution to the MOC anomaly"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "Relative (density gradient) contribution to the MOC anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"
    newname = 'BAROTROPIC_MOC'
    moc_ds = moc_ds.rename({"Reference (bottom pressure gradient) contribution to the MOC anomaly": newname})
    moc_ds[newname].attrs["description"] = "Reference (bottom pressure gradient) contribution to the MOC anomaly"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "Reference (bottom pressure gradient) contribution to the MOC anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"
    newname = 'EKMAN'
    moc_ds = moc_ds.rename({"Ekman (wind) contribution to the MOC anomaly": newname})

    moc_ds[newname].attrs["description"] = "Ekman (wind) contribution to the MOC anomaly"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "Ekman (wind) contribution to the MOC anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"
    newname = 'WESTERN_DENSITY'
    moc_ds = moc_ds.rename({"Western density contribution to the MOC anomaly": newname})
    moc_ds[newname].attrs["description"] = "Western density contribution to the MOC anomaly"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "Western density contribution to the MOC anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"
    newname = 'EASTERN_DENSITY'
    moc_ds = moc_ds.rename({"Eastern density contribution to the MOC anomaly": newname})
    moc_ds[newname].attrs["description"] = "Eastern density contribution to the MOC anomaly"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "Eastern density contribution to the MOC anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"
    newname = 'WESTERN_BOT_PRESSURE'
    moc_ds = moc_ds.rename({"Western bottom pressure contribution to the MOC anomaly": newname})
    moc_ds[newname].attrs["description"] = "Western bottom pressure contribution to the MOC anomaly"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "Western bottom pressure contribution to the MOC anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"
    newname = 'EASTERN_BOT_PRESSURE'
    moc_ds = moc_ds.rename({"Eastern bottom pressure contribution to the MOC anomaly": newname})
    moc_ds[newname].attrs["description"] = "Eastern bottom pressure contribution to the MOC anomaly"
    moc_ds[newname].attrs["units"] = "Sv"
    moc_ds[newname].attrs["long_name"] = "Eastern bottom pressure contribution to the MOC anomaly"
    moc_ds[newname].attrs["standard_name"] = "Transport Anomaly"

    moc_ds.attrs["source_file"] = fname
    moc_ds.attrs["source_path"] = source
    moc_ds.attrs["description"] = "34S Total MOC Anomaly and Constituents dataset"
    moc_ds.attrs["note"] = "Dataset accessed and processed via pandas and xarray"

    return moc_ds


def list_files_in_https_server(url):
    """
    List files in an HTTPS server directory using BeautifulSoup and requests.

    Parameters:
    url (str): The URL to the directory containing the files.

    Returns:
    list: A list of filenames found in the directory.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    soup = BeautifulSoup(response.text, "html.parser")
    files = []

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(".nc"):
            files.append(href)

    return files
