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
    

def _parse_calibcomm(calibcomm):
    if 'calibration' in calibcomm.values.item().decode('utf-8'):

        cal_date = calibcomm.values.item().decode('utf-8')
        print(cal_date)
        cal_date = cal_date.split('calibration')[-1].strip()
        cal_date = cal_date.replace(' ', '')
        print(cal_date)
        cal_date_YYYYmmDD = datetime.datetime.strptime(cal_date, '%d%b%y').strftime('%Y%m%d')
    else:   
        cal_date_YYYYmmDD = 'Unknown'
    if 's/n' in calibcomm.values.item().decode('utf-8'):
        serial_match = re.search(r's/n\s*(\d+)', calibcomm.values.item().decode('utf-8'))
        serial_number = serial_match.group(0).replace('s/n  ', '').strip()
    else:
        serial_number = 'Unknown'
    print(serial_number)

    return cal_date_YYYYmmDD, serial_number

def _clean_anc_vars_list(ancillary_variables_str):
    ancillary_variables_str = re.sub(r"(\w)(sg_cal)", r"\1 \2", ancillary_variables_str)
    ancilliary_vars_list = ancillary_variables_str.split()
    ancilliary_vars_list = [var.replace('sg_cal_', '') for var in ancilliary_vars_list]
    return ancilliary_vars_list

def _assign_calval(sg_cal, anc_var_list):
    calval = {}
    for anc_var in anc_var_list:
        var_value = sg_cal[anc_var].values.item()
        calval[anc_var] = var_value
    return calval