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
            "Title": "summary",
            "title": "summary",
            "web_link": "weblink",
            "note": "comment",
            "Acknowledgement": "acknowledgement",
            "DOI": "doi",
            "Reference": "references",
            "Creator": "creator_name",
            "contributor": "contributor_name",
            "Institution": "institution",
            "Project": "project",
            "Created_by": "creator_name",
            "Principle_investigator": "principal_investigator",
            "Principle_investigator_email": "principal_investigator_email",
            "Creation_date": "date_created",
        }

    # Step 1: merge any identical aliases first
    merged_attrs = merge_metadata_aliases(attrs, preferred_keys)

    # Step 2: normalize remaining cases and resolve conflicts
    cleaned = {}
    for key, value in merged_attrs.items():
        # key is already canonical if it was an alias
        if key in cleaned:
            if cleaned[key] == value:
                logger.debug(f"Skipping identical '{key}'")
                continue
            if len(str(value)) > len(str(cleaned[key])):
                logger.debug(
                    f"Replacing '{key}' value with longer one ("
                    f"{len(str(cleaned[key]))}→{len(str(value))} chars)"
                )
                cleaned[key] = value
            else:
                logger.debug(f"Keeping existing '{key}', ignoring shorter from merge")
        else:
            cleaned[key] = value

    # Step 3: consolidate contributors and institutions
    cleaned = _consolidate_contributors(cleaned)
    return cleaned

def _consolidate_contributors(cleaned: dict) -> dict:
    """
    Consolidate creators, PIs, publishers, and contributors into unified fields:
    - contributor_name, contributor_role, contributor_email aligned one-to-one
    - contributing_institutions, with placeholders for vocabularies/roles
    """
    # Helper: both log and stdout
    def dbg(msg, *args):
        log_debug(msg, *args)
        try:
            print(msg % args)
        except Exception:
            print(msg, args)

    dbg("Starting _consolidate_contributors with attrs: %s", cleaned)

    role_map = {
        "creator_name":           "creator",
        "creator":           "creator",
        "principal_investigator": "PI",
        "publisher_name":         "publisher",
        "publisher":         "publisher",
        "contributor_name":       "",
        "contributor":       "",
    }

    # Step A: extract all email buckets
    email_buckets = {}
    bucket_order = []
    for key in list(cleaned.keys()):
        if key.endswith("_email"):
            raw = cleaned.pop(key)
            parts = [v.strip() for v in str(raw).replace(";", ",").split(",") if v.strip()]
            email_buckets[key] = parts
            bucket_order.append(key)
    dbg("Email buckets: %s", email_buckets)

    # Step B: extract any name-keys and their roles
    names, roles, sources = [], [], []
    for key in list(cleaned.keys()):
        if key in role_map:
            raw = cleaned.pop(key)
            parts = [v.strip() for v in str(raw).replace(";", ",").split(",") if v.strip()]
            for p in parts:
                names.append(p)
                roles.append(role_map[key])
                sources.append(key)
    dbg("Names: %s, Roles: %s, Sources: %s", names, roles, sources)

    # Step C: build contributors
    if names:
        # C1) names + roles
        cleaned["contributor_name"] = ", ".join(names)
        if "contributor_role" not in cleaned:
            cleaned["contributor_role"] = ", ".join(roles)
        dbg("Set contributor_name=%r, contributor_role=%r",
            cleaned["contributor_name"], cleaned["contributor_role"])

        # C2) align emails to each source
        aligned = []
        buckets = {k: v.copy() for k,v in email_buckets.items()}
        for src in sources:
            base = src[:-5] if src.endswith("_name") else src
            ek = f"{base}_email"
            aligned.append(buckets.get(ek, []).pop(0) if buckets.get(ek) else "")
        cleaned["contributor_email"] = ", ".join(aligned)
        dbg("Aligned contributor_email=%r", cleaned["contributor_email"])

    elif bucket_order:
        # Email-only case: create one placeholder per email
        flat_emails, placeholder_roles = [], []
        for bk in bucket_order:
            print(f"Processing email bucket: {bk[:-6]}")
            role = role_map.get(bk[:-6], "")
            print(f"Role for {bk}: {role}")
            for email in email_buckets[bk]:
                flat_emails.append(email)
                placeholder_roles.append(role)

        cleaned["contributor_name"] = ", ".join([""] * len(flat_emails))
        cleaned["contributor_role"] = ", ".join(placeholder_roles)
        cleaned["contributor_email"] = ", ".join(flat_emails)
        dbg("Placeholder contributor_name=%r", cleaned["contributor_name"])
        dbg("Placeholder contributor_role=%r", cleaned["contributor_role"])
        dbg("Flattened contributor_email=%r", cleaned["contributor_email"])

    # Step D: consolidate institution keys
    insts = []
    for key in list(cleaned.keys()):
        if key.lower() in ("institution", "publisher_institution", "contributor_institution"):
            raw = cleaned.pop(key)
            parts = [v.strip() for v in str(raw).replace(";", ",").split(",") if v.strip()]
            insts.extend(parts)
    if insts:
        cleaned["contributing_institutions"] = ", ".join(dict.fromkeys(insts))
        cleaned.setdefault("contributing_institutions_vocabulary", "")
        cleaned.setdefault("contributing_institutions_role", "")
        cleaned.setdefault("contributing_institutions_role_vocabulary", "")
        dbg("Institutions=%r", cleaned["contributing_institutions"])

    dbg("Finished _consolidate_contributors: %s", cleaned)
    return cleaned


def merge_metadata_aliases(attrs: dict, preferred_keys: dict) -> dict:
    """
    Consolidate metadata keys that map to the same canonical form and share identical values,
    in a case‑insensitive way—except for 'featureType', which remains case‑sensitive.

    Parameters
    ----------
    attrs : dict
        Metadata dictionary with potential duplicates.
    preferred_keys : dict
        Mapping of lowercase alias keys to preferred canonical keys.

    Returns
    -------
    dict
        Metadata dictionary with duplicates merged.
    """
    merged = {}
    for key, value in attrs.items():
        # Preserve 'featureType' exactly
        if key == "featureType":
            canonical = "featureType"
        else:
            # case‑insensitive mapping: lowercase everything
            low = key.lower()
            canonical = preferred_keys.get(low, low)

        if canonical in merged:
            if merged[canonical] == value:
                log_debug(f"Merged duplicate key '{key}' into '{canonical}' (identical value)")
            else:
                log_debug(f"Conflict for '{canonical}' from '{key}'; keeping first value")
            continue

        merged[canonical] = value

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
    # 1) Validate source_file matches
    src = ds.attrs.get("source_file")
    if src and src != file_name:
        raise ValueError(f"file_name {file_name!r} ≠ ds.attrs['source_file'] {src!r}")
    log_debug(f"Standardising {file_name} for {array_name.upper()}")

    # 2) Collect new attrs from YAML
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

    # 3) Merge existing attrs + new global attrs + file-specific
    combined = {}
    combined.update(ds.attrs)  # original reader attrs
    combined.update(meta.get("metadata", {}))  # array‑level
    combined.update(
        {
            "summary": meta["metadata"].get("description", ""),
            "weblink": meta["metadata"].get("weblink", ""),
        }
    )
    combined.update(
        {k: file_meta[k] for k in ("acknowledgement", "data_product") if k in file_meta}
    )

    # 4) Clean up collisions & override ds.attrs wholesale
    cleaned = clean_metadata(combined)
    ds.attrs = cleaned
    #    ds = utilities.safe_update_attrs(ds, cleaned, overwrite=False)
    return ds
