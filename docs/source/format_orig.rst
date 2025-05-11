Array Format (Native / Original)
=================================

This document describes some of the native data formats present in AMOC datasets provided by different observing arrays.

In the logic of `amocarray`, we will first convert to an OceanSITES compatible format.  Documentation is outlined in the :doc:`OceanSITES format <format_oceanSITES>`.

**Note:** This is a work in progress and not all arrays are fully described.  The goal is to provide a summary of the data formats and how they could be transformed into a common format.  The common format is not yet defined but will ideally be able to capture most if not all of the original data.


**Table of Contents**

- :ref:`RAPID <array-rapid>`
- :ref:`OSNAP <array-osnap>`
- :ref:`MOVE <array-move>`
- :ref:`SAMBA <array-samba>`
- :ref:`FW2015 <array-fw2015>`
- :ref:`MOCHA <array-mocha>`


.. _array-rapid:

RAPID
~~~~~

For example, at 26°N, the RAPID array produces an AMOC transport time series (volume transport in depth space) which is a 1-dimensional time series with a single registered latitude (26.5) and no registered longitude.  It also provides profiles of temperature, salinity and dynamic height representing individual locations (single latitude, single nominal longitude) on a vertical grid of 20 dbar.  Several locations are provided, with names like WB, MAR_WEST, MAR_EAST, EB.  So there are N_PROF locations, with N_LEVELS and also TIME as dimensions. And the LATITUDE would be ``N_PROF`` (a small number, like 4, representing mooring locations)

More recently, they have started providing a section of temperature, saliity and velocity which are then N_PROF, TIME and N_LEVELS, but now the ``N_PROF`` (and both ``LONGITUDE`` and ``LATITUDE``) would be on a regular grid--or at least with more locations (longer N_PROF), though it's possible LATITUDE would be a single latitude (26.5).

RAPID also provides layer transports which are single time series with names like t_therm10, t_aiw10, t_ud10, t_ld10, etc, which are between specified depth ranges.  These could be simply: ``TRANSPORT`` (``N_LEVELS``, ``TIME``) with ``DEPTH_BOUND`` (``N_LEVELS``, 2) to give an upper and lower bound on the depths used to produce transport in layers?  It would also need something like ``TRANSPORT_NAME`` (``N_LEVELS``) of type string.

Check CF conventions for standard names: https://github.com/cf-convention/vocabularies/issues.  Note that **standard names** consist of lower-letters, digits and underscores, and begin with a letter. Upper case is not used.  See [here](https://cfconventions.org/Data/cf-standard-names/docs/guidelines.html).




Summary of RAPID files:
-----------------------

- ``moc_vertical.nc``:

  - ``depth``: dimension ``depth`` (307,), units `m`, type float64

  - ``time``: dimension ``time`` (13779,), type datetime

  - ``stream_function_mar``: (``depth``, ``time``), units `Sv`, type float64

  - **Convert to OceanSITES:** Here, we should change the dimension to all-caps ``DEPTH`` and ``TIME``.  Units on the streamfunction should be `sverdrup` to de-confliict with `Sv` for sievert. According to OceanSITES, the order of the variables should be  T, Z, Y, X, so the streamfunction should be (``TIME``, ``DEPTH``).  The filename should be something like ``OS_RAPID_YYYYMMDD-YYYYMMDD_DPR_moc_vertical.nc``. Here, we are using the ``OS`` prefix, ``RAPID`` as the PlatformCode, the date start and end for the DeploymentCode, and the data mode is ``DPR`` for derived product.  The additional text after is the original filename, ``moc_vertical.nc``.


- ``ts_gridded.nc``:

  - ``pressure``: dimension `depth` (242,), units `dbar`, type float64

  - ``time``: dimension `time` (13779,), type datetime

  - ``TG_west``: (`depth`, `time`), units `degC`, type float64, long name "Temperature west 26.52N/76.74W"

  - ``SG_wb3```: (`depth`, `time`), units `psu`, type float64, long name "Salinity WB3 26.50N/76.6W"

  - ``TG_marwest```: long name "Temperature MAR west 24.52N/50.57W"

  - ``TG_mareast``: long name "Temperature MAR east 24.52N/41.21W`

  - ``TG_east``: long name "Temperature east 26.99N/16.23W"

  - ``TG_west_flag``: (depth, time) with long name "Temperature west data FLAG" and units "data flag"

