.. This file is included under 'format_orig.rst' and should use '~~' or lower as the top header level.

.. _array-rapid:
RAPID Original Data Format
--------------------------

The RAPID array at 26°N produces a range of observational and derived products:

- 1D time series of AMOC transport
- Time series profiles of temperature, salinity, and velocity at specific locations (moorings)
- Gridded sections of hydrographic and velocity fields
- Layer transport estimates based on defined vertical boundaries
- Streamfunction evaluations in depth or density space


moc_vertical.nc
~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 35
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``depth``
     - ``depth``
     - (307,)
     - m
     - Vertical coordinate in meters
   * - ``time``
     - ``time``
     - (13779,)
     - datetime
     - Time coordinate, 12-hour intervals
   * - ``stream_function_mar``
     - ``depth``, ``time``
     - (307, 13779)
     - Sv
     - Overturning streamfunction at 26°N

ts_gridded.nc
~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 35
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``pressure``
     - ``depth``
     - (242,)
     - dbar
     - Pressure coordinate
   * - ``time``
     - ``time``
     - (13779,)
     - datetime
     - Time coordinate, 12-hour intervals
   * - ``TG_west``
     - ``depth``, ``time``
     - (242, 13779)
     - °C
     - Temperature west 26.52N/76.74W
   * - ``SG_wb3``
     - ``depth``, ``time``
     - (242, 13779)
     - psu
     - Salinity WB3 26.50N/76.6W
   * - ``TG_marwest``
     - ``depth``, ``time``
     - (242, 13779)
     - °C
     - Temperature MAR west 24.52N/50.57W
   * - ``TG_mareast``
     - ``depth``, ``time``
     - (242, 13779)
     - °C
     - Temperature MAR east 24.52N/41.21W
   * - ``TG_east``
     - ``depth``, ``time``
     - (242, 13779)
     - °C
     - Temperature east 26.99N/16.23W
   * - ``TG_west_flag``
     - ``depth``, ``time``
     - (242, 13779)
     - 1
     - Data quality flag for ``TG_west``

moc_transports.nc
~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 35
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``time``
     - ``time``
     - (13779,)
     - datetime
     - Time coordinate, 12-hour intervals
   * - ``t_therm10``
     - ``time``
     - (13779,)
     - Sv
     - Thermocline recirculation 0–800 m
   * - ``t_aiw10``
     - ``time``
     - (13779,)
     - Sv
     - Intermediate water 800–1100 m
   * - ``t_ud10``
     - ``time``
     - (13779,)
     - Sv
     - Upper NADW 1100–3000 m
   * - ``t_ld10``
     - ``time``
     - (13779,)
     - Sv
     - Lower NADW 3000–5000 m
   * - ``t_bw10``
     - ``time``
     - (13779,)
     - Sv
     - AABW >5000 m
   * - ``t_gs10``
     - ``time``
     - (13779,)
     - Sv
     - Florida Straits transport
   * - ``t_ek10``
     - ``time``
     - (13779,)
     - Sv
     - Ekman transport
   * - ``t_umo10``
     - ``time``
     - (13779,)
     - Sv
     - Upper Mid-Ocean transport
   * - ``moc_mar_hc10``
     - ``time``
     - (13779,)
     - Sv
     - Overturning transport MOC index

2d_gridded.nc
~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 35
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``time``
     - ``time``
     - (689,)
     - datetime
     - Time (10-day intervals)
   * - ``longitude``
     - ``longitude``
     - (254,)
     - degrees_east
     - Longitude coordinate
   * - ``depth``
     - ``depth``
     - (307,)
     - m
     - Depth coordinate
   * - ``CT``
     - ``time``, ``longitude``, ``depth``
     - (689, 254, 307)
     - °C
     - Conservative Temperature (ITS-90)
   * - ``SA``
     - ``time``, ``longitude``, ``depth``
     - (689, 254, 307)
     - g/kg
     - Absolute Salinity
   * - ``V_insitu``
     - ``time``, ``longitude``, ``depth``
     - (689, 254, 307)
     - m/s
     - Meridional velocity
   * - ``V_ekman``
     - ``time``, ``longitude``, ``depth``
     - (689, 254, 307)
     - m/s
     - Ekman velocity
   * - ``V_net``
     - ``time``
     - (689,)
     - m/s
     - Depth-integrated meridional velocity

meridional_transports.nc
~~~~~~~~~~~~~~~

.. list-table:: Variables
   :widths: 12 22 14 10 35
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``time``
     - ``time``
     - (689,)
     - datetime
     - Time (10-day intervals)
   * - ``depth``
     - ``depth``
     - (307,)
     - m
     - Depth coordinate
   * - ``sigma0``
     - ``sigma0``
     - (489,)
     - kg/m³ – 1000
     - Potential density anomaly (σ₀)
   * - ``amoc_depth``
     - ``time``
     - (689,)
     - Sv
     - Maximum overturning from depth-streamfunction
   * - ``amoc_sigma``
     - ``time``
     - (689,)
     - Sv
     - Maximum overturning from density-streamfunction
   * - ``heat_trans``
     - ``time``
     - (689,)
     - PW
     - Northward heat transport
   * - ``frwa_trans``
     - ``time``
     - (689,)
     - Sv
     - Northward freshwater transport
   * - ``press``
     - ``depth``
     - (307,)
     - dbar
     - Pressure coordinate
   * - ``stream_depth``
     - ``time``, ``depth``
     - (689, 307)
     - Sv
     - Overturning streamfunction in depth space
   * - ``stream_sigma``
     - ``time``, ``sigma0``
     - (689, 489?)
     - Sv
     - Overturning streamfunction in density space
