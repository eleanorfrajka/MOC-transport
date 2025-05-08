AMOCarray Format AC1 – RST
=================================

This document defines the AC1 standard data format produced by the ``amocarray.convert.to_AC1()`` function.
The AC1 format provides a unified, interoperable structure for mooring array datasets such as MOVE, RAPID, OSNAP, and SAMBA.

1. Overview
-----------

The AC1 format ensures consistency, metadata clarity, and long-term interoperability for Atlantic Meridional Overturning Circulation (AMOC) mooring array datasets. It is based on ``xarray.Dataset`` objects, compatible with NetCDF4, and adheres to CF conventions where applicable.

0. Background
-------------

Individual observing arrays produce data in various formats.

RAPID
~~~~~

For example, at 26°N, the RAPID array produces an AMOC transport time series (volume transport in depth space) which is a 1-dimensional time series with a single registered latitude (26.5) and no registered longitude.  It also provides profiles of temperature, salinity and dynamic height representing individual locations (single latitude, single nominal longitude) on a vertical grid of 20 dbar.  Several locations are provided, with names like WB, MAR_WEST, MAR_EAST, EB.  So there are N_PROF locations, with N_LEVELS and also TIME as dimensions. And the LATITUDE would be N_PROF (a small number, like 4, representing mooring locations)

More recently, they have started providing a section of temperature, saliity and velocity which are then N_PROF, TIME and N_LEVELS, but now the N_PROF (and both LONGITUDE and LATITUDE) would be on a regular grid--or at least with more locations (longer N_PROF), though it's possible LATITUDE would be a single latitude (26.5).

RAPID also provides layer transports which are single time series with names like t_therm10, t_aiw10, t_ud10, t_ld10, etc, which are between specified depth ranges.  These could be simply: TRANSPORT (N_LEVELS, TIME) with DEPTH_BOUND (N_LEVELS, 2) to give an upper and lower bound on the depths used to produce transport in layers?  It would also need something like TRANSPORT_NAME (N_LEVELS) of type string.

OSNAP
~~~~~

At OSNAP, we have variables like MOC_ALL, MOC_EAST and MOC_WEST which are time series (TIME), but these could be represented as MOC (N_PROF, TIME) where instead of the three different variables, N_PROF=3.  This would be somewhat more difficult to communicate to the user, since LATITUDE and LONGITUDE are not single points per N_PROF but instead may represent end points of a section.

Variables MOC_ALL_ERR are also provided, which could be translated to MOC_ERR (N_PROF, TIME) with LATITUDE (N_PROF) or LATITUDE_BOUND (N_PROF, 2).

Heat fluxes also exist, as MHT_ALL, MHT_EAST and MHT_WEST, so these could be MHT (N_PROF, TIME).

MOVE
~~~~

MOVE provides the TRANSPORT_TOTAL which corresponds to the MOC, but also things like transport_component_internal (TIME,), transport_component_internal_offset (TIME,), and transport_component_boundary (TIME,).  This would be similar to RAPID's version of "interior transport" and "western boundary wedge", but it's not so clear how to make these similarly named.


SAMBA
~~~~~

SAMBA (Upper_Abyssal_Transport_Anomalies.txt) has two main variables which are (TIME,), named 'upper-cell volume transport anomaly' which suggests a quantity TRANSPORT_ANOMALY (N_LEVELS, TIME), where we would then have again a DEPTH_BOUND (N_LEVELS, 2).

But the other SAMBA product (MOC_TotalAnomaly_and_constituents.asc) also has a "Total MOC anomaly" (MOC), a "Relative (density gradient) contribution" which is like MOVE's internal or RAPID's interior.  There is a "Reference (bottom pressure gradient) contribution" which is like MOVE's offset or RAPID's compensation.  An Ekman (all have this--will need an attribute with the source of the wind fields used), and also a separate **"Western density contribution"** and **"Eastern density contribution"** which are not available in the RAPID project, and are not the same idea as the OSNAP west and OSNAP east, but could suggest an (N_PROF=2, TIME) for west and east.

FW2015
~~~~~~

This is a different beast but similar to RAPID in that it has components which represent transport for different segments of the array (like Gulf Stream, Ekman and upper-mid-ocean) where these sum to produce MOC.  This is *vaguely* like OSNAP east and OSNAP west, except I don't think those sum to produce the total overturning.  And Ekman could be part of a layer transport but here is has no depth reference.  Gulf Stream has longitude bounds and a single latitude (LATITUDE, LONGITUDE_BOUND) and limits over which the depths are represented (DEPTH_BOUND?) but no N_LEVELS.  It doesn't quite make sense to call the dimension N_PROF since these aren't profiles.  Maybe **N_COMPONENT**?

MOCHA
~~~~~

