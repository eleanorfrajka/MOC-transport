import xarray as xr
import os
from bs4 import BeautifulSoup
import requests

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

def read_26N(source):
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
        file_list = list_files_in_https_server(source)
    elif os.path.isdir(source):
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
        
        datasets.append(ds)

    return datasets

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
