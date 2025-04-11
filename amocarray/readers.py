import xarray as xr
import os
from bs4 import BeautifulSoup
import requests
from pathlib import Path

from amocarray import utilities
# Dropbox location Public/linked_elsewhere/amocarray_data/
server = "https://www.dropbox.com/scl/fo/4bjo8slq1krn5rkhbkyds/AM-EVfSHi8ro7u2y8WAcKyw?rlkey=16nqlykhgkwfyfeodkj274xpc&dl=0"

def download_file(url, dest_folder):
    """
    Download a file from a URL to a destination folder.

    Parameters:
    url (str): The URL of the file to download.
    dest_folder (str): The folder where the file will be saved.

    Returns:
    str: The path to the downloaded file.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    local_filename = os.path.join(dest_folder, os.path.basename(url))
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

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
