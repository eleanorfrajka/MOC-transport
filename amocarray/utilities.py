# Based on https://github.com/voto-ocean-knowledge/votoutils/blob/main/votoutils/utilities/utilities.py
import re
import numpy as np
import pandas as pd
import logging
import datetime
import xarray as xr



def _validate_dims(ds):
    dim_name = list(ds.dims)[0] # Should be 'N_MEASUREMENTS' for OG1
    if dim_name != 'N_MEASUREMENTS':
        raise ValueError(f"Dimension name '{dim_name}' is not 'N_MEASUREMENTS'.")
    