
CF Standard Names
=================

This document summarizes selected CF standard names used in the AC1 dataset for describing seawater properties and meridional transports.

------------------------------------------------------------------

Coordinates
-----------


latitude
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** degree_north

**Description:**
Latitude is positive northward. In rotated grids, use `grid_latitude` instead.

------------------------------------------------------------------

longitude
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** degree_east

**Description:**
Longitude is positive eastward. In rotated grids, use `grid_longitude` instead.

------------------------------------------------------------------



Temperature
-----------

sea_water_conservative_temperature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Canonical Units:** K

**Description:**
Conservative Temperature is defined as part of the Thermodynamic Equation of Seawater 2010 (TEOS-10), adopted in 2010 by the International Oceanographic Commission (IOC). It is specific potential enthalpy (see `sea_water_specific_potential_enthalpy`) divided by a fixed value of the specific heat capacity of sea water:

.. math::

   C_T = h^0 / c_{p0}, \quad 	ext{where } c_{p0} = 3991.86795711963 	ext{ J kg⁻¹ K⁻¹}

Conservative Temperature is a significantly more accurate measure of seawater heat content than potential temperature (θ), improving precision by a factor of ~100. It is proportional to the heat content per unit mass of seawater.

**References:**
- TEOS-10: https://www.teos-10.org
- McDougall, 2003: doi:10.1175/1520-0485(2003)033<0945:PEACOV>2.0.CO;2

**Metadata Guidance:**
Strongly recommended to include a `units_metadata` attribute: `"on-scale"` or `"difference"`.

------------------------------------------------------------------

sea_water_temperature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** K

**Description:**
Sea water temperature refers to the *in situ* temperature of seawater. Use a vertical coordinate to specify measurement depth.

**Historical Context:**
- IPTS-48 (1948–1967)
- IPTS-68 (1968–1989)
- ITS-90 (1990 onward)

**Conversion Equations:**

.. math::

   t_{68} = t_{48} - 4.4 	imes 10^{-6} \cdot t_{48} \cdot (100 - t_{48}) \
   t_{90} = 0.99976 \cdot t_{68}

**Metadata Guidance:**
Use `units_metadata`: `"on-scale"` or `"difference"`.

------------------------------------------------------------------


Salinity
-----------

sea_water_absolute_salinity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** g kg⁻¹

**Description:**
Absolute Salinity \( S_A \), from TEOS-10, is the mass fraction of dissolved material in seawater. It accounts for regional composition variations and yields accurate density calculations.

**Metadata Guidance:**
Include a `comment` attribute specifying the TEOS-10 software version and anomaly climatology.

**References:**
- TEOS-10: https://www.teos-10.org
- Millero et al., 2008: doi:10.1016/j.dsr.2007.10.001

------------------------------------------------------------------

sea_water_practical_salinity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** 1 (dimensionless)

**Description:**
Practical Salinity \( S_P \) is computed from conductivity and is reported on the Practical Salinity Scale of 1978 (PSS-78). Use only for post-1978 data derived from conductivity.

**References:**
- TEOS-10: https://www.teos-10.org
- Lewis, 1980: doi:10.1109/JOE.1980.1145448

------------------------------------------------------------------

sea_water_salinity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** 1e-3 (dimensionless; parts per thousand)

**Description:**
Generic term for salt content in seawater. Use only when the salinity does not conform to a defined standard. Deprecated for post-1978 observations in favor of `sea_water_practical_salinity`.

**Conversion Notes:**


.. math::

   S_P = (S_K - 0.03) \times \left( \frac{1.80655}{1.805} \right)

.. math::

   S_P = S_C

------------------------------------------------------------------


Pressure
--------

sea_water_pressure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** dbar

**Description:**
Sea water pressure includes the pressure from the overlying seawater, sea ice, atmosphere, and other media. Use `sea_water_pressure_due_to_sea_water` to isolate seawater-only pressure.

------------------------------------------------------------------


