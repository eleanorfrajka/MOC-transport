import logging
import os
import warnings
from ftplib import FTP
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse
from typing import Callable, Dict, List, Optional, Tuple

import pandas as pd
import requests
import xarray as xr
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def apply_defaults(default_source: str, default_files: List[str]) -> Callable:
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
    Callable
        A wrapped function with defaults applied.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            source: Optional[str] = None,
            file_list: Optional[List[str]] = None,
            *args,
            **kwargs,
        ) -> Callable:
            if source is None:
                source = default_source
            if file_list is None:
                file_list = default_files
            return func(source=source, file_list=file_list, *args, **kwargs)

        return wrapper

    return decorator


def get_local_file(
    source_url: str, data_dir: Optional[Path] = None, redownload: bool = False
) -> Union[Path, str]:
    """
    Check if the file exists locally in `data_dir`. If not, download it.

    Parameters
    ----------
    source_url : str
        Remote URL of the file.
    data_dir : Path or None, optional
        Local directory to save/load the data file. If None, the function returns the source URL.
    redownload : bool, default=False
        If True, force re-download even if the file exists locally.

    Returns
    -------
    Path or str
        Path to the local file if `data_dir` is provided, else the original `source_url`.
    """
    if data_dir is None:
        # No local directory provided; return URL (download will happen elsewhere)
        return source_url

    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    local_file = data_dir / Path(source_url).name

    if local_file.exists() and not redownload:
        logger.info(f"Using local file: {local_file}")
        return local_file

    # Download and save to local_file
    logger.info(f"Downloading file from {source_url} to {local_file}")
    download_file(source_url, str(data_dir))
    return local_file


def safe_update_attrs(
    ds: xr.Dataset,
    new_attrs: Dict[str, str],
    overwrite: bool = False,
    verbose: bool = True,
) -> xr.Dataset:
    """
    Safely update attributes of an xarray Dataset without overwriting existing keys,
    unless explicitly allowed.

    Parameters
    ----------
    ds : xr.Dataset
        The xarray Dataset whose attributes will be updated.
    new_attrs : dict of str
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
                        UserWarning,
                    )
                continue  # Skip assignment
        ds.attrs[key] = value

    return ds


def _validate_dims(ds: xr.Dataset) -> None:
    """
    Validate the dimensions of an xarray Dataset.

    This function checks if the first dimension of the dataset is named 'TIME' or 'time'.
    If not, it raises a ValueError.

    Parameters
    ----------
    ds : xr.Dataset
        The xarray Dataset to validate.

    Raises
    ------
    ValueError
        If the first dimension name is not 'TIME' or 'time'.
    """
    dim_name = list(ds.dims)[0]  # Should be 'N_MEASUREMENTS' for OG1
    if dim_name not in ["TIME", "time"]:
        raise ValueError(f"Dimension name '{dim_name}' is not 'TIME' or 'time'.")


def _is_valid_url(url: str) -> bool:
    """
    Validate if a given string is a valid URL with supported schemes.

    Parameters
    ----------
    url : str
        The URL string to validate.

    Returns
    -------
    bool
        True if the URL is valid and uses a supported scheme ('http', 'https', 'ftp'),
        otherwise False.
    """
    try:
        result = urlparse(url)
        return all(
            [
                result.scheme in ("http", "https", "ftp"),
                result.netloc,
                result.path,  # Ensure there's a path, not necessarily its format
            ]
        )
    except Exception:
        return False


def _is_valid_file(path: str) -> bool:
    """
    Check if the given path is a valid file and has a '.nc' extension.

    Parameters
    ----------
    path : str
        The file path to validate.

    Returns
    -------
    bool
        True if the path is a valid file and ends with '.nc', otherwise False.
    """
    return Path(path).is_file() and path.endswith(".nc")


def download_file(url: str, dest_folder: str) -> str:
    """
    Download a file from HTTP(S) or FTP to the specified destination folder.

    Parameters
    ----------
    url : str
        The URL of the file to download.
    dest_folder : str
        Local folder to save the downloaded file.

    Returns
    -------
    str
        The full path to the downloaded file.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    local_filename = os.path.join(dest_folder, os.path.basename(url))
    parsed_url = urlparse(url)

    if parsed_url.scheme in ("http", "https"):
        # HTTP(S) download
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    elif parsed_url.scheme == "ftp":
        # FTP download
        with FTP(parsed_url.netloc) as ftp:
            ftp.login()  # anonymous login
            with open(local_filename, "wb") as f:
                ftp.retrbinary(f"RETR {parsed_url.path}", f.write)

    else:
        raise ValueError(f"Unsupported URL scheme in {url}")

    return local_filename


