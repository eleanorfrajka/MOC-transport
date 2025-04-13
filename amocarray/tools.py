import re

import numpy as np
import xarray as xr

from amocarray import logger

log = logger.log


def generate_reverse_conversions(
    forward_conversions: dict[str, dict[str, float]]
) -> dict[str, dict[str, float]]:
    """
    Create a unit conversion dictionary with both forward and reverse conversions.

    Parameters
    ----------
    forward_conversions : dict of {str: dict of {str: float}}
        Mapping of source units to target units and conversion factors.
        Example: {"m": {"cm": 100, "km": 0.001}}

    Returns
    -------
    dict of {str: dict of {str: float}}
        Complete mapping of units including reverse conversions.
        Example: {"cm": {"m": 0.01}, "km": {"m": 1000}}

    Notes
    -----
    If a conversion factor is zero, a warning is printed, and the reverse conversion is skipped.
    """
    complete_conversions: dict[str, dict[str, float]] = {}

    for from_unit, targets in forward_conversions.items():
        complete_conversions.setdefault(from_unit, {})
        for to_unit, factor in targets.items():
            complete_conversions[from_unit][to_unit] = factor
            complete_conversions.setdefault(to_unit, {})
            if factor == 0:
                print(
                    f"Warning: zero factor in conversion from {from_unit} to {to_unit}"
                )
                continue
            complete_conversions[to_unit][from_unit] = 1 / factor

    return complete_conversions


# Various conversions from the key to units_name with the multiplicative conversion factor
base_unit_conversion = {
    "cm/s": {"m/s": 0.01},
    "cm s-1": {"m s-1": 0.01},
    "S/m": {"mS/cm": 0.1},
    "dbar": {"Pa": 10000, "kPa": 10},
    "degrees_Celsius": {"Celsius": 1},
    "m": {"cm": 100, "km": 0.001},
    "g m-3": {"kg m-3": 0.001},
    "Sverdrup": {"Sv": 1},
}

unit_conversion = generate_reverse_conversions(base_unit_conversion)

# Specify the preferred units, and it will convert if the conversion is available in unit_conversion
preferred_units = ["m s-1", "dbar", "S m-1", "Sv"]

# String formats for units.  The key is the original, the value is the desired format
unit_str_format = {
    "m/s": "m s-1",
    "cm/s": "cm s-1",
    "S/m": "S m-1",
    "meters": "m",
    "degrees_Celsius": "Celsius",
    "g/m^3": "g m-3",
}


# ------------------------------------------------------------------------------------------------------
# Calculations for new variables
# ------------------------------------------------------------------------------------------------------


def split_by_unique_dims(ds: xr.Dataset) -> dict[tuple[str, ...], xr.Dataset]:
    """
    Splits an xarray dataset into multiple datasets based on the unique set of dimensions of the variables.

    Parameters
    ----------
    ds : xarray.Dataset
        The input xarray dataset containing various variables.

    Returns
    -------
    dict of tuple of str to xarray.Dataset
        A dictionary where keys are tuples of unique dimensions, and values are xarray datasets
        containing variables that share the same set of dimensions.

    Examples
    --------
    >>> import xarray as xr
    >>> data = xr.Dataset({
    ...     'var1': (('x', 'y'), [[1, 2], [3, 4]]),
    ...     'var2': (('x',), [5, 6]),
    ...     'var3': (('y',), [7, 8])
    ... })
    >>> split_datasets = split_by_unique_dims(data)
    >>> for dims, ds in split_datasets.items():
    ...     print(f"Dimensions: {dims}")
    ...     print(ds)
    Dimensions: ('x', 'y')
    <xarray.Dataset>
    Dimensions:  (x: 2, y: 2)
    Dimensions without coordinates: x, y
    Data variables:
        var1     (x, y) int64 1 2 3 4
    Dimensions: ('x',)
    <xarray.Dataset>
    Dimensions:  (x: 2)
    Dimensions without coordinates: x
    Data variables:
        var2     (x) int64 5 6
    Dimensions: ('y',)
    <xarray.Dataset>
    Dimensions:  (y: 2)
    Dimensions without coordinates: y
    Data variables:
        var3     (y) int64 7 8
    """
    unique_dims_datasets: dict[tuple[str, ...], xr.Dataset] = {}

    for var_name, var_data in ds.data_vars.items():
        dims = tuple(var_data.dims)
        if dims not in unique_dims_datasets:
            unique_dims_datasets[dims] = xr.Dataset()
        unique_dims_datasets[dims][var_name] = var_data

    return unique_dims_datasets


