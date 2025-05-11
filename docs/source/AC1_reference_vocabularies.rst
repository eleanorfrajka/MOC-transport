
AC1 Reference vocabularies
==========================

This is an analysis of what vocabularies might be useful for the AC1 datasets.

A primary reference vocabulary is the "Climate and Forecast (CF) Standard Names" vocabulary, which is a controlled vocabulary for climate and forecast data. The CF standard names are used to describe the physical variables in the datasets.  See [http://vocab.nerc.ac.uk/standard_name/](http://vocab.nerc.ac.uk/standard_name/).

We also have the SeaDataNet Parameter Discovery Vocabulary, which is a controlled vocabulary for oceanographic parameters. The SeaDataNet vocabulary is used to describe the parameters in the datasets. See [http://vocab.nerc.ac.uk/collection/P02/current/](http://vocab.nerc.ac.uk/collection/P02/current/).

Temperature
-----------

**SeaDataNet Parameter Discovery Vocabulary (P02):**

- **Code:** TEMP — Temperature of the water column

- **URI:** https://vocab.nerc.ac.uk/collection/P02/current/TEMP/

- **Definition:** Includes temperature parameters at any depth in the water column (excluding the top few microns sampled by radiometers), encompassing both measured and calculated values like Conservative Temperature.


sea_water_conservative_temperature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** https://vocab.nerc.ac.uk/collection/P07/current/IFEDAFIE/

- **Label:** sea_water_conservative_temperature

- **Definition:** Conservative Temperature is defined as part of the Thermodynamic Equation of Seawater 2010 (TEOS-10), and represents specific potential enthalpy divided by a fixed heat capacity value. It is a more accurate proxy for ocean heat content than potential temperature.

**Notes:**

- Conservative Temperature is TEOS-10’s recommended replacement for potential temperature in climate-quality datasets.

- This variable is increasingly used in gridded ocean heat content products and climate model diagnostics.


sea_water_temperature
~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** https://vocab.nerc.ac.uk/collection/P07/current/CFSN0335/

- **Label:** sea_water_temperature

- **Definition:** The in situ temperature of sea water. This is the temperature a water parcel has at the location and depth of observation. To specify the depth, use a vertical coordinate variable.

**Notes:**

- `sea_water_temperature` is commonly used for directly measured CTD temperatures and numerical model outputs.

- It is distinct from potential temperature and Conservative Temperature, which are adjusted to a reference pressure.

- When using historical data, be mindful of the temperature scale (IPTS-68, ITS-90, etc.).

Salinity
--------

**SeaDataNet Parameter Discovery Vocabulary (P02):**

- **Code:** PSAL — Salinity of the water column

- **URI:** https://vocab.nerc.ac.uk/collection/P02/current/PSAL/

- **Definition:** Parameters quantifying the concentration of sodium chloride in any body of water at any point between the bed and the atmosphere

sea_water_absolute_salinity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/JIBGDIEJ/

- **Label:** sea_water_absolute_salinity

- **Definition:** Absolute Salinity, defined by TEOS-10, is the mass fraction of dissolved material in sea water. It is the salinity variable that yields the correct in situ density using the TEOS-10 equation of state, even when composition differs from the Reference Composition.

**Notes:**

- Often computed from Practical Salinity using regional climatologies of the Absolute Salinity Anomaly.

- Required for accurate density and heat content calculations under TEOS-10.

- Metadata should document the version of the TEOS-10 library and anomaly fields used.

sea_water_practical_salinity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/IADIHDIJ/

- **Label:** sea_water_practical_salinity

- **Definition:** Practical Salinity (S_P) is derived from conductivity measurements and expressed on the Practical Salinity Scale of 1978 (PSS-78). It is dimensionless and does not represent mass concentration.


**Notes:**

- This is the most commonly archived salinity value in observational datasets since 1978.

- Should not be used for pre-1978 datasets or when salinity is determined via chlorinity.

- Not suitable for thermodynamic calculations under TEOS-10; convert to Absolute Salinity for those applications.

sea_water_salinity
~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CFSN0331/

- **Label:** sea_water_salinity

- **Definition:** A general term for the salt content of sea water, not tied to a specific measurement scale (e.g., PSS-78). Use only when the salinity type is unknown or does not conform to a defined standard.

**Notes:**

- Use of this standard name is **discouraged** for post-1978 data when `sea_water_practical_salinity` is
applicable

- May appear in legacy datasets or when the methodology is uncertain.

- Always prefer more precise terms (`_practical_salinity`, `_absolute_salinity`, etc.) when possible.

Pressure
--------

sea_water_pressure
~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CFSN0330/

- **Label:** sea_water_pressure

- **Definition:** Total pressure in the seawater medium, including contributions from overlying seawater, sea ice, atmosphere, and any other overburden.


**Notes:**

- For pressure due to seawater only, use `sea_water_pressure_due_to_sea_water`.

- Canonical units are usually expressed in dbar.

- Commonly derived from pressure sensors or computed from depth.

sea_water_pressure_at_sea_floor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CF12N583/

- **Label:** sea_water_pressure_at_sea_floor

- **Definition:** The total pressure exerted at the seabed, including contributions from overlying seawater, ice, and atmosphere.


**Notes:**

- Frequently used in sea level and mass transport studies.

- May include inverted barometer corrections if adjusted post hoc.

- Expressed in dbar in most oceanographic datasets.

reference_pressure
~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/9334Z59K/

- **Label:** reference_pressure

- **Definition:** A constant scalar pressure value, typically representative of sea level pressure, used to define the reference state for potential density or temperature calculations.

**Notes:**

- Required as a scalar coordinate for CF-compliant representations of potential temperature or density.

- Units are typically in pascals (Pa), though oceanographic practice often uses dbar for physical interpretability.


Density
-------

**SeaDataNet Parameter Discovery Vocabulary (P02):**

- **Code:** DENS — Density of the water column

- **URI:** http://vocab.nerc.ac.uk/collection/P02/current/SIGT/

- **Definition:** Absolute determinations of water column density plus parameters (generally expressed as density anomaly) derived from temperature and salinity


sea_water_sigma_theta
~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CFSN0333/

- **Label:** sea_water_sigma_theta

- **Definition:** Potential density of sea water (density when moved adiabatically to a reference pressure), minus 1000 kg m⁻³. Commonly used to identify isopycnal surfaces. Reference pressure should be specified via a scalar coordinate with standard name `reference_pressure`.



**Notes:**

- The sigma-theta value is dimensionally equivalent to density minus 1000.

- Often used to stratify or bin hydrographic sections.

---

sea_water_potential_density
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CFSN0395/

- **Label:** sea_water_potential_density

- **Definition:** The density a seawater parcel would have if moved adiabatically to a reference pressure, usually sea level pressure. Reference pressure should be specified using a `reference_pressure` scalar coordinate.


**Notes:**

- Often used in thermohaline analyses and water mass classification.

- Subtract 1000 kg m⁻³ to obtain `sigma_theta`.

---

sea_water_neutral_density
~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/BBAH2105/

- **Label:** sea_water_neutral_density

- **Definition:** Neutral density is a variable whose surfaces approximately follow the direction of no buoyant motion. Designed to represent the neutral tangent plane slope more closely than potential density.


**Notes:**

- Especially useful for isopycnal transport diagnostics and water mass mixing studies.

- Refer to Jackett & McDougall (1997) for technical formulation.

ocean_sigma_coordinate
~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CFSN0473/

- **Label:** ocean_sigma_coordinate

- **Definition:** A parametric vertical coordinate used primarily in terrain-following ocean models. Not to be confused with `sea_water_sigma_theta`, which is a density-related scalar field.


**Notes:**

- Typically defined by formulas relating model levels to depth using pressure, surface elevation, and  bottom depth.

- See CF Conventions Appendix D for implementation details.

---

ocean_sigma_z_coordinate
~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/3HWMM33G/

- **Label:** ocean_sigma_z_coordinate

- **Definition:** A variant of the sigma coordinate system that adjusts for local stretching/compression in the vertical axis (z-star or z-level hybrid coordinates). See Appendix D of the CF convention for information about parametric vertical coordinates.



**Notes:**

- Particularly useful in hybrid coordinate systems and numerical ocean modeling.


Velocity
--------

**SeaDataNet Parameter Discovery Vocabulary (P02):**

- **Code:** RFVL — Horizontal velocity of the water column (currents)

- **URI:** https://vocab.nerc.ac.uk/collection/P02/current/RFVL/

- **Definition:** Parameters expressing the velocity (including scalar speeds and directions) of water column horizontal movement, commonly termed Eulerian currents


baroclinic_northward_sea_water_velocity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CFSN0729/

- **Label:** baroclinic_northward_sea_water_velocity

- **Definition:** The northward component of the baroclinic part of the sea water velocity field. "Baroclinic" refers to the component of motion associated with density gradients (excluding the depth-averaged flow).


**Notes:**

- Typically derived by subtracting the barotropic (depth-mean) velocity from the full velocity field.

- Used in dynamic studies of shear, stratification, and eddy activity.

---

barotropic_northward_sea_water_velocity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**

- **URI:** http://vocab.nerc.ac.uk/collection/P07/current/CFSN0731/

- **Label:** barotropic_northward_sea_water_velocity

- **Definition:** The northward component of the depth-averaged sea water velocity. "Barotropic" denotes the vertically uniform component of flow.


**Notes:**

- Common in analysis of large-scale circulation, especially transport estimates through straits and sections.

- Units are m s⁻¹ and typically gridded or averaged over large depth intervals.

Transport
---------

ocean_meridional_overturning_streamfunction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CF Standard Name (P07):**
- **URI:** https://vocab.nerc.ac.uk/collection/P07/current/CFSN0466/

- **Label:** ocean_meridional_overturning_streamfunction

- **Definition:** Meridional overturning streamfunction representing the net vertical and meridional circulation of the ocean, excluding the contribution from parameterized eddy velocities. This streamfunction is typically derived from the zonal integration of the meridional component of velocity.


**Notes:**
- Units are typically m³ s⁻¹.

- Often calculated from model output or observational sections like RAPID or OSNAP.

- Differentiates from `ocean_meridional_overturning_mass_streamfunction`, which includes all resolved and parameterized transport processes.

Freshwater Transport
--------------------

northward_ocean_freshwater_transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **CF Standard Name**: *northward_ocean_freshwater_transport*

- **CF URI**: [`CF standard name <http://vocab.nerc.ac.uk/standard_name/northward_ocean_freshwater_transport/>`_]

- **NERC P07**: [`CFSN0507 <http://vocab.nerc.ac.uk/collection/P07/current/CFSN0507/>`_]

- **SeaDataNet P01**: Not available

- **Other Notes**: Total northward transport of freshwater, incorporating all contributing components (e.g., overturning, gyre, eddies). Often computed from salinity and velocity fields, and expressed in Sverdrup equivalents adjusted for freshwater flux.




northward_ocean_freshwater_transport_due_to_overturning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **CF Standard Name**: *northward_ocean_freshwater_transport_due_to_overturning*

- **NERC P07**: [`CFSN0482 <http://vocab.nerc.ac.uk/collection/P07/current/CFSN0482/>`_]

- **SeaDataNet P01**: Not available

- **Other Notes**: Used in MOC decomposition to estimate the freshwater transport component associated with the overturning circulation. Expressed in Sverdrups or equivalent volume transport units adjusted for salinity.

northward_ocean_freshwater_transport_due_to_gyre
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **CF Standard Name**: *northward_ocean_freshwater_transport_due_to_gyre*

- **CF URI**: [`CF standard name <http://vocab.nerc.ac.uk/standard_name/northward_ocean_freshwater_transport_due_to_gyre/>`_]

- **NERC P07**: [`CFSN0510 <http://vocab.nerc.ac.uk/collection/P07/current/CFSN0510/>`_]

- **SeaDataNet P01**: Not available

- **Other Notes**: Component of northward freshwater transport attributed to horizontal (gyre-scale) circulation patterns. Derived from salinity and velocity anomalies relative to the zonal mean; complements overturning and eddy components.

