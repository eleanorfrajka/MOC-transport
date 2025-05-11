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


.. include:: format_orig_osnap.rst
.. include:: format_orig_rapid.rst
.. include:: format_orig_move.rst
.. include:: format_orig_samba.rst

.. _array-fw2015:

FW2015
-------

This is a different beast but similar to RAPID in that it has components which represent transport for different segments of the array (like Gulf Stream, Ekman and upper-mid-ocean) where these sum to produce MOC.  This is *vaguely* like OSNAP east and OSNAP west, except I don't think those sum to produce the total overturning.  And Ekman could be part of a layer transport but here is has no depth reference.  Gulf Stream has longitude bounds and a single latitude (``LATITUDE``, ``LONGITUDE_BOUND``) and limits over which the depths are represented (``DEPTH_BOUND``?) but no N_LEVELS.  It doesn't quite make sense to call the dimension N_PROF since these aren't profiles.  Maybe **N_COMPONENT**?


Summary of FW2015 files:
~~~~~~~~~~~~~~~~~~~~~~~~~~`
- ``MOCproxy_for_figshare_v1.mat``

  - ``TIME``: dimension ``TIME`` (264,), type datetime

  - ``MOC_PROXY``: dimension ``TIME``, units `Sv`

  - ``EK``: dimension ``TIME``, units `Sv`

  - ``GS``: dimension ``TIME``, units `Sv`

  - ``UMO_PROXY``: dimension ``TIME``, units `Sv`

Potential reformats:
~~~~~~~~~~~~~~~~~~~~~~~~~~`

- **Overturning:**

  - ``MOC``: time series (dimension: ``TIME``)

- **Component transports:**

  - Dimensions: ``TIME``, ``N_COMPONENT`` (1404, 7)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  ``N_COMPONENT`` for the number of components.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_COMPONENT``) -  This would also have ``TRANSPORT_NAME`` (``N_COMPONENT``, string) to indicate what the component is (e.g. `EK`, `GS`, `LNADW`, `MOC`, `MOC_PROXY`, `UMO_GRID`, `UMO_PROXY`, `UNADW_GRID`, etc).  Note that some of these were just copies of what the RAPID time series was at the time.





.. _array-mocha:

MOCHA
-----


Summary of MOCHA files:
~~~~~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~

So this might be suggested as a TEMPERATURE (``TIME``, ``N_LEVELS``) but unclear how to indicate that this is a zonal mean temperature as compared to the ones which are TEMPERATURE (``N_PROF``, ``TIME``, ``N_LEVELS``) for the full sections.


- **Heat Transport Components**:

  - `Q_eddy`, `Q_ek`, `Q_fc`, `Q_gyre`, `Q_int` → suggest ``MHT_COMPONENT`` (``N_COMPONENT``, ``TIME``)

  - Total: ``MHT`` (``TIME``)

- **Additional Variables**:

  - `T_basin`, `V_basin`, `T_fc_fwt`, etc.

  - These suggest basin-mean properties: ``TEMPERATURE`` (``TIME``, ``N_LEVELS``)

- **Note**: ``N_COMPONENT`` should indicate summable components if applicable