def download_ftp_file(url: str, dest_folder: str = "data") -> str:
    """
    Download a file from an FTP URL and save it to the destination folder.

    Parameters
    ----------
    url : str
        The full FTP URL to the file.
    dest_folder : str, optional
        Local folder to save the downloaded file. Defaults to "data".

    Returns
    -------
    str
        Path to the downloaded file.

    Raises
    ------
    ValueError
        If the URL scheme is not 'ftp'.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    if parsed_url.scheme != "ftp":
        raise ValueError(
            f"Unsupported URL scheme: {parsed_url.scheme}. Only 'ftp' is supported."
        )

    ftp_host: str = parsed_url.netloc
    ftp_file_path: str = parsed_url.path

    # Ensure destination folder exists
    os.makedirs(dest_folder, exist_ok=True)

    # Local filename
    local_filename: str = os.path.join(dest_folder, os.path.basename(ftp_file_path))

    logger.info(f"Connecting to FTP host: {ftp_host}")
    with FTP(ftp_host) as ftp:
        ftp.login()  # anonymous guest login
        logger.info(f"Downloading {ftp_file_path} to {local_filename}")
        with open(local_filename, "wb") as f:
            ftp.retrbinary(f"RETR {ftp_file_path}", f.write)

    logger.info(f"Download complete: {local_filename}")
    return local_filename


def parse_ascii_header(
    file_path: str, comment_char: str = "%"
) -> Tuple[List[str], int]:
    """
    Parse the header of an ASCII file to extract column names and the number of header lines.

    Header lines are identified by the given comment character (default: '%').
    Columns are defined in lines like:
    '<comment_char> Column 1: <column_name>'.

    Parameters
    ----------
    file_path : str
        Path to the ASCII file.
    comment_char : str, optional
        Character used to identify header lines. Defaults to '%'.

    Returns
    -------
    tuple of (list of str, int)
        A tuple containing:
        - A list of column names extracted from the header.
        - The number of header lines to skip.
    """
    column_names: List[str] = []
    header_line_count: int = 0

    with open(file_path, "r") as file:
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
                # Stop when the first non-header line is found
                break

    return column_names, header_line_count


def list_files_in_https_server(url: str) -> List[str]:
    """
    List files in an HTTPS server directory using BeautifulSoup and requests.

    Parameters
    ----------
    url : str
        The URL to the directory containing the files.

    Returns
    -------
    List[str]
        A list of filenames found in the directory with '.nc' extension.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    soup = BeautifulSoup(response.text, "html.parser")
    files: List[str] = []

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(".nc"):
            files.append(href)

    return files


def read_ascii_file(file_path: str, comment_char: str = "#") -> pd.DataFrame:
    """
    Read an ASCII file into a pandas DataFrame, skipping lines starting with a specified comment character.

    Parameters
    ----------
    file_path : str
        Path to the ASCII file.
    comment_char : str, optional
        Character denoting comment lines. Defaults to '#'.

    Returns
    -------
    pd.DataFrame
        The loaded data as a pandas DataFrame.
    """
    return pd.read_csv(file_path, sep=r"\s+", comment=comment_char, on_bad_lines="skip")
