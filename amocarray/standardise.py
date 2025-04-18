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
from amocarray.logger import log_debug

log = logger.log  # Use the global logger


def clean_metadata(attrs: dict, preferred_keys: dict = None) -> dict:
    """
    Clean up a metadata dictionary:
    - Normalize key casing
    - Merge aliases with identical values
    - Apply standard naming (via preferred_keys mapping)
    """
    if preferred_keys is None:
        preferred_keys = {
            "title": "summary",
            "web_link": "weblink",
            "note": "comment",
            "acknowledgement": "acknowledgement",
            "Acknowledgement": "acknowledgement",
            "doi": "doi",
            "DOI": "doi",
            "references": "references",
            "Reference": "references",
            "creator_name": "creator_name",
            "Creator": "creator_name",
            "creator_email": "creator_email",
            "creator_url": "creator_url",
            "institution": "institution",
            "Institution": "institution",
            "project": "project",
            "Project": "project",
            "Created_by": "creator_name",
            "Creation_date": "date_created",
        }

    # Step 1: merge any identical aliases first
    merged_attrs = merge_metadata_aliases(attrs, preferred_keys)

    # Step 2: normalize remaining cases and resolve conflicts
    cleaned = {}
    for key, value in merged_attrs.items():
        key_lower = key.lower()
        canonical_key = preferred_keys.get(
            key, preferred_keys.get(key_lower, key_lower)
        )

        if canonical_key in cleaned:
            if cleaned[canonical_key] == value:
                log_debug(
                    f"Skipped duplicate (identical) metadata key: '{key}' → '{canonical_key}'"
                )
                continue
            elif len(str(value)) > len(str(cleaned[canonical_key])):
                log_debug(
                    f"Replaced metadata key: '{canonical_key}' with longer value from '{key}' "
                    f"({len(str(cleaned[canonical_key]))} → {len(str(value))} chars)"
                )
                cleaned[canonical_key] = value
            else:
                log_debug(
                    f"Kept existing metadata key: '{canonical_key}', ignored value from '{key}' (shorter or less detailed)"
                )
        else:
            if canonical_key != key:
                log_debug(f"Renamed metadata key: '{key}' → '{canonical_key}'")
            cleaned[canonical_key] = value

    return cleaned


def merge_metadata_aliases(attrs: dict, preferred_keys: dict) -> dict:
    """
    Consolidate metadata keys that map to the same canonical form and share identical values.

    Parameters
    ----------
    attrs : dict
        Metadata dictionary with potential duplicates.
    preferred_keys : dict
        Mapping of alternate keys to preferred canonical keys.

    Returns
    -------
    dict
        Metadata dictionary with duplicates merged.
    """
    merged = {}
    reverse_map = {}

    for key, value in attrs.items():
        key_lower = key.lower()
        canonical_key = preferred_keys.get(
            key, preferred_keys.get(key_lower, key_lower)
        )

        if canonical_key in merged:
            if merged[canonical_key] == value:
                log_debug(
                    f"Merged duplicate key '{key}' into '{canonical_key}' (identical value)"
                )
            else:
                log_debug(
                    f"Found conflicting values for key '{canonical_key}' from '{key}' — retaining first seen"
                )
            continue
        else:
            merged[canonical_key] = value
            reverse_map[canonical_key] = key

    return merged


def standardise_samba(ds: xr.Dataset, file_name: str) -> xr.Dataset:
    return standardise_array(ds, file_name, array_name="samba")


def standardise_rapid(ds: xr.Dataset, file_name: str) -> xr.Dataset:
    return standardise_array(ds, file_name, array_name="rapid")


def standardise_move(ds: xr.Dataset, file_name: str) -> xr.Dataset:
    return standardise_array(ds, file_name, array_name="move")


def standardise_osnap(ds: xr.Dataset, file_name: str) -> xr.Dataset:
    return standardise_array(ds, file_name, array_name="osnap")


def standardise_array(ds: xr.Dataset, file_name: str, array_name: str) -> xr.Dataset:
    """Standardise a mooring array dataset using YAML-based metadata.

    Parameters
    ----------
    ds : xr.Dataset
        Raw dataset loaded from a reader.
    file_name : str
        Filename (e.g., 'moc_transports.nc') expected to match ds.attrs["source_file"].
    array_name : str
        Name of the mooring array (e.g., 'samba', 'rapid', 'move', 'osnap').

    Returns
    -------
    xr.Dataset
        Standardised dataset with renamed variables and enriched metadata.

    Raises
    ------
    ValueError
        If file_name does not match ds.attrs["source_file"].
    """
    if "source_file" in ds.attrs and ds.attrs["source_file"] != file_name:
        raise ValueError(
            f"Mismatch between file_name='{file_name}' and ds.attrs['source_file']='{ds.attrs['source_file']}'"
        )

    meta = utilities.load_array_metadata(array_name)
    file_meta = meta["files"].get(file_name, {})

    # Rename variables
    rename_dict = file_meta.get("variable_mapping", {})
    ds = ds.rename(rename_dict)

    # Apply per-variable metadata
    var_meta = file_meta.get("variables", {})
    for var_name, attrs in var_meta.items():
        if var_name in ds.variables:
            ds[var_name].attrs.update(attrs)

    # Build global attributes
    global_attrs = dict(meta.get("metadata", {}))
    global_attrs.update(
        {
            "summary": global_attrs.get("description", ""),
            "weblink": global_attrs.get("weblink", ""),
        }
    )
    if "acknowledgement" in file_meta:
        global_attrs["acknowledgement"] = file_meta["acknowledgement"]
    if "data_product" in file_meta:
        global_attrs["data_product"] = file_meta["data_product"]

    cleaned_attrs = clean_metadata(global_attrs)
    return utilities.safe_update_attrs(ds, cleaned_attrs, overwrite=False)