sea_water_pressure_at_sea_floor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** dbar

**Description:**
Pressure at the ocean bottom, including contributions from all overlying media.

------------------------------------------------------------------

reference_pressure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** Pa

**Description:**
A constant scalar value representing reference pressure (e.g., for calculating potential density).

------------------------------------------------------------------


Density
-------
sea_water_sigma_theta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** kg m⁻³

**Description:**
Sigma-theta of sea water is the potential density (i.e. the density when moved adiabatically to a reference pressure) minus 1000 kg m⁻³. To specify the reference pressure, include a scalar coordinate variable with standard name `reference_pressure`. Not to be confused with `ocean_sigma_coordinate`.

------------------------------------------------------------------

ocean_sigma_z_coordinate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** 1 (dimensionless)

**Description:**
A parametric vertical coordinate. See Appendix D of the CF convention for details.

------------------------------------------------------------------

ocean_sigma_coordinate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** 1 (dimensionless)

**Description:**
A parametric vertical coordinate used in ocean models. Not to be confused with `sea_water_sigma_theta`.

------------------------------------------------------------------

sea_water_potential_density
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** kg m⁻³

**Description:**
The density a parcel of sea water would have if moved adiabatically to a reference pressure (typically sea level). Use `reference_pressure` as a scalar coordinate. Subtracting 1000 kg m⁻³ yields `sea_water_sigma_theta`.

------------------------------------------------------------------

sea_water_neutral_density
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** kg m⁻³

**Description:**
Neutral density is a variable that approximates the local slope of the neutral tangent plane. Differences between neutral density and potential density anomaly can be substantial away from the equator. See Jackett & McDougall (1997) for details.


Velocity
--------




baroclinic_northward_sea_water_velocity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** m s⁻¹

**Description:**
Northward component of baroclinic sea water velocity.

------------------------------------------------------------------

barotropic_northward_sea_water_velocity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** m s⁻¹

**Description:**
Northward component of barotropic sea water velocity.


Transport
--------

northward_ocean_freshwater_transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** kg s⁻¹

**Description:**
Northward component of total ocean freshwater transport, including both seawater and sea ice.

------------------------------------------------------------------

northward_ocean_freshwater_transport_due_to_gyre
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Canonical Units:** kg s⁻¹

**Description:**
Part of northward freshwater transport due to ocean gyre circulation, calculated from deviations from zonal means. Excludes parameterized eddy velocity.

------------------------------------------------------------------

northward_ocean_freshwater_transport_due_to_overturning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Canonical Units:** kg s⁻¹

**Description:**
Part of northward freshwater transport due to overturning circulation, based on zonal means. Excludes parameterized eddy velocity.

------------------------------------------------------------------

northward_ocean_heat_transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Canonical Units:** W

**Description:**
Northward component of total ocean heat transport, including seawater and sea ice.

------------------------------------------------------------------

northward_ocean_heat_transport_due_to_gyre
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Canonical Units:** W

**Description:**
Part of northward heat transport due to ocean gyre circulation, using deviations from zonal means. Excludes parameterized eddy velocity.

------------------------------------------------------------------

northward_ocean_heat_transport_due_to_overturning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Canonical Units:** W

**Description:**
Part of northward heat transport due to overturning circulation, based on zonal means. Excludes parameterized eddy velocity.

------------------------------------------------------------------

ocean_volume_transport_across_line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** m³ s⁻¹

**Description:**
Transport across a specified line (e.g., latitude), defined as the line integral of normal volume transport across that section.

------------------------------------------------------------------

streamfunction
----------------

ocean_meridional_overturning_mass_streamfunction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Canonical Units:** kg s⁻¹

**Description:**
Overturning streamfunction including all resolved and parameterized processes that impact mass or volume transport.

------------------------------------------------------------------

ocean_meridional_overturning_streamfunction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Canonical Units:** m³ s⁻¹

**Description:**
Overturning streamfunction excluding the parameterized eddy velocity.



------------------------------------------------------------------



