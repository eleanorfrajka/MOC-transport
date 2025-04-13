"""
Standardisation functions for AMOC observing array datasets.

These functions take raw loaded datasets and:
- Rename variables to standard names
- Add variable-level metadata
- Add or update global attributes
- Prepare datasets for downstream analysis

Currently implemented:
- SAMBA
"""

import xarray as xr

from amocarray import utilities, logger

log = logger.log  # Use the global logger


def standardise_rapid(ds: xr.Dataset) -> xr.Dataset:
    """
    Standardise RAPID dataset:
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
    """
    Standardise SAMBA dataset:
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
    # Variable renaming and attributes
    variable_mapping = {
        "Upper_Abyssal_Transport_Anomalies.txt": {
            "Upper-cell volume transport anomaly (relative to record-length average of 17.3 Sv)": "UPPER_TRANSPORT",
            "Abyssal-cell volume transport anomaly (relative to record-length average of 7.8 Sv)": "ABYSSAL_TRANSPORT",
        },
        "MOC_TotalAnomaly_and_constituents.asc": {
            "Total MOC anomaly (relative to record-length average of 14.7 Sv)": "MOC",
            "Relative (density gradient) contribution to the MOC anomaly": "RELATIVE_MOC",
            "Reference (bottom pressure gradient) contribution to the MOC anomaly": "BAROTROPIC_MOC",
            "Ekman (wind) contribution to the MOC anomaly": "EKMAN",
            "Western density contribution to the MOC anomaly": "WESTERN_DENSITY",
            "Eastern density contribution to the MOC anomaly": "EASTERN_DENSITY",
            "Western bottom pressure contribution to the MOC anomaly": "WESTERN_BOT_PRESSURE",
            "Eastern bottom pressure contribution to the MOC anomaly": "EASTERN_BOT_PRESSURE",
        },
    }

    variable_attrs = {
        "UPPER_TRANSPORT": "Upper-cell volume transport anomaly (relative to record-length average of 17.3 Sv)",
        "ABYSSAL_TRANSPORT": "Abyssal-cell volume transport anomaly (relative to record-length average of 7.8 Sv)",
        "MOC": "MOC Total Anomaly (relative to record-length average of 17.3 Sv)",
        "RELATIVE_MOC": "Relative (density gradient) contribution to the MOC anomaly",
        "BAROTROPIC_MOC": "Reference (bottom pressure gradient) contribution to the MOC anomaly",
        "EKMAN": "Ekman (wind) contribution to the MOC anomaly",
        "WESTERN_DENSITY": "Western density contribution to the MOC anomaly",
        "EASTERN_DENSITY": "Eastern density contribution to the MOC anomaly",
        "WESTERN_BOT_PRESSURE": "Western bottom pressure contribution to the MOC anomaly",
        "EASTERN_BOT_PRESSURE": "Eastern bottom pressure contribution to the MOC anomaly",
    }

    units = "Sv"

    # Rename variables if mapping exists
    if file_name in variable_mapping:
        rename_dict = variable_mapping[file_name]
        ds = ds.rename(rename_dict)

        # Attach attributes to variables
        for var in rename_dict.values():
            if var in ds.variables:
                ds[var].attrs.update(
                    {
                        "description": variable_attrs.get(var, ""),
                        "units": units,
                        "long_name": variable_attrs.get(var, ""),
                        "standard_name": "Transport Anomaly",
                    }
                )

    # Global attributes clean-up
    global_attrs = {
        "summary": "South Atlantic Meridional Overturning Circulation (SAMBA) standardised dataset",
        "comment": "Dataset accessed and processed via http://github.com/AMOCcommunity/amocarray",
        "weblink": "https://www.aoml.noaa.gov/phod/samoc",
        "acknowledgement": "SAMBA data were collected and made freely available by the SAMOC international project and contributing national programs.",
    }

    # Safe update of attributes
    utilities.safe_update_attrs(ds, global_attrs, overwrite=False)

    return ds
