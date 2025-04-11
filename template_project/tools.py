import numpy as np
import pandas as pd
import xarray as xr
import gsw
from datetime import datetime


# Various conversions from the key to units_name with the multiplicative conversion factor
unit_conversion = {
    'cm/s': {'units_name': 'm/s', 'factor': 0.01},
    'cm s-1': {'units_name': 'm s-1', 'factor': 0.01},
    'm/s': {'units_name': 'cm/s', 'factor': 100},
    'm s-1': {'units_name': 'cm s-1', 'factor': 100},
    'S/m': {'units_name': 'mS/cm', 'factor': 0.1},
    'S m-1': {'units_name': 'mS cm-1', 'factor': 0.1},
    'mS/cm': {'units_name': 'S/m', 'factor': 10},
    'mS cm-1': {'units_name': 'S m-1', 'factor': 10},
    'dbar': {'units_name': 'Pa', 'factor': 10000},
    'Pa': {'units_name': 'dbar', 'factor': 0.0001},
    'dbar': {'units_name': 'kPa', 'factor': 10},
    'degrees_Celsius': {'units_name': 'Celsius', 'factor': 1},
    'Celsius': {'units_name': 'degrees_Celsius', 'factor': 1},
    'm': {'units_name': 'cm', 'factor': 100},
    'm': {'units_name': 'km', 'factor': 0.001},
    'cm': {'units_name': 'm', 'factor': 0.01},
    'km': {'units_name': 'm', 'factor': 1000},
    'g m-3': {'units_name': 'kg m-3', 'factor': 0.001},
    'kg m-3': {'units_name': 'g m-3', 'factor': 1000},
}

# Specify the preferred units, and it will convert if the conversion is available in unit_conversion
preferred_units = ['m s-1', 'dbar', 'S m-1']

# String formats for units.  The key is the original, the value is the desired format
unit_str_format = {
    'm/s': 'm s-1',
    'cm/s': 'cm s-1',
    'S/m': 'S m-1',
    'meters': 'm',
    'degrees_Celsius': 'Celsius',
    'g/m^3': 'g m-3',
}


##-----------------------------------------------------------------------------------------------------------
## Calculations for new variables
##-----------------------------------------------------------------------------------------------------------
def calc_Z(ds):
    """
    Calculate the depth (Z position) of the glider using the gsw library to convert pressure to depth.
    
    Parameters
    ----------
    ds (xarray.Dataset): The input dataset containing 'PRES', 'LATITUDE', and 'LONGITUDE' variables.
    
    Returns
    -------
    xarray.Dataset: The dataset with an additional 'DEPTH' variable.
    """
    # Ensure the required variables are present
    if 'PRES' not in ds.variables or 'LATITUDE' not in ds.variables or 'LONGITUDE' not in ds.variables:
        raise ValueError("Dataset must contain 'PRES', 'LATITUDE', and 'LONGITUDE' variables.")

    # Initialize the new variable with the same dimensions as dive_num
    ds['DEPTH_Z'] = (['N_MEASUREMENTS'], np.full(ds.dims['N_MEASUREMENTS'], np.nan))

    # Calculate depth using gsw
    depth = gsw.z_from_p(ds['PRES'], ds['LATITUDE'])
    ds['DEPTH_Z'] = depth

    # Assign the calculated depth to a new variable in the dataset
    ds['DEPTH_Z'].attrs = {
        "units": "meters",
        "positive": "up",
        "standard_name": "depth",
        "comment": "Depth calculated from pressure using gsw library, positive up.",
    }
    
    return ds

def split_by_unique_dims(ds):
    """
    Splits an xarray dataset into multiple datasets based on the unique set of dimensions of the variables.

    Parameters:
    ds (xarray.Dataset): The input xarray dataset containing various variables.

    Returns:
    tuple: A tuple containing xarray datasets, each with variables sharing the same set of dimensions.
    """
    # Dictionary to hold datasets with unique dimension sets
    unique_dims_datasets = {}

    # Iterate over the variables in the dataset
    for var_name, var_data in ds.data_vars.items():
        # Get the dimensions of the variable
        dims = tuple(var_data.dims)
        
        # If this dimension set is not in the dictionary, create a new dataset
        if dims not in unique_dims_datasets:
            unique_dims_datasets[dims] = xr.Dataset()
        
        # Add the variable to the corresponding dataset
        unique_dims_datasets[dims][var_name] = var_data

    # Convert the dictionary values to a dictionary of datasets
    return {dims: dataset for dims, dataset in unique_dims_datasets.items()}