def reformat_units_var(
    ds: xr.Dataset, var_name: str, unit_format: dict[str, str] = unit_str_format
) -> str:
    """
    Reformat the units of a variable in the dataset based on a provided mapping.

    Parameters
    ----------
    ds : xarray.Dataset
        The input dataset containing variables with units to be reformatted.
    var_name : str
        The name of the variable whose units need to be reformatted.
    unit_format : dict of {str: str}, optional
        A dictionary mapping old unit strings to new formatted unit strings.
        Defaults to `unit_str_format`.

    Returns
    -------
    str
        The reformatted unit string. If the old unit is not found in `unit_format`,
        the original unit string is returned.
    """
    old_unit = ds[var_name].attrs["units"]
    new_unit = unit_format.get(old_unit, old_unit)
    return new_unit


def convert_units_var(
    var_values: np.ndarray | float,
    current_unit: str,
    new_unit: str,
    unit_conversion: dict[str, dict[str, float]] = unit_conversion,
) -> np.ndarray | float:
    """
    Converts variable values from one unit to another using a predefined conversion factor.

    Parameters
    ----------
    var_values : numpy.ndarray or float
        The values to be converted.
    current_unit : str
        The current unit of the variable values.
    new_unit : str
        The target unit to which the variable values should be converted.
    unit_conversion : dict of {str: dict of {str: float}}, optional
        A dictionary containing conversion factors between units. The default is `unit_conversion`.

    Returns
    -------
    numpy.ndarray or float
        The converted variable values. If no conversion factor is found, the original values are returned.

    Raises
    ------
    KeyError
        If the conversion factor for the specified units is not found in the `unit_conversion` dictionary.

    Notes
    -----
    If the conversion factor for the specified units is not available, a message is printed, and the original
    values are returned without any conversion.
    """
    try:
        conversion_factor = unit_conversion[current_unit][new_unit]
        return var_values * conversion_factor
    except KeyError:
        print(f"No conversion information found for {current_unit} to {new_unit}")
        return var_values


def convert_qc_flags(dsa: xr.Dataset, qc_name: str) -> xr.Dataset:
    """
    Convert and update quality control (QC) flags in a dataset.

    This function processes a QC variable in the given dataset by converting its
    data type, updating its attributes, and linking it to the associated variable.
    It assumes that the QC variable name ends with '_qc' and that the associated
    variable has a `long_name` attribute.

    Parameters
    ----------
    dsa : xarray.Dataset
        The dataset containing the QC variable and the associated variable.
    qc_name : str
        The name of the QC variable to process.

    Returns
    -------
    xarray.Dataset
        The updated dataset with modified QC variable attributes and a link
        between the QC variable and the associated variable.

    Notes
    -----
    - The QC variable's data type is converted to `int8`.
    - The `flag_meaning` attribute of the QC variable is updated to remove the
      'QC_' prefix, if present.
    - A `long_name` attribute is added to the QC variable, describing it as a
      quality flag for the associated variable.
    - The `standard_name` attribute of the QC variable is set to 'status_flag'.
    - The `ancillary_variables` attribute of the associated variable is updated
      to reference the QC variable.

    Examples
    --------
    >>> import xarray as xr
    >>> data = xr.Dataset({
    ...     'temperature': (['time'], [15.0, 16.0, 14.5]),
    ...     'temperature_qc': (['time'], ['1', '2', '1'], {'flag_meaning': 'QC_good QC_bad'})
    ... })
    >>> data['temperature'].attrs['long_name'] = 'Sea temperature'
    >>> updated_data = convert_qc_flags(data, 'temperature_qc')
    >>> updated_data['temperature_qc'].attrs
    {'flag_meaning': 'good bad', 'long_name': 'Sea temperature quality flag', 'standard_name': 'status_flag'}
    >>> updated_data['temperature'].attrs
    {'long_name': 'Sea temperature', 'ancillary_variables': 'temperature_qc'}
    """
    var_name: str = qc_name[:-3]
    if qc_name in list(dsa):
        # Convert QC variable to int8
        dsa[qc_name].values = dsa[qc_name].values.astype("int8")
        # Remove 'QC_' prefix from flag_meaning attribute
        if "flag_meaning" in dsa[qc_name].attrs:
            flag_meaning: str = dsa[qc_name].attrs["flag_meaning"]
            dsa[qc_name].attrs["flag_meaning"] = flag_meaning.replace("QC_", "")
        # Add a long_name attribute to the QC variable
        dsa[qc_name].attrs["long_name"] = (
            dsa[var_name].attrs.get("long_name", "") + " quality flag"
        )
        dsa[qc_name].attrs["standard_name"] = "status_flag"
        # Update ancillary_variables attribute of the associated variable
        dsa[var_name].attrs["ancillary_variables"] = qc_name
    return dsa


