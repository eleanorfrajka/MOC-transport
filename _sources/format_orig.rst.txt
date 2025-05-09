Array Format (Native / Original)
=================================

This document describes some of the native data formats present in AMOC datasets provided by different observing arrays.

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


Summary of RAPID files:
-----------------------

- ``moc_vertical.nc``:

  - ``depth``: dimension ``depth`` (307,), units `m`, type float64

  - ``time``: dimension ``time`` (13779,), type datetime

  - ``stream_function_mar``: (```depth``, ``time``), units `Sv`, type float64

- ``ts_gridded.nc``:

  - ```pressure```: dimension `depth` (242,), units `dbar`, type float64

  - ``time``: dimension `time` (13779,), type datetime

  - ``TG_west``: (`depth`, `time`), units `degC`, type float64, long name "Temperature west 26.52N/76.74W"

  - ``SG_wb3```: (`depth`, `time`), units `psu`, type float64, long name "Salinity WB3 26.50N/76.6W"

  - ``TG_marwest```: long name "Temperature MAR west 24.52N/50.57W"

  - ``TG_mareast``: long name "Temperature MAR east 24.52N/41.21W`

  - ``TG_east``: long name "Temperature east 26.99N/16.23W"

  - ``TG_west_flag``: (depth, time) with long name "Temperature west data FLAG" and units "data flag"

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


Potential reformats:
--------------------


- **Key Products**:

  - ``MOC``: time series (dimension: ``TIME``)

  - ``TEMPERATURE``, ``SALINITY``: gridded profiles (``TIME``, ``N_PROF``, ``N_LEVELS``), and specifying what version of temperature/salinity.

  - ``TEMPERATURE_FLAG``, ``SALINITY_FLAG``: (``TIME``, ``N_PROF``, ``N_LEVELS``),  With the attribute describing what the values mean

  - ?? ``TRANSPORT_LAYER``: e.g. `t_therm10`, `t_aiw10`... layered transports.  These are single time series, but there are several which could be bundled with an ``N_LEVELS`` dimension.

  - ?? ``TRANSPORT_COMPONENT``: e.g. `t_gs10`, `t_ek10`, `t_umo10`... these are also single time series, but could be bundled with an ``N_COMPONENT`` dimension.

- **Suggested Dimensions**:

  - ``TRANSPORT``: (``N_LEVELS``, ``TIME``)

  - ``LATITUDE``: (``N_PROF``,) Corresponding to the locations in the long name of e.g. `TG_west` or `SG_wb3`

  - ``LONGITUDE``: (``N_PROF``,) Corresponding to the locations in the long name of e.g. `TG_west` or `SG_wb3`

  - ``PRESSURE``: (``N_LEVELS``,)

  - ``DEPTH_BOUND``: (``N_LEVELS``, 2) - This ``N_LEVELS`` would not be the same as the ``N_LEVELS`` in the temperature/salinity profiles, but would be the depth bounds for the transport layers.

  - ``TRANSPORT_NAME``: (``N_LEVELS``, string)

.. _array-osnap:

OSNAP
~~~~~

At OSNAP, we have variables like MOC_ALL, MOC_EAST and MOC_WEST which are time series (``TIME``), but these could be represented as MOC (``N_PROF``, ``TIME``) where instead of the three different variables, N_PROF=3.  This would be somewhat more difficult to communicate to the user, since LATITUDE and LONGITUDE are not single points per N_PROF but instead may represent end points of a section.

Variables MOC_ALL_ERR are also provided, which could be translated to MOC_ERR (``N_PROF``, ``TIME``) with LATITUDE (``N_PROF``) or LATITUDE_BOUND (``N_PROF``, 2).

Heat fluxes also exist, as MHT_ALL, MHT_EAST and MHT_WEST, so these could be MHT (``N_PROF``, ``TIME``).



Summary of OSNAP files:
-----------------------



Potential reformats:
--------------------

- **Key Products**:

  - ``MOC_ALL``, ``MOC_EAST``, ``MOC_WEST``: time series (``TIME``)

  - Error estimates: ``MOC_ALL_ERR``

  - Heat flux: ``MHT_ALL``, ``MHT_EAST``, ``MHT_WEST``

- **Suggested Reformats**:

  - Collapse to: ``MOC`` (``N_PROF``, ``TIME``) where ``N_PROF``=3

  - ``LATITUDE_BOUND``: (``N_PROF``, 2) may be needed

  - ``MOC_ERR`` (``N_PROF``, ``TIME``)

.. _array-move:

MOVE
~~~~

MOVE provides the TRANSPORT_TOTAL which corresponds to the MOC, but also things like transport_component_internal (``TIME``,), transport_component_internal_offset (``TIME``,), and transport_component_boundary (``TIME``,).  This would be similar to RAPID's version of "interior transport" and "western boundary wedge", but it's not so clear how to make these similarly named.


Summary of MOVE files:
----------------------

- **Key Products**:

  - ``TRANSPORT_TOTAL``: equivalent to MOC (``TIME``,)

  - Component breakdown:

    - ``transport_component_internal``

    - ``transport_component_internal_offset``

    - ``transport_component_boundary``

- **Notes**: Similar in structure to RAPID layer decomposition but naming is inconsistent between RAPID and MOVE.


Potential reformats:
--------------------


.. _array-samba:

SAMBA
~~~~~

SAMBA (Upper_Abyssal_Transport_Anomalies.txt) has two main variables which are (``TIME``,), named 'upper-cell volume transport anomaly' which suggests a quantity TRANSPORT_ANOMALY (``N_LEVELS``, ``TIME``), where we would then have again a DEPTH_BOUND (``N_LEVELS``, 2).

But the other SAMBA product (MOC_TotalAnomaly_and_constituents.asc) also has a "Total MOC anomaly" (``MOC``), a "Relative (density gradient) contribution" which is like MOVE's internal or RAPID's interior.  There is a "Reference (bottom pressure gradient) contribution" which is like MOVE's offset or RAPID's compensation.  An Ekman (all have this--will need an attribute with the source of the wind fields used), and also a separate **"Western density contribution"** and **"Eastern density contribution"** which are not available in the RAPID project, and are not the same idea as the OSNAP west and OSNAP east, but could suggest an (``N_PROF``=2, ``TIME``) for west and east.

Summary of MOVE files:
----------------------



Potential reformats:
--------------------

- **Files**:

  - `Upper_Abyssal_Transport_Anomalies.txt`

    - ``TRANSPORT_ANOMALY`` (``N_LEVELS``, ``TIME``)`

    - ``DEPTH_BOUND`` (``N_LEVELS``, 2)

  - `MOC_TotalAnomaly_and_constituents.asc`

    - ``MOC``, ``Relative...``, ``Reference...``, ``Ekman...``, ``Western...``, ``Eastern...``

- **Suggested Dimensions**:

  - ``MOC_COMPONENT`` (``N_PROF``=2, ``TIME``) for East/West

  - Include metadata for Ekman wind source

.. _array-fw2015:





FW2015
~~~~~~

This is a different beast but similar to RAPID in that it has components which represent transport for different segments of the array (like Gulf Stream, Ekman and upper-mid-ocean) where these sum to produce MOC.  This is *vaguely* like OSNAP east and OSNAP west, except I don't think those sum to produce the total overturning.  And Ekman could be part of a layer transport but here is has no depth reference.  Gulf Stream has longitude bounds and a single latitude (``LATITUDE``, ``LONGITUDE_BOUND``) and limits over which the depths are represented (``DEPTH_BOUND``?) but no N_LEVELS.  It doesn't quite make sense to call the dimension N_PROF since these aren't profiles.  Maybe **N_COMPONENT**?


Summary of FW2015 files:
------------------------


Potential reformats:
--------------------

- **Overview**: Like RAPID but decomposed into components such as Gulf Stream, Ekman, and Upper Mid-Ocean

- **Dimensions**:

  - Possibly ``N_COMPONENT`` instead of ``N_PROF``

  - ``LATITUDE``, ``LONGITUDE_BOUND``, and ``DEPTH_BOUND`` may be relevant

- **Note**: Components sum to MOC unlike OSNAP_EAST/WEST




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


