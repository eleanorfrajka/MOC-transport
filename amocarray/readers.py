import xarray as xr
import os
from bs4 import BeautifulSoup
import requests
from importlib_resources import files
import pooch

# Dropbox location Public/linked_elsewhere/amocarray_data/
server = "https://www.dropbox.com/scl/fo/4bjo8slq1krn5rkhbkyds/AM-EVfSHi8ro7u2y8WAcKyw?rlkey=16nqlykhgkwfyfeodkj274xpc&dl=0"

data_source_og = pooch.create(
    path=pooch.os_cache("amocarray"),
    base_url=server,
    registry={'moc_vertical.nc': 'sha256:3d3a40fc45102c4dbe32fcbd03d1ec19724495145d014c6d02a44b8413447d46'},
)

# readers.py: Will only read files.  Not manipulate them.
#
# Comment 2024 Oct 30: I needed an initial file list to create the registry
# This is impractical for expansion, so may need to move away from pooch.
# This was necessary to get an initial file list
# mylist = fetchers.list_files_in_https_server(server)
# fetchers.create_pooch_registry_from_directory("/Users/eddifying/Dropbox/data/sg015-ncei-download/")
# Example usage
#directory_path = "/Users/eddifying/Dropbox/data/sg015-ncei-snippet"
#pooch_registry = create_pooch_registry_from_directory(directory_path)
#print(pooch_registry)

# Information on creating a registry file: https://www.fatiando.org/pooch/latest/registry-files.html
# But instead of pkg_resources (https://setuptools.pypa.io/en/latest/pkg_resources.html#)
# we should use importlib.resources
# Here's how to use importlib.resources (https://importlib-resources.readthedocs.io/en/latest/using.html)
#data_source_og = pooch.create(
#    path=pooch.os_cache("amocarray"),
#    base_url=server,
#    registry=None,
#)
#registry_file = files('amocarray').joinpath('amoc_registry.txt')
#data_source_og.load_registry(registry_file)

def load_sample_dataset(dataset_name="moc_vertical.nc"):
    if dataset_name in data_source_og.registry.keys():
        file_path = data_source_og.fetch(dataset_name)
        return xr.open_dataset(file_path)
    else:
        msg = f"Requested sample dataset {dataset_name} not known. Specify one of the following available datasets: {list(data_source_og.registry.keys())}"
        raise ValueError(msg)


def read_26N(source):
    """
    Load datasets from either an online source or a local directory, optionally filtering by profile range.

    Parameters:
    source (str): The URL to the directory containing the NetCDF files or the path to the local directory.
    start_profile (int, optional): The starting profile number to filter files. Defaults to None.
    end_profile (int, optional): The ending profile number to filter files. Defaults to None.

    Returns:
    A list of xarray.Dataset objects loaded from the filtered NetCDF files.
    """
    if source is None:
        server = 'https://rapid.ac.uk/sites/default/files/rapid_data/'
        filelist = ['moc_vertical.nc', 'ts_gridded.nc', 'moc_transports.nc']
    if source.startswith("http://") or source.startswith("https://"):
        # Create a Pooch object to manage the remote files
        data_source_online = pooch.create(
            path=pooch.os_cache("amocarray"),
            base_url=source,
            registry=None,
        )
        registry_file = files('amocarray').joinpath('amoc_registry.txt')
        data_source_og.load_registry(registry_file)

        # List all files in the URL directory
        file_list = list_files_in_https_server(source)
    elif os.path.isdir(source):
        file_list = os.listdir(source)
    else:
        raise ValueError("Source must be a valid URL or directory path.")

    filtered_files = filter_files_by_profile(file_list, start_profile, end_profile)
    
    datasets = []

    for file in filtered_files:
        if source.startswith("http://") or source.startswith("https://"):
            ds = load_sample_dataset(file)
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

def create_pooch_registry_from_directory(directory):
    """
    Create a Pooch registry from files in a specified directory.

    Parameters:
    directory (str): The path to the directory containing the files.

    Returns:
    dict: A dictionary representing the Pooch registry with filenames as keys and their SHA256 hashes as values.
    """
    registry = {}
    files = os.listdir(directory)

    for file in files:
        if file.endswith(".nc"):
            file_path = os.path.join(directory, file)
            sha256_hash = pooch.file_hash(file_path, alg="sha256")
            registry[file] = f"sha256:{sha256_hash}"

    return registry