def find_best_dtype(var_name: str, da: xr.DataArray) -> np.dtype:
    """
    Determines the most suitable data type for a given variable.

    Parameters
    ----------
    var_name : str
        The name of the variable.
    da : xarray.DataArray
        The data array containing the variable's values.

    Returns
    -------
    numpy.dtype
        The optimal data type for the variable based on its name and values.
    """
    input_dtype = da.dtype.type
    if "latitude" in var_name.lower() or "longitude" in var_name.lower():
        return np.double
    if var_name[-2:].lower() == "qc":
        return np.int8
    if "time" in var_name.lower():
        return input_dtype
    if var_name[-3:] == "raw" or "int" in str(input_dtype):
        if np.nanmax(da.values) < 2**16 / 2:
            return np.int16
        elif np.nanmax(da.values) < 2**32 / 2:
            return np.int32
    if input_dtype == np.float64:
        return np.float32
    return input_dtype


def set_fill_value(new_dtype: np.dtype) -> int:
    """
    Calculate the fill value for a given data type.

    Parameters
    ----------
    new_dtype : numpy.dtype
        The data type for which the fill value is to be calculated.

    Returns
    -------
    int
        The calculated fill value based on the bit-width of the data type.
    """
    fill_val: int = 2 ** (int(re.findall(r"\d+", str(new_dtype))[0]) - 1) - 1
    return fill_val


def set_best_dtype(ds: xr.Dataset) -> xr.Dataset:
    """
    Adjust the data types of variables in a dataset to optimize memory usage.

    Parameters
    ----------
    ds : xarray.Dataset
        The input dataset whose variables' data types will be adjusted.

    Returns
    -------
    xarray.Dataset
        The dataset with updated data types for its variables, potentially saving memory.

    Notes
    -----
    - The function determines the best data type for each variable using `find_best_dtype`.
    - Attributes like `valid_min` and `valid_max` are updated to match the new data type.
    - If the new data type is integer-based, NaN values are replaced with a fill value.
    - Logs the percentage of memory saved after the data type adjustments.
    """
    bytes_in: int = ds.nbytes
    for var_name in list(ds):
        da: xr.DataArray = ds[var_name]
        input_dtype: np.dtype = da.dtype.type
        new_dtype: np.dtype = find_best_dtype(var_name, da)
        for att in ["valid_min", "valid_max"]:
            if att in da.attrs.keys():
                da.attrs[att] = np.array(da.attrs[att]).astype(new_dtype)
        if new_dtype == input_dtype:
            continue
        _log.debug(f"{var_name} input dtype {input_dtype} change to {new_dtype}")
        da_new: xr.DataArray = da.astype(new_dtype)
        ds = ds.drop_vars(var_name)
        if "int" in str(new_dtype):
            fill_val: int = set_fill_value(new_dtype)
            da_new[np.isnan(da)] = fill_val
            da_new.encoding["_FillValue"] = fill_val
        ds[var_name] = da_new
    bytes_out: int = ds.nbytes
    _log.info(
        f"Space saved by dtype downgrade: {int(100 * (bytes_in - bytes_out) / bytes_in)} %",
    )
    return ds
