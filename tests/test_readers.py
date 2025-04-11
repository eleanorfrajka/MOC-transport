import pytest
import xarray as xr
from pathlib import Path
from urllib.parse import urlparse
import pathlib
import sys
import pytest
import xarray as xr
from pathlib import Path
from urllib.parse import urlparse
script_dir = pathlib.Path(__file__).parent.absolute()
parent_dir = script_dir.parents[0]
sys.path.append(str(parent_dir))

from amocarray import readers, utilities

# Sample data
VALID_URL = "https://mooring.ucsd.edu/move/nc/"
VALID_FILENAME = "OS_MOVE_TRANSPORTS.nc"
INVALID_STRING = "not_a_valid_source"

# Replace with actual path to a local .nc file if you have one for local testing
LOCAL_VALID_FILE = "/path/to/your/OS_MOVE_TRANSPORTS.nc"

def test_read_16n_url():
    ds = readers.read_16N(source=VALID_URL, file_list=VALID_FILENAME)
    assert isinstance(ds, xr.Dataset)
    assert "source_file" in ds.attrs
    assert ds.attrs["source_file"] == VALID_FILENAME
    assert ds.attrs["source_path"] == VALID_URL
    assert ds.attrs["description"] == "MOVE transport estimates dataset from UCSD mooring project"

@pytest.mark.skipif(not Path(LOCAL_VALID_FILE).is_file(), reason="Local test file not found")
def test_read_16n_local():
    source = str(Path(LOCAL_VALID_FILE).parent)
    file_list = Path(LOCAL_VALID_FILE).name
    ds = readers.read_16N(source=source, file_list=file_list)
    assert isinstance(ds, xr.Dataset)
    assert "source_file" in ds.attrs
    assert ds.attrs["source_file"] == file_list

def test_read_16n_invalid_source():
    with pytest.raises(ValueError, match="Source must be a valid URL or directory path."):
        readers.read_16N(source=INVALID_STRING, file_list=VALID_FILENAME)

def test_validate_dims_valid():
    ds = readers.read_16N(source=VALID_URL, file_list=VALID_FILENAME)
    correct_dim = list(ds.dims)[0]
    ds = ds.rename({correct_dim: "TIME"})
    utilities._validate_dims(ds)  # Should not raise

def test_validate_dims_invalid():
    ds = readers.read_16N(source=VALID_URL, file_list=VALID_FILENAME)
    incorrect_dim = list(ds.dims)[0]
    if incorrect_dim == "TIME":
        ds = ds.rename({"TIME": "WRONG_DIM"})
    with pytest.raises(ValueError, match="Dimension name '.*' is not 'TIME'."):
        utilities._validate_dims(ds)