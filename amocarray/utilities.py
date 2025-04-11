# Based on https://github.com/voto-ocean-knowledge/votoutils/blob/main/votoutils/utilities/utilities.py
import re
import numpy as np
import pandas as pd
import logging
import datetime
import xarray as xr
from urllib.parse import urlparse
from pathlib import Path



def _validate_dims(ds):
    dim_name = list(ds.dims)[0]  # Should be 'N_MEASUREMENTS' for OG1
    if dim_name not in ['TIME', 'time']:
        raise ValueError(f"Dimension name '{dim_name}' is not 'TIME' or 'time'.")
    
# Helper functions
def _is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc, result.path.endswith("/")])
    except Exception:
        return False

def _is_valid_file(path: str) -> bool:
    return Path(path).is_file() and path.endswith(".nc")
