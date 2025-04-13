import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from pandas import DataFrame
from pandas.io.formats.style import Styler


# ------------------------------------------------------------------------------------
# Views of the ds or nc file
# ------------------------------------------------------------------------------------
def show_contents(
    data: str | xr.Dataset, content_type: str = "variables"
) -> Styler | pd.DataFrame:
    """
    Wrapper function to show contents of an xarray Dataset or a netCDF file.

    Parameters
    ----------
    data : str or xr.Dataset
        The input data, either a file path to a netCDF file or an xarray Dataset.
    content_type : str, optional
        The type of content to show, either 'variables' (or 'vars') or 'attributes' (or 'attrs').
        Default is 'variables'.

    Returns
    -------
    pandas.io.formats.style.Styler or pandas.DataFrame
        A styled DataFrame with details about the variables or attributes.

    Raises
    ------
    TypeError
        If the input data is not a file path (str) or an xarray Dataset.
    ValueError
        If the content_type is not 'variables' (or 'vars') or 'attributes' (or 'attrs').
    """
    if content_type in ["variables", "vars"]:
        if isinstance(data, (str, xr.Dataset)):
            return show_variables(data)
        else:
            raise TypeError("Input data must be a file path (str) or an xarray Dataset")
    elif content_type in ["attributes", "attrs"]:
        if isinstance(data, (str, xr.Dataset)):
            return show_attributes(data)
        else:
            raise TypeError(
                "Attributes can only be shown for netCDF files (str) or xarray Datasets"
            )
    else:
        raise ValueError(
            "content_type must be either 'variables' (or 'vars') or 'attributes' (or 'attrs')"
        )


def show_variables(data: str | xr.Dataset) -> Styler:
    """
    Processes an xarray Dataset or a netCDF file, extracts variable information,
    and returns a styled DataFrame with details about the variables.

    Parameters
    ----------
    data : str or xr.Dataset
        The input data, either a file path to a netCDF file or an xarray Dataset.

    Returns
    -------
    pd.io.formats.style.Styler
        A styled DataFrame containing the following columns:
        - dims: The dimension of the variable (or "string" if it is a string type).
        - name: The name of the variable.
        - units: The units of the variable (if available).
        - comment: Any additional comments about the variable (if available).
        - standard_name: The standard name of the variable (if available).
        - dtype: The data type of the variable.

    Raises
    ------
    TypeError
        If the input data is not a file path (str) or an xarray Dataset.
    """
    from netCDF4 import Dataset
    from pandas import DataFrame

    if isinstance(data, str):
        print(f"information is based on file: {data}")
        dataset = Dataset(data)
        variables = dataset.variables
    elif isinstance(data, xr.Dataset):
        print("information is based on xarray Dataset")
        variables = data.variables
    else:
        raise TypeError("Input data must be a file path (str) or an xarray Dataset")

    info = {}
    for i, key in enumerate(variables):
        var = variables[key]
        if isinstance(data, str):
            dims = var.dimensions[0] if len(var.dimensions) == 1 else "string"
            units = "" if not hasattr(var, "units") else var.units
            comment = "" if not hasattr(var, "comment") else var.comment
        else:
            dims = var.dims[0] if len(var.dims) == 1 else "string"
            units = var.attrs.get("units", "")
            comment = var.attrs.get("comment", "")

        info[i] = {
            "name": key,
            "dims": dims,
            "units": units,
            "comment": comment,
            "standard_name": var.attrs.get("standard_name", ""),
            "dtype": str(var.dtype) if isinstance(data, str) else str(var.data.dtype),
        }

    vars = DataFrame(info).T

    dim = vars.dims
    dim[dim.str.startswith("str")] = "string"
    vars["dims"] = dim

    vars = (
        vars.sort_values(["dims", "name"])
        .reset_index(drop=True)
        .loc[:, ["dims", "name", "units", "comment", "standard_name", "dtype"]]
        .set_index("name")
        .style
    )

    return vars


def show_attributes(data: str | xr.Dataset) -> pd.DataFrame:
    """
    Processes an xarray Dataset or a netCDF file, extracts attribute information,
    and returns a DataFrame with details about the attributes.

    Parameters
    ----------
    data : str or xr.Dataset
        The input data, either a file path to a netCDF file or an xarray Dataset.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the following columns:
        - Attribute: The name of the attribute.
        - Value: The value of the attribute.
        - DType: The data type of the attribute.

    Raises
    ------
    TypeError
        If the input data is not a file path (str) or an xarray Dataset.
    """
    from netCDF4 import Dataset
    from pandas import DataFrame

    if isinstance(data, str):
        print(f"information is based on file: {data}")
        rootgrp = Dataset(data, "r", format="NETCDF4")
        attributes = rootgrp.ncattrs()
        get_attr = lambda key: getattr(rootgrp, key)
    elif isinstance(data, xr.Dataset):
        print("information is based on xarray Dataset")
        attributes = data.attrs.keys()
        get_attr = lambda key: data.attrs[key]
    else:
        raise TypeError("Input data must be a file path (str) or an xarray Dataset")

    info = {}
    for i, key in enumerate(attributes):
        dtype = type(get_attr(key)).__name__
        info[i] = {"Attribute": key, "Value": get_attr(key), "DType": dtype}

    attrs = DataFrame(info).T

    return attrs


