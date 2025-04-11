import pathlib
import sys
import pytest
import xarray as xr
from pathlib import Path
from urllib.parse import urlparse
script_dir = pathlib.Path(__file__).parent.absolute()
parent_dir = script_dir.parents[0]
sys.path.append(str(parent_dir))

from amocarray import utilities


# Sample data
VALID_URL = "https://mooring.ucsd.edu/move/nc/"
INVALID_URL = "ftdp://invalid-url.com/data.nc"
INVALID_STRING = "not_a_valid_source"

# Replace with actual path to a local .nc file if you have one for local testing
LOCAL_VALID_FILE = "/path/to/your/OS_MOVE_TRANSPORTS.nc"
LOCAL_INVALID_FILE = "/path/to/invalid_file.txt"

@pytest.mark.parametrize("url,expected", [
    (VALID_URL, True),
    (INVALID_URL, False),
    ("not_a_url", False),
])
def test_is_valid_url(url, expected):
    assert utilities._is_valid_url(url) == expected

@pytest.mark.parametrize("path,expected", [
    (LOCAL_VALID_FILE, Path(LOCAL_VALID_FILE).is_file() and LOCAL_VALID_FILE.endswith(".nc")),
    (LOCAL_INVALID_FILE, False),
    ("non_existent_file.nc", False),
])
def test_is_valid_file(path, expected):
    assert utilities._is_valid_file(path) == expected