The heat transports at RAPID-MOCHA are provided with N_LEVELS, TIME, and variables:
- Q_eddy
- Q_ek
- Q_fc
- Q_gyre
- Q_int.
Again, we have a situation where N_PROF isn't really appropriate.  &**N_COMPONENT**?  WE should double check that things called **N_COMPONENT** then somehow sum to produce a total?  Then we would have something like MHT_COMPONENT (N_COMPONENT, TIME) and MHT (TIME)

But we also have things like:
- T_basin (TIME, N_LEVELS)
- T_basin_mean (N_LEVELS)
- T_fc_fwt (TIME)
- V_basin (TIME, N_LEVELS) --> is this identical to new RAPID velo sxn?
- V_basin_mean (N_LEVELS)
- V_fc (TIME, N_LEVELS)
So this might be suggested as a TEMPERATURE (TIME, N_LEVELS) but unclear how to indicate that this is a zonal mean temperature as compared to the ones which are TEMPERATURE (N_PROF, TIME, N_LEVELS) for the full sections.

2. File Format
--------------

- **File type**: NetCDF4
- **Data structure**: ``xarray.Dataset``
- **Dimensions**:
  - ``TIME`` (required)
  - ``DEPTH`` (optional)
  - ``LATITUDE``, ``LONGITUDE`` (optional, where applicable)
- **Encoding**:
  - Default: ``float32`` for data variables
  - Compression: Enabled if saved to NetCDF
  - Chunking: Optional, recommended for large datasets

3. Variables
------------

.. list-table:: Variables.  The requirement status (RS) is shown in the last column, where **M** is mandatory, *HD* is highly desirable, and *S* is suggested.
   :widths: 20 25 20 20 5
   :header-rows: 1

   * - Name
     - Dimensions
     - Units
     - Description
     - RS
   * - TIME
     - (TIME,)
     - seconds since 1970-01-01
     - Timestamps in UTC
     - **M**
   * - LONGITUDE
     - scalar or array
     - degrees_east
     - Mooring or array longitude
     - S
   * - LATITUDE
     - scalar or array
     - degrees_north
     - Mooring or array latitude
     - S
   * - DEPTH
     - optional
     - m
     - Depth levels if applicable
     - S
   * - TEMPERATURE
     - (TIME, ...)
     - degree_Celsius
     - In situ or potential temperature
     - S
   * - SALINITY
     - (TIME, ...)
     - psu
     - Practical or absolute salinity
     - S
   * - TRANSPORT
     - (TIME,)
     - Sv
     - Overturning transport estimate
     - S

4. Global Attributes
--------------------

.. list-table:: Global Attributes
   :widths: 20 20 25 5
   :header-rows: 1

   * - Attribute
     - Example
     - Description
     - RS
   * - title
     - "RAPID-MOCHA Transport Time Series"
     - Descriptive dataset title
     - **M**
   * - platform
     - "moorings"
     - Type of platform
     - **M**
   * - platform_vocabulary
     - "https://vocab.nerc.ac.uk/collection/L06/current/"
     - Controlled vocab for platform types
     - **M**
   * - featureType
     - "timeSeries"
     - NetCDF featureType
     - **M**
   * - id
     - "RAPID_20231231_<orig>.nc"
     - Unique file identifier
     - **M**
   * - contributor_name
     - "Dr. Jane Doe"
     - Name of dataset PI
     - **M**
   * - contributor_email
     - "jane.doe@example.org"
     - Email of dataset PI
     - **M**
   * - contributor_id
     - "ORCID:0000-0002-1825-0097"
     - Identifier (e.g., ORCID)
     - HD
   * - contributor_role
     - "principalInvestigator"
     - Role using controlled vocab
     - **M**
   * - contributor_role_vocabulary
     - "http://vocab.nerc.ac.uk/search_nvs/W08/"
     - Role vocab reference
     - **M**
   * - contributing_institutions
     - "University of Hamburg"
     - Responsible org(s)
     - **M**
   * - contributing_institutions_vocabulary
     - "https://ror.org/012tb2g32"
     - Institutional ID vocab (e.g. ROR, EDMO)
     - HD
   * - contributing_institutions_role
     - "operator"
     - Role of institution
     - **M**
   * - contributing_institutions_role_vocabulary
     - "https://vocab.nerc.ac.uk/collection/W08/current/"
     - Vocabulary for institution roles
     - **M**
   * - source_acknowledgement
     - "...text..."
     - Attribution to original dataset providers
     - **M**
   * - source_doi
     - "https://doi.org/..."
     - Semicolon-separated DOIs of original datasets
     - **M**
   * - amocarray_version
     - "0.2.1"
     - Version of amocarray used
     - **M**
   * - web_link
     - "http://project.example.org"
     - Semicolon-separated URLs for more information
     - S
   * - start_date
     - "20230301T000000"
     - Overall dataset start time (UTC)
     - **M**
   * - date_created
     - "20240419T130000"
     - File creation time (UTC, zero-filled as needed)
     - **M**

