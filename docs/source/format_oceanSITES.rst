OceanSITES format for AC1
=========================

This document outlines how the OceanSITES format (v1.4) applies to the `amocarray` datasets.

1. Overview
-----------

The AC1 format improves the interoperability for Atlantic Meridional Overturning Circulation (AMOC) mooring array datasets.  It uses NetCDF (Network Common Data Format) where the software is based on ``xarray.Dataset`` objects.  It is derived from the OceanSITES data format [see here](https://www.ocean-ops.org/oceansites/data/index.html) or [https://www.ocean-ops.org/oceansites/docs/oceansites_data_format_reference_manual.pdf](oceansites_data_format_reference_manual.pdf), but additionally attempts to specify vocabularies.

Note, if the link to the pdf is broken, here is a version downloaded in 2025 [oceansites_data_format_reference_manual.pdf](oceansites_data_format_reference_manual.pdf) which describes OceanSITES version 1.4.

**For developers:** Please read the OceanSITES data manual, and also check [https://cfconventions.org/cf-conventions/cf-conventions.html#discrete-sampling-geometries](https://cfconventions.org/cf-conventions/cf-conventions.html#discrete-sampling-geometries).

featureType
~~~~~~~~~~~

- For the RAPID T&S profiles at individual mooring sites, we are probably looking at a `featureType` of `timeSeriesProfile` (a series of profile features at the same horizontal position with time values in strict monotonically increasing order).  This may also apply for the gridded sections of T, S and V available at both RAPID and OSNAP.  For this, we may further want the "H.5.1 Multidimensional array representations of time series profiles".

axis and coordinates
~~~~~~~~~~~~~~~~~~~~
OceanSITES recommends coordinates with an "axis" attribute defining that they represent the X, Y, Z or T axis (which should appear in the relative order T, Z, Y, X). Here, they use the naming: `TIME`, `LATITUDE`, `LONGITUDE`, and `DEPTH`.  For Time, by default, it represents the *center of the data sample or averaging period*.  (**Note: this departs from OSNAP data files**).  Apparently in OceanSITES, "depth" is strongly preferred over "pressure".


Flags and QC
~~~~~~~~~~~~
For Flags, these are indicated as **<PARAM>_QC** with standard values "flag_values" = 0, 1, 2, 3, 4, 7, 8, 9 and "flag_meanings" = "unknown good_data probably_good_data potentially_correctable_bad_data bad_data nominal_value interpolated_value missing_value" (attribute to the variable) defined.  There is also an optional **<PARAM>_UNCERTAINTY** with "technique_title" as "Title of the document that describes the technique that was applied to estimate the uncertainty of the data".  I'm not sure whether either of these applies to the "_FLAG" for RAPID or the "_ERR" for OSNAP.  But OSNAP does have the "QC_indicator" and "Processing_level".  QC_indicator is OceanSITES specific (see table 2) and "processing_level" is table 3.

The QC_indicator (ref table 2) are used in the <PARAM>_QC variable to describe the quality of each measurement.  I'm not sure this is how OSNAP uses it.  Processing level options applied to all measurements of a variable and are given as an overall indicator in the attributes of each variable:

- Raw instrument data

- Instrument data that has been converted to geophysical values

- Post-recovery calibrations have been applied

- Data has been scaled using contextual information

- Known bad data has been replaced with null values

- Known bad data has been replaced with values based on surrounding
data

- Ranges applied, bad data flagged

- Data interpolated

- Data manually reviewed

- Data verified against model or other contextual information

- Other QC process applied

Parameter
~~~~~~~~~

3. Variables
------------

.. list-table:: Variables.  The requirement status (RS) is shown in the last column, where **M** is mandatory, *HD* is highly desirable, and *S* is suggested.
   :widths: 20 25 20 20 5
   :header-rows: 1

   * - Name
     - CF standard name
     - Long name
     - Description
     - RS
   * - PRES
     - sea_water_pressure
     - Pressure
     - Timestamps in UTC
     - **M**
   * - PSAL
     - sea_water_practical_salinity
     - Salinity
     -
     -
   * - TEMP
     - sea_water_temperature
     - temperature
     -
     -
   * - VCUR
     - northward_sea_water_velocity
     -
     -
     -
   * - UCUR
     - eastward_sea_water_velocity
     -
     -
     -
   *

Merged, gridded and derived data files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OceanSITES says a number of higher-level data products can be created:

- A "long time series" version that may concatenate multiple deployments (some homogenization)

- A "gridded" version which interpolates to a space-time grid different from native instrumental resolution (this is what OSNAP and RAPID provide for their TEMPERATURE and SALINITY fields)

- A "derived" data product (e.g., the "overturning circulation" or "meridional heat transport")

The file format for the higher-level data is netCDF. Each file is compliant with the
following conventions:

- CF metadata conventions: Standard names for data variables are required
when available, and all other CF conventions should be used when possible.

- Unidata Attribute Convention for Data Discovery (ACDD).  See [here](https://www.esipfed.org/what-is-acdd/).

- Additional metadata attributes from the deployment-by-deployment files (as
specified earlier in this document) are possible and welcome, as long as they
make sense for the data product in question.

OceanSITES file naming conventions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

According to OceanSITES, the filenaming convention is:

`OS_[PlatformCode]_[DeploymentCode]_[DataMode]_[PARTX].nc`

where for higher-level products, instead of `[DataMode]`, a code is inserted to define the type of data.  Instead of `[DeploymentCode]` a time range is used by default.  And for data from multiple platforms/sites, the `[PlatformCode]` can be replaced with an appropriate choice of site, project, array or network which can be taken from the global attributes of the underlying source data.

`OS_[PSPANCode]_[StartEndCode]_ [ContentType]_[PARTX].nc`

- [PSPANCode] - Deployment, platform, site, project, array, or network code from
the underlying source data files. If all data are from one deployment of one
platform, the platform and deployment code should be used. Else, move down the
sequence terms until one is found that is unique and appropriate for all data in the
file. This could be "OSNAP", "RAPID", "MOVE", "SAMBA"?

- [StartEndCode] - A code that describes the time range of the data in the file.
Preferred format is e.g. “20050301-20190831” to indicate data from March 2005
through August 2019.

- [ContentType] - A three-letter code that describes the content of the file
(distinguished from the deployment files, which have a one-letter code here), one
of:
  - LTS: The data are “long time series” data that are essentially at the native instrumental resolution in space and time. The primary difference from the deployment-by-deployment files is that a single file contains merged data from multiple deployments.
  - GRD: The data are “gridded”, meaning that some sort of binning, averaging, interpolating has been done to format the data onto a space-time grid that is different from the native resolution, and more than a simple concatenation like the “LTS” option.
  - DPR: The data are a “derived product”, which means that there are data that were derived from multiple sites or some other higher-order processing that the data provider distinguishes from the lower-level data.

- [PARTX] - An optional user-defined field for additional identification or explanation of data. For gridded data, this could include the record interval as subfields of ISO 8601 (PnYnMnDTnHnMnS), e.g. P1M for monthly data, T30M for 30 minutes, T1H for hourly.


Units
~~~~~

Check out [udunits](https://docs.unidata.ucar.edu/udunits/current/).

SI base units (XML) are [here](https://docs.unidata.ucar.edu/udunits/current/udunits2-base.xml)

Derived units (XML) are [here](https://docs.unidata.ucar.edu/udunits/current/udunits2-derived.xml).

Non-SI units including sverdrup, **where apparently we cannot use Sv because it also means "sievert" in the SI unit-system**.
