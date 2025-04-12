# Based on https://github.com/voto-ocean-knowledge/votoutils/blob/main/votoutils/utilities/utilities.py
import os
import re
import numpy as np
import pandas as pd
import logging
import datetime
import xarray as xr
import requests
from urllib.parse import urlparse
from pathlib import Path
from ftplib import FTP
from bs4 import BeautifulSoup
import warnings

from functools import wraps

def apply_defaults(default_source, default_files):
    """
    Decorator to apply default values for 'source' and 'file_list' parameters if they are None.

    Parameters
    ----------
    default_source : str
        Default source URL or path.
    default_files : list of str
        Default list of filenames.

    Returns
    -------
    function
        Wrapped function with defaults applied.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(source=None, file_list=None, *args, **kwargs):
            if source is None:
                source = default_source
            if file_list is None:
                file_list = default_files
            return func(source=source, file_list=file_list, *args, **kwargs)
        return wrapper
    return decorator

def safe_update_attrs(ds, new_attrs, overwrite=False, verbose=True):
    """
    Safely update attributes of an xarray Dataset without clobbering existing keys,
    unless explicitly allowed.

    Parameters
    ----------
    ds : xr.Dataset
        The xarray Dataset whose attributes will be updated.
    new_attrs : dict
        Dictionary of new attributes to add.
    overwrite : bool, optional
        If True, allow overwriting existing attributes. Defaults to False.
    verbose : bool, optional
        If True, emit a warning when skipping existing attributes. Defaults to True.

    Returns
    -------
    xr.Dataset
        The dataset with updated attributes.
    """
    for key, value in new_attrs.items():
        if key in ds.attrs:
            if not overwrite:
                if verbose:
                    warnings.warn(
                        f"Attribute '{key}' already exists in dataset attrs and will not be overwritten.",
                        UserWarning
                    )
                continue  # Skip assignment
        ds.attrs[key] = value

    return ds

def _validate_dims(ds):
    dim_name = list(ds.dims)[0]  # Should be 'N_MEASUREMENTS' for OG1
    if dim_name not in ['TIME', 'time']:
        raise ValueError(f"Dimension name '{dim_name}' is not 'TIME' or 'time'.")
    
def _is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([
            result.scheme in ("http", "https", "ftp"),
            result.netloc,
            result.path  # <- just check there's a path, not how it ends
        ])
    except Exception:
        return False

def _is_valid_file(path: str) -> bool:
    return Path(path).is_file() and path.endswith(".nc")

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