def show_variables_by_dimension(
    data: str | xr.Dataset, dimension_name: str = "trajectory"
) -> Styler:
    """
    Extracts variable information from an xarray Dataset or a netCDF file and returns a styled DataFrame
    with details about the variables filtered by a specific dimension.

    Parameters
    ----------
    data : str or xr.Dataset
        The input data, either a file path to a netCDF file or an xarray Dataset.
    dimension_name : str, optional
        The name of the dimension to filter variables by, by default "trajectory".

    Returns
    -------
    pandas.io.formats.style.Styler
        A styled DataFrame containing the following columns:
        - dims: The dimension of the variable (or "string" if it is a string type).
        - name: The name of the variable.
        - units: The units of the variable (if available).
        - comment: Any additional comments about the variable (if available).

    Raises
    ------
    TypeError
        If the input data is not a file path (str) or an xarray Dataset.
    """
    if isinstance(data, str):
        print(f"information is based on file: {data}")
        dataset = xr.open_dataset(data)
        variables = dataset.variables
    elif isinstance(data, xr.Dataset):
        print("information is based on xarray Dataset")
        variables = data.variables
    else:
        raise TypeError("Input data must be a file path (str) or an xarray Dataset")

    info = {}
    for i, key in enumerate(variables):
        var = variables[key]
        if isinstance(data, str):
            dims = var.dimensions[0] if len(var.dimensions) == 1 else "string"
            units = "" if not hasattr(var, "units") else var.units
            comment = "" if not hasattr(var, "comment") else var.comment
        else:
            dims = var.dims[0] if len(var.dims) == 1 else "string"
            units = var.attrs.get("units", "")
            comment = var.attrs.get("comment", "")

        if dims == dimension_name:
            info[i] = {
                "name": key,
                "dims": dims,
                "units": units,
                "comment": comment,
            }

    vars = DataFrame(info).T

    dim = vars.dims
    dim[dim.str.startswith("str")] = "string"
    vars["dims"] = dim

    vars = (
        vars.sort_values(["dims", "name"])
        .reset_index(drop=True)
        .loc[:, ["dims", "name", "units", "comment"]]
        .set_index("name")
        .style
    )

    return vars


def plot_monthly_anomalies(
    osnap_data: xr.DataArray,
    rapid_data: xr.DataArray,
    move_data: xr.DataArray,
    samba_data: xr.DataArray,
    osnap_label: str,
    rapid_label: str,
    move_label: str,
    samba_label: str,
) -> tuple[plt.Figure, list[plt.Axes]]:
    """
    Plot the monthly anomalies for OSNAP, RAPID, MOVE, and SAMBA on 4 axes (top to bottom).

    Parameters
    ----------
    osnap_data : xarray.DataArray
        Monthly anomalies for OSNAP.
    rapid_data : xarray.DataArray
        Monthly anomalies for RAPID.
    move_data : xarray.DataArray
        Monthly anomalies for MOVE.
    samba_data : xarray.DataArray
        Monthly anomalies for SAMBA.
    osnap_label : str
        Label for OSNAP plot.
    rapid_label : str
        Label for RAPID plot.
    move_label : str
        Label for MOVE plot.
    samba_label : str
        Label for SAMBA plot.

    Returns
    -------
    tuple[matplotlib.figure.Figure, list[matplotlib.axes._axes.Axes]]
        The figure and axes objects of the generated plot.
    """
    # Resample each input dataset to monthly averages
    osnap_data = osnap_data.resample(TIME="ME").mean()
    rapid_data = rapid_data.resample(TIME="ME").mean()
    move_data = move_data.resample(TIME="ME").mean()
    samba_data = samba_data.resample(TIME="ME").mean()
    fig, axes = plt.subplots(4, 1, figsize=(6, 8), sharex=True)

    # OSNAP
    axes[0].plot(osnap_data["TIME"], osnap_data, color="blue", label=osnap_label)
    axes[0].axhline(0, color="black", linestyle="--", linewidth=0.5)
    axes[0].set_title(osnap_label)
    axes[0].set_ylabel("Transport [Sv]")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # RAPID
    axes[1].plot(rapid_data["TIME"], rapid_data, color="red", label=rapid_label)
    axes[1].axhline(0, color="black", linestyle="--", linewidth=0.5)
    axes[1].set_title(rapid_label)
    axes[1].set_ylabel("Transport [Sv]")
    axes[1].legend()
    axes[1].grid(True, linestyle="--", alpha=0.5)

    # MOVE
    axes[2].plot(move_data["TIME"], move_data, color="green", label=move_label)
    axes[2].axhline(0, color="black", linestyle="--", linewidth=0.5)
    axes[2].set_title(move_label)
    axes[2].set_ylabel("Transport [Sv]")
    axes[2].legend()
    axes[2].grid(True, linestyle="--", alpha=0.5)

    # SAMBA
    axes[3].plot(samba_data["TIME"], samba_data, color="purple", label=samba_label)
    axes[3].axhline(0, color="black", linestyle="--", linewidth=0.5)
    axes[3].set_title(samba_label)
    axes[3].set_xlabel("Time")
    axes[3].set_ylabel("Transport [Sv]")
    axes[3].legend()
    axes[3].grid(True, linestyle="--", alpha=0.5)
    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlim([pd.Timestamp("2000-01-01"), pd.Timestamp("2022-12-31")])
        ax.set_clip_on(False)
        ax.set_yticks(range(int(ax.get_ylim()[0]) + 1, int(ax.get_ylim()[1]) + 1, 5))
    axes[0].set_ylim([5, 25])  # OSNAP
    axes[1].set_ylim([5, 25])  # RAPID
    axes[2].set_ylim([5, 25])  # MOVE
    axes[3].set_ylim([-10, 10])  # SAMBA

    plt.tight_layout()
    return fig, axes