- **Convert to OceanSITES:** Dimensions should be ``TIME`` and ``DEPTH``, where the coordinate name can be ``PRES`` for ``pressure``.  The featureType global attribute can be ``timeSeriesProfile``.

- ``moc_transports.nc``:

  - ``time``: dimension `time` (13779,), type datetime

  - ``t_therm10``: (`time`,), units `Sv`, type float64, long name "thermocline recirculation 0-800m"

  - ``t_aiw10``: (`time`,), units `Sv`, type float64, long name "intermediate water 800-1100m"

  - ``t_ud10``: (`time`,), units `Sv`, type float64, long name "upper NADW 1100-3000m"

  - ``t_ld10``: (`time`,), units `Sv`, type float64, long name "lower NADW 3000-5000m"

  - ``t_bw10``: (`time`,), units `Sv`, type float64, long name "AABW >5000m"

  - ``t_gs10``: (`time`,), units `Sv`, type float64, long name "Florida Straits transport"

  - ``t_ek10``: (`time`,), units `Sv`, type float64, long name "Ekman transport"

  - ``t_umo10``: (`time`,), units `Sv`, type float64, long name "upper Mid-Ocean transport"

  - ``moc_mar_hc10``: (`time`,), units `Sv`, type float64, long name "overturning transport"

- ``2d_gridded.nc``:

  - ``time``: dimension `time` (689,), type datetime

  - ``longitude``: dimension `longitude` (254,), type float64

  - ``depth``: dimension `depth` (307,), type float64

  - ``CT``: (`time`, `longitude`, `depth`), units `degC` ITS-90?

  - ``SA``: same as CT, units g/kg.

  - ``V_insitu``: (`time`, `longitude`, `depth`) Meridional velocity

  - ``V_ekman``: Ekman velocity in m/s.

  - ``V_net``: (`time`), net meridional velocity in m/s.