def reformat_units_var(ds, var_name, unit_format=unit_str_format):
    """
    Renames units in the dataset based on the provided dictionary for OG1.

    Parameters
    ----------
    ds (xarray.Dataset): The input dataset containing variables with units to be renamed.
    unit_format (dict): A dictionary mapping old unit strings to new formatted unit strings.

    Returns
    -------
    xarray.Dataset: The dataset with renamed units.
    """
    old_unit = ds[var_name].attrs['units']
    if old_unit in unit_format:
        new_unit = unit_format[old_unit]
    else:
        new_unit = old_unit
    return new_unit

def convert_units_var(var_values, current_unit, new_unit, unit_conversion=unit_conversion):
    """
    Convert the units of variables in an xarray Dataset to preferred units.  This is useful, for instance, to convert cm/s to m/s.

    Parameters
    ----------
    ds (xarray.Dataset): The dataset containing variables to convert.
    preferred_units (list): A list of strings representing the preferred units.
    unit_conversion (dict): A dictionary mapping current units to conversion information.
    Each key is a unit string, and each value is a dictionary with:
        - 'factor': The factor to multiply the variable by to convert it.
        - 'units_name': The new unit name after conversion.

    Returns
    -------
    xarray.Dataset: The dataset with converted units.
    """
    if current_unit in unit_conversion and new_unit in unit_conversion[current_unit]['units_name']:
        conversion_factor = unit_conversion[current_unit]['factor']
        new_values = var_values * conversion_factor
    else:
        new_values = var_values
        print(f"No conversion information found for {current_unit} to {new_unit}")
#        raise ValueError(f"No conversion information found for {current_unit} to {new_unit}")
    return new_values

def convert_qc_flags(dsa, qc_name):
    # Must be called *after* var_name has OG1 long_name
    var_name = qc_name[:-3] 
    if qc_name in list(dsa):
        # Seaglider default type was a string.  Convert to int8.
        dsa[qc_name].values = dsa[qc_name].values.astype("int8")
        # Seaglider default flag_meanings were prefixed with 'QC_'. Remove this prefix.
        if 'flag_meaning' in dsa[qc_name].attrs:
            flag_meaning = dsa[qc_name].attrs['flag_meaning']
            dsa[qc_name].attrs['flag_meaning'] = flag_meaning.replace('QC_', '')
        # Add a long_name attribute to the QC variable
        dsa[qc_name].attrs['long_name'] = dsa[var_name].attrs.get('long_name', '') + ' quality flag'
        dsa[qc_name].attrs['standard_name'] = 'status_flag'
        # Mention the QC variable in the variable attributes
        dsa[var_name].attrs['ancillary_variables'] = qc_name
    return dsa

def find_best_dtype(var_name, da):
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

def set_fill_value(new_dtype):
    fill_val = 2 ** (int(re.findall("\d+", str(new_dtype))[0]) - 1) - 1
    return fill_val

def set_best_dtype(ds):
    bytes_in = ds.nbytes
    for var_name in list(ds):
        da = ds[var_name]
        input_dtype = da.dtype.type
        new_dtype = find_best_dtype(var_name, da)
        for att in ["valid_min", "valid_max"]:
            if att in da.attrs.keys():
                da.attrs[att] = np.array(da.attrs[att]).astype(new_dtype)
        if new_dtype == input_dtype:
            continue
        _log.debug(f"{var_name} input dtype {input_dtype} change to {new_dtype}")
        da_new = da.astype(new_dtype)
        ds = ds.drop_vars(var_name)
        if "int" in str(new_dtype):
            fill_val = set_fill_value(new_dtype)
            da_new[np.isnan(da)] = fill_val
            da_new.encoding["_FillValue"] = fill_val
        ds[var_name] = da_new
    bytes_out = ds.nbytes
    _log.info(
        f"Space saved by dtype downgrade: {int(100 * (bytes_in - bytes_out) / bytes_in)} %",
    )
    return ds