5. Variable Attributes
----------------------

.. list-table:: Variable Attributes
   :widths: 20 60 5
   :header-rows: 1

   * - Attribute
     - Description
     - RS
   * - long_name
     - Descriptive name of the variable
     - **M**
   * - standard_name
     - CF-compliant standard name (if available)
     - **M**
   * - vocabulary
     - Controlled vocabulary identifier
     - HD
   * - _FillValue
     - Fill value, same dtype as variable
     - **M**
   * - units
     - Physical units (e.g., m/s, degree_Celsius)
     - **M**
   * - coordinates
     - Comma-separated coordinate list (e.g., "TIME, DEPTH")
     - **M**

6. Metadata Requirements
------------------------

Metadata are provided as YAML files for each array. These define variable mappings, unit conversions, and attributes to attach during standardisation.

Example YAML (osnap_array.yml):

.. code-block:: yaml

   variables:
     temp:
       name: TEMPERATURE
       units: degree_Celsius
       long_name: In situ temperature
       standard_name: sea_water_temperature

     sal:
       name: SALINITY
       units: g/kg
       long_name: Practical salinity
       standard_name: sea_water_practical_salinity

     uvel:
       name: U
       units: m/s
       long_name: Zonal velocity
       standard_name: eastward_sea_water_velocity

7. Validation Rules
-------------------

- All datasets must include the TIME coordinate.
- At least one of: TEMPERATURE, SALINITY, TRANSPORT, U, V must be present.
- Global attribute array_name must match one of: ["move", "rapid", "osnap", "samba"].
- File must pass CF-check where possible.

8. Examples
-----------

YAML input: see metadata/osnap_array.yml

Resulting NetCDF Header (excerpt):

.. code-block:: text

   dimensions:
       TIME = 384
       DEPTH = 4

   variables:
       float32 TEMPERATURE(TIME, DEPTH)
           long_name = "In situ temperature"
           standard_name = "sea_water_temperature"
           units = "degree_Celsius"
       ...

   global attributes:
       :title = "OSNAP Array Transport Data"
       :institution = "AWI / University of Hamburg"
       :array_name = "osnap"
       :Conventions = "CF-1.8"

9. Conversion Tool
------------------

To produce AC1-compliant datasets from raw standardised inputs, use:

.. code-block:: python

   from amocarray.convert import to_AC1
   ds_ac1 = to_AC1(ds_std)

This function:

- Validates standardised input
- Adds metadata from YAML
- Ensures output complies with AC1 format

10. Notes
---------

- Format is extensible for future variables or conventions
- Please cite amocarray and relevant data providers when using AC1-formatted datasets

11. Provenance and Attribution
------------------------------

To ensure transparency and appropriate credit to original data providers, the AC1 format includes structured global attributes for data provenance.

Required Provenance Fields:

.. list-table::
   :widths: 30 60
   :header-rows: 1

   * - Attribute
     - Purpose
   * - source
     - Semicolon-separated list of original dataset short names
   * - source_doi
     - Semicolon-separated list of DOIs for original data
   * - source_acknowledgement
     - Semicolon-separated list of attribution statements
   * - history
     - Auto-generated history log with timestamp and tool version
   * - amocarray_version
     - Version of amocarray used for conversion
   * - generated_doi
     - DOI assigned to the converted AC1 dataset (optional)

Example:

.. code-block:: text

   :source = "OSNAP; SAMBA"
   :source_doi = "https://doi.org/10.35090/gatech/70342; https://doi.org/10.1029/2018GL077408"
   :source_acknowledgement = "OSNAP data were collected and made freely available by the OSNAP project and all the national programs that contribute to it (www.o-snap.org); M. Kersalé et al., Highly variable upper and abyssal overturning cells in the South Atlantic. Sci. Adv. 6, eaba7573 (2020). DOI: 10.1126/sciadv.aba7573"
   :history = "2025-04-19T13:42Z: Converted to AC1 using amocarray v0.2.1"
   :amocarray_version = "0.2.1"
   :generated_doi = "https://doi.org/10.xxxx/amocarray-ac1-2025"

YAML Integration (optional):

.. code-block:: yaml

   metadata:
     citation:
       doi: "https://doi.org/10.1029/2018GL077408"
       acknowledgement: >
         M. Kersalé et al., Highly variable upper and abyssal overturning cells in the South Atlantic.
         Sci. Adv. 6, eaba7573 (2020). DOI: 10.1126/sciadv.aba7573