- ``meridional_transports.nc``:

  - ``time``: dimension `time` (689,), type datetime

  - ``depth``: (307,)

  - ``sigma0``: (631, ) potential density with reference pressure = 0

  - ``amoc_depth``: (`time`,), maximum of streamfunction evaluated in depth coordinates.  Units Sv.

  - ``amoc_sigma``: (`time`,), maximum of streamfunction evaluated in sigma coordinates.  Units Sv.

  - ``heat_trans``: (`time`,) meridional (northward) heat transport, units PW.

  - ``frwa_trans``: (`time`,) meridional freshwater transport, units Sv.

  - ``press``: (depth,) pressure in dbar

  - ``stream_depth``: (`time`, `depth`)` streamfunction evaluated in depth space. Units Sv.

  - ``stream_sigma``: (`time`, `sigma0`) streamfunction evaluated in density space. Units Sv.


Potential reformats:
--------------------


**Key Products**:

- **Overturning:**
  - ``MOC``: time series (dimension: ``TIME``)

  - ``STREAMFUNCTION``: (``DEPTH``, ``TIME``) - this is the vertical profile of MOC (originally ``stream_function_mar`` in ``moc_vertical.nc``, note that this extends deeper than the depth grid in ``ts_gridded.nc`` due to the incorporation of an AABW profile).

- **Profiles:** ``TEMPERATURE``, ``SALINITY``, vertically gridded at mooring locations.

  - Dimensions: ``TIME``, ``N_PROF``, ``N_LEVELS`` (242,1)

  - Coordinates: ``LATITUDE``, ``LONGITUDE`` (``N_PROF``=5,) - these would be the locations of the profiles, which are current in the "long name" for each of the ``TG_west``, ``TG_east``, ``TG_wb3``, ``TG_MARWEST``, ``TG_mareast``.  etc. ``TIME`` in datetime.  And ``PRESSURE`` (``N_LEVELS``,) - this is the depth grid in ``ts_gridded.nc``.

  - Variables: ``TEMPERATURE``, ``SALINITY``, ``TEMPERATURE_FLAG``, ``SALINITY_FLAG`` (``TIME``, ``N_PROF``, ``N_LEVELS``).  Attributes would specify units and the version of temperature/salinity.   and specifying what version of temperature/salinity.   The flags would have an attribute describing what the values mean (e.g. "1=good, 2=bad, etc").

- **Gridded sections:** ``TEMPERATURE``, ``SALINITY``, ``VELOCITY``

  - Dimensions: ``TIME``, ``N_PROF``, ``N_LEVELS`` (13000, longitude grid, 242?)

  - Coordinates: ``LATITUDE``, ``LONGITUDE`` (``N_PROF``=longitude grid,), ``TIME`` in datetime.  And ``PRESSURE`` (``N_LEVELS``,)

  - Variables: ``TEMPERATURE``, ``SALINITY``, ``VELOCITY`` (``TIME``, ``N_PROF``, ``N_LEVELS``).  Attributes would specify units and the version of temperature/salinity.   and specifying what version of temperature/salinity.   The flags would have an attribute describing what the values mean (e.g. "1=good, 2=bad, etc").

- **Layer transports:**

  - Dimensions: ``TIME``, ``N_LEVELS`` (13779, 5)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  And ``DEPTH_BOUND`` (``N_LEVELS``, 2) - this would be the depth bounds for the transport layers.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_LEVELS``) - this would be the time series of transport in layers.  This would also have ``DEPTH_BOUND`` (``N_LEVELS``, 2) to give an upper and lower bound on the depths used to produce transport in layers.  It would also need something like ``TRANSPORT_NAME`` (``N_LEVELS``, string) to indicate what the layer is (e.g. `t_therm10`, `t_aiw10`, etc).

- **Component transports:**

  - Dimensions: ``TIME``, ``N_COMPONENT`` (13779, 5)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  ``N_COMPONENT`` for the number of components.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_COMPONENT``) -  This would also have ``TRANSPORT_NAME`` (``N_COMPONENT``, string) to indicate what the component is (e.g. `t_gs10`, `t_ek10`, etc).  This would be similar to the layer transport but without the depth bounds.


.. _array-osnap:

OSNAP
~~~~~

At OSNAP, we have variables like MOC_ALL, MOC_EAST and MOC_WEST which are time series (``TIME``), but these could be represented as MOC (``N_PROF``, ``TIME``) where instead of the three different variables, N_PROF=3.  This would be somewhat more difficult to communicate to the user, since LATITUDE and LONGITUDE are not single points per N_PROF but instead may represent end points of a section.

Variables MOC_ALL_ERR are also provided, which could be translated to MOC_ERR (``N_PROF``, ``TIME``) with LATITUDE (``N_PROF``) or LATITUDE_BOUND (``N_PROF``, 2).

Heat fluxes also exist, as MHT_ALL, MHT_EAST and MHT_WEST, so these could be MHT (``N_PROF``, ``TIME``).



Summary of OSNAP files:
-----------------------

- ``OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc``

  - ``TIME``: dimension ``TIME`` (71,), type datetime

  - ``MOC_ALL``: dimension ``TIME``, units `Sv`, long_name = "Total MOC", QC_indicatoris = "good data", processing_level = "data manually reviewed", comment = "maximum of the overturning streamfunction in sigma_theta coordinates", description = "Maximum overturning streamfunction across full OSNAP array", standard_name = "Transport_anomaly"

  - ``MOC_ALL_ERR``: dimension ``TIME``, units `Sv`, long_name = "MOC uncertainty", comment = "Determined from a Monte Carlo analysis".  description ="Uncertainty in MOC_ALL", standard_name = "Transport_anomaly"

  - ``MOC_EAST``: dimension ``TIME``, units `Sv`, long_name = "MOC east", QC_indicatoris = "good data", processing_level = "data manually reviewed", comment = "maximum of the overturning streamfunction in sigma_theta coordinates", description = "Overturning streamfunction at OSNAP East", standard_name = "Transport_anomaly"

  - ``MHT_ALL``: dimension ``TIME``, units `PW`, long_name = "Heat transport", QC_indicatoris = "good data", processing_level = "data manually reviewed", description = "Meridional heat transport across full OSNAP array", standard_name = "Heat_transport"

  - ``MFT_ALL``: dimension ``TIME``, units `Sv`, long_name = "Freshwater transport", QC_indicatoris = "good data", processing_level = "data manually reviewed", description = "Meridional freshwater transport across full OSNAP array", standard_name = "Freshwater_transport"

- ``OSNAP_Streamfunction_201408_202006_2023.nc`` (71, sigma=481)

  - ``TIME``: dimension ``TIME`` (71,), type datetime.  standard_name = "time", long_name = "Start date of each monthly period", axis = "T", processing_level = "data manually reviewed", units = "days since 1950-01-01", units = "dates since 1950-01-01", comment = "Start date of each month"

  - ``LEVEL``: dimension ``LEVEL``  (481,), float64, ranging from 23.3 to 28.1. standard_name = "potential_density", long_name = "Sigma-theta levels", units = "kg m-3", processing_level = "data manually reviewed", description = "Potential density surfaces (\sigma\theta)"

  - ``T_ALL``: dimension (``LEVEL``, ``TIME``), units `Sv`, long_name = "Streamfunction total", QC_indicatoris = "good data", processing_level = "data manually reviewed", comment = "Streamfunction in sigma_theta coordinates", description = "Streamfunction in \sigma\theta coordinates across full OSNAP", standard_name = "Transport"

  - ``T_EAST``: dimension (``LEVEL``, ``TIME``), units `Sv`, long_name = "Streamfunction east", QC_indicatoris = "good data", processing_level = "data manually reviewed", comment = "Streamfunction in sigma_theta coordinates", description = "Streamfunction in \sigma\theta at OSNAP East", standard_name = "Transport"

  - ``T_WEST``: dimension (``LEVEL``, ``TIME``), units `Sv`, long_name = "Streamfunction west", QC_indicatoris = "good data", processing_level = "data manually reviewed", comment = "Streamfunction in sigma_theta coordinates", description = "Streamfunction in \sigma\theta at OSNAP West", standard_name = "Transport"

- ``OSNAP_Gridded_201408_202006_2023.nc``  (71, depth=199, 256)

  - ``TIME``: dimension ``TIME`` (71,), type datetime.  standard_name = "time", long_name = "Start date of each monthly period", axis = "T", processing_level = "data manually reviewed", units = "days since 1950-01-01", units = "dates since 1950-01-01", comment = "Start date of each month"

  - ``LATITUDE``: dimension ``LATITUDE`` (256,), type float32, standard_name = "latitude", long_name = "Latitude", units = "degrees_north", axis = "Y", description = "Latitude in degrees"

  - ``LONGITUDE``: dimension ``LONGITUDE`` (256,), type float32, standard_name = "longitude", long_name = "Longitude", units = "degrees_east", axis = "X", description = "Longitude in degrees"

  - ``DEPTH``: dimension ``DEPTH`` (199,), type float32, ranging from 15 to 3975, standard_name = "depth", long_name = "Depth", units = "m", positive = "down", axis = "Z", description = "Depth in meters"

  - ``VELO``: dimension (``TIME``, ``DEPTH``, ``LONGITUDE``), float32, standard_name = "sea_water_velocity", long_name = "Velocity", units = "m s-1", QC_indicator = "good data", processing_level = "Data manually reviewed", description = "Cross-sectional velocity along OSNAP"

  - ``TEMP``: dimension (``TIME``, ``DEPTH``, ``LONGITUDE``), float32, standard_name = "sea_water_temperature", long_name = "Temperature", units = "degC", QC_indicator = "good data", processing_level = "Data manually reviewed", description = "In-situ temperature along OSNAP"

  - ``SAL``: dimension (``TIME``, ``DEPTH``, ``LONGITUDE``), float32, standard_name = "sea_water_practical_salinity", long_name = "Salinity", units = "psu", QC_indicator = "good data", processing_level = "Data manually reviewed", description = "Practical salinity along OSNAP"

Potential reformats:
--------------------

- **Overturning:**
  - ``MOC`` and ``MOC_ERR``: time series (dimension: ``TIME``, ``N_LOCATION``=3) where ``N_LOCATION``=3 (e.g. MOC_ALL, MOC_EAST, MOC_WEST)

  - ``STREAMFUNCTION``: (``N_LEVELS``, ``TIME``, ``N_PROF``=3) - This would be from ``OSNAP_Streamfunction_201408_202006_2023.nc``and is the overturning streamfunction in sigma-theta coordinates.

  - ``MHT`` and ``MHT_ERR``: same dimensions as ``MOC``

  - ``MFT`` and ``MFT_ERR``: same dimensions as ``MOC``

  - ``LATITUDE_BOUND``: (``N_LOCATION``, 3) - this would be the latitude bounds for the west, east and full.

  - ``LONGITUDE_BOUND``: (``N_LOCATION``, 3) - this would be the longitude bounds for the west, east and full.


- **Gridded sections:** ``TEMPERATURE``, ``SALINITY``, ``VELOCITY``

  - Dimensions: ``TIME``, ``N_PROF``, ``N_LEVELS`` (71, depth=199, longitude=256)

  - Coordinates: ``LATITUDE``, ``LONGITUDE`` (``N_PROF``=longitude grid,), ``TIME`` in datetime.  And ``DEPTH`` (``N_LEVELS``,)

  - Variables: ``TEMPERATURE``, ``SALINITY``, ``VELOCITY`` (``TIME``, ``N_PROF``, ``N_LEVELS``).  Attributes would specify units and the version of temperature/salinity.   and specifying what version of temperature/salinity.   The flags would have an attribute describing what the values mean (e.g. "1=good, 2=bad, etc").


.. _array-move:

MOVE
~~~~

MOVE provides the TRANSPORT_TOTAL which corresponds to the MOC, but also things like transport_component_internal (``TIME``,), transport_component_internal_offset (``TIME``,), and transport_component_boundary (``TIME``,).  This would be similar to RAPID's version of "interior transport" and "western boundary wedge", but it's not so clear how to make these similarly named.


Summary of MOVE files:
----------------------

- ``OS_MOVE_TRANSPORTS.nc``: time coverage 2000-01-01 to 2018-06-30

  - ``TIME``: dimension ``TIME`` (6756,), type datetime

  - ``TRANSPORT_TOTAL``: dimension ``TIME``, units `Sverdrup`, valid_min -100.0, valid_max 100.0.  long_name = "Total ocean volume transport across the MOVE line between Guadeloupe and Researcher Ridge in the depth layer defined by pressures 1200 to 4950 dbar", "standard_name" = "ocean_volume_transport_across_line".

  - ``transport_component_internal``: dimension ``TIME``, units `Sverdrup`, valid_min -100.0, valid_max 100.0.  long_name = "Internal component of ocean volume transport across the MOVE line".

  - ``transport_component_internal_offset``: dimension ``TIME``, units `Sverdrup`, valid_min -100.0, valid_max 100.0.  long_name = "Offset to be added to internal component of ocean volume transport across the MOVE line".

  - ``transport_component_boundary``: dimension ``TIME``, units `Sverdrup`, valid_min -100.0, valid_max 100.0.  long_name = "Boundary component of ocean volume transport across the MOVE line".

- **Notes**: Similar in structure to RAPID layer decomposition but naming is inconsistent between RAPID and MOVE.

Potential reformats:
--------------------

- **Overturning:**
  - ``MOC``: time series (dimension: ``TIME``)

- **Component transports:**

  - Dimensions: ``TIME``, ``N_COMPONENT`` (13779, 3)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  ``N_COMPONENT`` for the number of components.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_COMPONENT``) -  This would also have ``TRANSPORT_NAME`` (``N_COMPONENT``, string) to indicate what the component is (e.g. `transport_component_internal`, `transport_component_internal_offset`, `transport_component_boundary`, etc).


.. _array-samba:

SAMBA
~~~~~

SAMBA (Upper_Abyssal_Transport_Anomalies.txt) has two main variables which are (``TIME``,), named 'upper-cell volume transport anomaly' which suggests a quantity TRANSPORT_ANOMALY (``N_LEVELS``, ``TIME``), where we would then have again a DEPTH_BOUND (``N_LEVELS``, 2).

But the other SAMBA product (MOC_TotalAnomaly_and_constituents.asc) also has a "Total MOC anomaly" (``MOC``), a "Relative (density gradient) contribution" which is like MOVE's internal or RAPID's interior.  There is a "Reference (bottom pressure gradient) contribution" which is like MOVE's offset or RAPID's compensation.  An Ekman (all have this--will need an attribute with the source of the wind fields used), and also a separate **"Western density contribution"** and **"Eastern density contribution"** which are not available in the RAPID project, and are not the same idea as the OSNAP west and OSNAP east, but could suggest an (``N_PROF``=2, ``TIME``) for west and east.

Summary of SAMBA files:
-----------------------

- ``Upper_Abyssal_Transport_Anomalies.txt`` (``TIME``=1404)

  - ``TIME``: dimension ``TIME`` (1404,), type datetime

  - ``UPPER_TRANSPORT``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description ="Upper-cell volume transport anomaly (relative to record-length average of 17.3 Sv)", standard_name = "Transport_anomaly"

  - ``ABYSSAL_TRANSPORT``:  dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description ="Abyssal-cell volume transport anomaly (relative to record-length average of 7.8 Sv)", standard_name = "Transport_anomaly"


- ``MOC_TotalAnomaly_and_constituents.asc`` (``TIME``=2964)

  - ``TIME``: dimension ``TIME`` (2964,), type datetime

  - ``MOC``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description ="MOC Total Anomaly (relative to record-length average of 14.7 Sv)", standard_name = "Transport_anomaly"

  - ``RELATIVE_MOC``: dimension ``TIME``, units `Sv`, long_name = "Relative (density gradient) contribution", description ="Relative (density gradient) contribution to MOC anomaly", standard_name = "Transport_anomaly"

  - ``BAROTROPIC_MOC``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly",  description ="Reference (bottom pressure gradient) contribution to MOC anomaly", standard_name = "Transport_anomaly"

  - ``EKMAN``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description = "Ekman (wind) contribution to the MOC anomaly", standard_name = "Transport_anomaly"

  - ``WESTERN_DENSITY``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description ="Western density contribution to the MOC anomaly", standard_name = "Transport_anomaly"

  - ``EASTERN_DENSITY``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description ="Eastern density contribution to the MOC anomaly", standard_name = "Transport_anomaly"

  - ``WESTERN_BOT_PRESSURE``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description ="Western bottom pressure contribution to the MOC anomaly", standard_name = "Transport_anomaly"

  - ``EASTERN_BOT_PRESSURE``: dimension ``TIME``, units `Sv`, long_name = "Transport_anomaly", description ="Eastern bottom pressure contribution to the MOC anomaly", standard_name = "Transport_anomaly"

Potential reformats:
--------------------

- **Overturning:**

  - ``MOC``: time series (dimension: ``TIME``)

**Note:** Check the readme to see what the relationship is between the upper, abyssal and MOC transports.


- **Component transports:**

  - Dimensions: ``TIME``, ``N_COMPONENT`` (1404, 7)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  ``N_COMPONENT`` for the number of components.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_COMPONENT``) -  This would also have ``TRANSPORT_NAME`` (``N_COMPONENT``, string) to indicate what the component is (e.g. `RELATIVE_MOC`, `BAROTROPIC_MOC`, `EKMAN`, `WESTERN_DENSITY`, etc).

**Note:** It would be good to verify how these components should (or shouldn't) add up to the total transports.


.. _array-fw2015:

FW2015
~~~~~~

This is a different beast but similar to RAPID in that it has components which represent transport for different segments of the array (like Gulf Stream, Ekman and upper-mid-ocean) where these sum to produce MOC.  This is *vaguely* like OSNAP east and OSNAP west, except I don't think those sum to produce the total overturning.  And Ekman could be part of a layer transport but here is has no depth reference.  Gulf Stream has longitude bounds and a single latitude (``LATITUDE``, ``LONGITUDE_BOUND``) and limits over which the depths are represented (``DEPTH_BOUND``?) but no N_LEVELS.  It doesn't quite make sense to call the dimension N_PROF since these aren't profiles.  Maybe **N_COMPONENT**?


Summary of FW2015 files:
------------------------

- ``MOCproxy_for_figshare_v1.mat``

  - ``TIME``: dimension ``TIME`` (264,), type datetime

  - ``MOC_PROXY``: dimension ``TIME``, units `Sv`

  - ``EK``: dimension ``TIME``, units `Sv`

  - ``GS``: dimension ``TIME``, units `Sv`

  - ``UMO_PROXY``: dimension ``TIME``, units `Sv`

Potential reformats:
--------------------

- **Overturning:**

  - ``MOC``: time series (dimension: ``TIME``)

- **Component transports:**

  - Dimensions: ``TIME``, ``N_COMPONENT`` (1404, 7)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  ``N_COMPONENT`` for the number of components.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_COMPONENT``) -  This would also have ``TRANSPORT_NAME`` (``N_COMPONENT``, string) to indicate what the component is (e.g. `EK`, `GS`, `LNADW`, `MOC`, `MOC_PROXY`, `UMO_GRID`, `UMO_PROXY`, `UNADW_GRID`, etc).  Note that some of these were just copies of what the RAPID time series was at the time.





.. _array-mocha:

MOCHA
~~~~~


Summary of MOCHA files:
-----------------------

The heat transports at RAPID-MOCHA are provided with N_LEVELS, TIME, and variables:

- Q_eddy

- Q_ek

- Q_fc

- Q_gyre

- Q_int.

Again, we have a situation where N_PROF isn't really appropriate.  Maybe **N_COMPONENT**?  WE should double check that things called **N_COMPONENT** then somehow sum to produce a total?  Then we would have something like MHT_COMPONENTS (``N_COMPONENT``, ``TIME``) and MHT (``TIME``)

But we also have things like:

- T_basin (``TIME``, ``N_LEVELS``)

- T_basin_mean (``N_LEVELS``)

- T_fc_fwt (``TIME``)

- V_basin (``TIME``, ``N_LEVELS``) --> is this identical to new RAPID velo sxn?

- V_basin_mean (``N_LEVELS``)

- V_fc (``TIME``, ``N_LEVELS``)


Potential reformats:
--------------------

So this might be suggested as a TEMPERATURE (``TIME``, ``N_LEVELS``) but unclear how to indicate that this is a zonal mean temperature as compared to the ones which are TEMPERATURE (``N_PROF``, ``TIME``, ``N_LEVELS``) for the full sections.


- **Heat Transport Components**:

  - `Q_eddy`, `Q_ek`, `Q_fc`, `Q_gyre`, `Q_int` → suggest ``MHT_COMPONENT`` (``N_COMPONENT``, ``TIME``)

  - Total: ``MHT`` (``TIME``)

- **Additional Variables**:

  - `T_basin`, `V_basin`, `T_fc_fwt`, etc.

  - These suggest basin-mean properties: ``TEMPERATURE`` (``TIME``, ``N_LEVELS``)

- **Note**: ``N_COMPONENT`` should indicate summable components if applicable


