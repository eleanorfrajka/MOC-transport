"""Standardisation functions for AMOC observing array datasets.

These functions take raw loaded datasets and:
- Rename variables to standard names
- Add variable-level metadata
- Add or update global attributes
- Prepare datasets for downstream analysis

Currently implemented:
- SAMBA
"""

import xarray as xr

from amocarray import logger, utilities

log = logger.log  # Use the global logger


def standardise_rapid(ds: xr.Dataset) -> xr.Dataset:
    """Standardise RAPID dataset:
    - Rename time dimension and variable from 'time' to 'TIME'.

    Parameters
    ----------
    ds : xr.Dataset
        Raw RAPID dataset loaded from read_rapid().

    Returns
    -------
    xr.Dataset
        Standardised RAPID dataset.

    """
    # Rename dimension
    if "time" in ds.sizes:
        ds = ds.rename_dims({"time": "TIME"})

    # Rename variable
    if "time" in ds.variables:
        ds = ds.rename({"time": "TIME"})

    # Swap dimension to ensure 'TIME' is the index coordinate
    if "TIME" in ds.coords:
        ds = ds.swap_dims({"TIME": "TIME"})

    # Optional: global metadata updates (future)
    # utilities.safe_update_attrs(ds, {"weblink": "..."})

    return ds


def standardise_samba(ds: xr.Dataset, file_name: str) -> xr.Dataset:
    """Standardise SAMBA dataset:
    - Rename variables to standard names.
    - Add variable-level metadata (units, description, etc.).
    - Update global attributes.

    Parameters
    ----------
    ds : xr.Dataset
        Raw SAMBA dataset loaded from read_samba().
    file_name : str
        Original source file name, used to determine mapping and metadata.

    Returns
    -------
    xr.Dataset
        Standardised SAMBA dataset.
    """
    meta = utilities.load_array_metadata("samba")
    file_meta = meta["files"].get(file_name, {})

    # Rename variables using the YAML mapping
    rename_dict = file_meta.get("variable_mapping", {})
    ds = ds.rename(rename_dict)

    # Apply per-variable attributes
    var_meta = file_meta.get("variables", {})
    for var_name, attrs in var_meta.items():
        if var_name in ds.variables:
            ds[var_name].attrs.update(attrs)

    # Compose global attributes from array-wide + file-specific
    global_attrs = dict(meta.get("metadata", {}))  # array-wide
    global_attrs.update(
        {
            "summary": meta["metadata"].get("description", ""),
            "weblink": meta["metadata"].get("weblink", ""),
        }
    )
    if "acknowledgement" in file_meta:
        global_attrs["acknowledgement"] = file_meta["acknowledgement"]
    if "data_product" in file_meta:
        global_attrs["data_product"] = file_meta["data_product"]

    # Update global attrs, non-destructively
    ds = utilities.safe_update_attrs(ds, global_attrs, overwrite=False)

    return ds
