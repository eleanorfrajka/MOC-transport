.. This file is included under 'format_orig.rst' and should use '~~' or lower as the top header level.

.. _array-osnap:
OSNAP Original Data Format
-----------------------

The OSNAP array provides multiple observational data products including time series of overturning and heat/freshwater transport, streamfunctions in density space, and gridded fields of velocity, temperature, and salinity.


At OSNAP, we have variables like MOC_ALL, MOC_EAST and MOC_WEST which are time series (``TIME``), but these could be represented as MOC (``N_PROF``, ``TIME``) where instead of the three different variables, N_PROF=3.  This would be somewhat more difficult to communicate to the user, since LATITUDE and LONGITUDE are not single points per N_PROF but instead may represent end points of a section.

Variables MOC_ALL_ERR are also provided, which could be translated to MOC_ERR (``N_PROF``, ``TIME``) with LATITUDE (``N_PROF``) or LATITUDE_BOUND (``N_PROF``, 2).

Heat fluxes also exist, as MHT_ALL, MHT_EAST and MHT_WEST, so these could be MHT (``N_PROF``, ``TIME``).


OSNAP_MOC_MHT_MFT_TimeSeries_201408_202006_2023.nc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 70
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``TIME``
     - ``TIME``
     - (71,)
     - datetime
     -
       - **standard_name**: ``time``
       - **long_name**: `Start date` of each monthly period
       - **units**: days since 1950-01-01
       - **comment**: Start date of each month
       - **processing_level**: data manually reviewed
   * - ``MOC_ALL``
     - ``TIME``
     - (71,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Total MOC
       - **description**: Maximum overturning streamfunction across full OSNAP array
       - **comment**: Maximum of the overturning streamfunction in sigma_theta coordinates
       - **QC_indicatoris**: good data
       - **processing_level**: data manually reviewed
   * - ``MOC_ALL_ERR``
     - ``TIME``
     - (71,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: MOC uncertainty
       - **description**: Uncertainty in MOC_ALL
       - **comment**: Determined from a Monte Carlo analysis
   * - ``MOC_EAST``
     - ``TIME``
     - (71,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: MOC east
       - **description**: Overturning streamfunction at OSNAP East
       - **comment**: Maximum of the overturning streamfunction in sigma_theta coordinates
       - **QC_indicatoris**: good data
       - **processing_level**: data manually reviewed
   * - ``MHT_ALL``
     - ``TIME``
     - (71,)
     - PW
     -
       - **standard_name**: ``Heat_transport``
       - **long_name**: Heat transport
       - **description**: Meridional heat transport across full OSNAP array
       - **QC_indicatoris**: good data
       - **processing_level**: data manually reviewed
   * - ``MFT_ALL``
     - ``TIME``
     - (71,)
     - Sv
     -
       - **standard_name**: ``Freshwater_transport``
       - **long_name**: Freshwater transport
       - **description**: Meridional freshwater transport across full OSNAP array
       - **QC_indicatoris**: good data
       - **processing_level**: data manually reviewed

OSNAP_Streamfunction_201408_202006_2023.nc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 70
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``TIME``
     - ``TIME``
     - (71,)
     - datetime
     -
       - **standard_name**: ``time``
       - **long_name**: Start date of each monthly period
       - **units**: days since 1950-01-01
       - **comment**: Start date of each month
       - **processing_level**: data manually reviewed
   * - ``LEVEL``
     - ``LEVEL``
     - (481,)
     - kg m-3
     -
       - **standard_name**: ``potential_density``
       - **long_name**: Sigma-theta levels
       - **description**: Potential density surfaces (\sigma\theta)
       - **processing_level**: data manually reviewed
   * - ``T_ALL``
     - ``LEVEL``, ``TIME``
     - (481, 71)
     - Sv
     -
       - **standard_name**: ``Transport``
       - **long_name**: Streamfunction total
       - **description**: Streamfunction in \sigma\theta coordinates across full OSNAP
       - **comment**: Streamfunction in sigma_theta coordinates
       - **QC_indicatoris**: good data
       - **processing_level**: data manually reviewed
   * - ``T_EAST``
     - ``LEVEL``, ``TIME``
     - (481, 71)
     - Sv
     -
       - **standard_name**: ``Transport``
       - **long_name**: Streamfunction east
       - **description**: Streamfunction in \sigma\theta at OSNAP East
       - **comment**: Streamfunction in sigma_theta coordinates
       - **QC_indicatoris**: good data
       - **processing_level**: data manually reviewed
   * - ``T_WEST``
     - ``LEVEL``, ``TIME``
     - (481, 71)
     - Sv
     -
       - **standard_name**: ``Transport``
       - **long_name**: Streamfunction west
       - **description**: Streamfunction in \sigma\theta at OSNAP West
       - **comment**: Streamfunction in sigma_theta coordinates
       - **QC_indicatoris**: good data
       - **processing_level**: data manually reviewed


OSNAP_Gridded_201408_202006_2023.nc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 70
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``TIME``
     - ``TIME``
     - (71,)
     - datetime
     -
       - **standard_name**: ``time``
       - **long_name**: Start date of each monthly period
       - **units**: days since 1950-01-01
       - **comment**: Start date of each month
       - **processing_level**: data manually reviewed
   * - ``LATITUDE``
     - ``LATITUDE``
     - (256,)
     - degrees_north
     -
       - **standard_name**: ``latitude``
       - **long_name**: Latitude
       - **description**: Latitude in degrees
       - **axis**: Y
   * - ``LONGITUDE``
     - ``LONGITUDE``
     - (256,)
     - degrees_east
     -
       - **standard_name**: ``longitude``
       - **long_name**: Longitude
       - **description**: Longitude in degrees
       - **axis**: X
   * - ``DEPTH``
     - ``DEPTH``
     - (199,)
     - m
     -
       - **standard_name**: ``depth``
       - **long_name**: Depth
       - **description**: Depth in meters
       - **positive**: down
       - **axis**: Z
   * - ``VELO``
     - ``TIME``, ``DEPTH``, ``LONGITUDE``
     - (71, 199, 256)
     - m s-1
     -
       - **standard_name**: ``sea_water_velocity``
       - **long_name**: Velocity
       - **description**: Cross-sectional velocity along OSNAP
       - **QC_indicator**: good data
       - **processing_level**: Data manually reviewed
   * - ``TEMP``
     - ``TIME``, ``DEPTH``, ``LONGITUDE``
     - (71, 199, 256)
     - degC
     -
       - **standard_name**: ``sea_water_temperature``
       - **long_name**: Temperature
       - **description**: In-situ temperature along OSNAP
       - **QC_indicator**: good data
       - **processing_level**: Data manually reviewed
   * - ``SAL``
     - ``TIME``, ``DEPTH``, ``LONGITUDE``
     - (71, 199, 256)
     - psu
     -
       - **standard_name**: ``sea_water_practical_salinity``
       - **long_name**: Salinity
       - **description**: Practical salinity along OSNAP
       - **QC_indicator**: good data
       - **processing_level**: Data manually reviewed
