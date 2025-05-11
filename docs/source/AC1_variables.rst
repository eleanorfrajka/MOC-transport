Variable Names
===============

There is no single universal standard that mandates variable names in an ``xarray.Dataset`` or CF conventions.  Therefore, the standard_name and vocabulary are critically important for interoperability.



**CMIP6 Variable Mapping by Category**

This table maps CF standard names to CMIP6 variable names, organized by category.
These short names are typically used in CMIP6 NetCDF output and should be matched to your xarray variables
via the `standard_name` attribute.

Temperature
-----------

+-----------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+
| CF Standard Name                              | CMIP6 Name     | Description                                          | MIP Table  | Dimensions                |
+===============================================+================+======================================================+============+===========================+
| sea_water_conservative_temperature            |                | Conservative temperature                             |            | (time, depth, lat, lon)   |
| sea_water_temperature                         |                | Sea water temperature                                |            | (time, depth, lat, lon)   |
| sea_water_potential_temperature               | thetao         | Sea water potential temperature                      | Omon       | (time, depth, lat, lon)   |
+-----------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+

Salinity
--------

+-----------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+
| CF Standard Name                              | CMIP6 Name     | Description                                          | MIP Table  | Dimensions                |
+===============================================+================+======================================================+============+===========================+
| sea_water_absolute_salinity                   |                | Absolute salinity (g/kg)                             |            | (time, depth, lat, lon)   |
| sea_water_practical_salinity                  | so             | Practical salinity                                   | Omon       | (time, depth, lat, lon)   |
| sea_water_salinity                            |                | General salinity (deprecated)                        |            | (time, depth, lat, lon)   |
+-----------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+

Pressure
--------

+------------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+
| CF Standard Name                               | CMIP6 Name     | Description                                          | MIP Table  | Dimensions                |
+================================================+================+======================================================+============+===========================+
| sea_water_pressure                             | pso            | Pressure                                             | Omon       | (time, depth, lat, lon)   |
| sea_water_pressure_at_sea_floor                |                | Pressure at sea floor                                | Omon       | (time, depth, lat, lon)   |
+------------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+

Density
-------

+------------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+
| CF Standard Name                               | CMIP6 Name     | Description                                          | MIP Table  | Dimensions                |
+================================================+================+======================================================+============+===========================+
| sea_water_sigma_theta                          | sigma0         | Density anomaly to 1000, surface reference           | Omon       | (time, depth, lat, lon)   |
| sea_water_potential_density                    |                | Same as sigma-theta                                  | Omon       | (time, depth, lat, lon)   |
| sea_water_neutral_density                      | gamma_n        | Neutral density estimate                             | Omon       | (time, depth, lat, lon)   |
| ocean_sigma_coordinate                         | —              | Vertical coordinate metadata                         | —          | —                         |
+------------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+

Velocity
--------

+----------------------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+
| CF Standard Name                                         | CMIP6 Name     | Description                                          | MIP Table  | Dimensions                |
+==========================================================+================+======================================================+============+===========================+
| baroclinic_northward_sea_water_velocity                  | votemper       | Baroclinic (layered) meridional velocity             | Omon       | (time, depth, lat, lon)   |
| bartropic_northward_sea_water_velocity                   | vbar           | Depth-averaged (barotropic) meridional velocity      | Omon       | (time, lat, lon)          |
+----------------------------------------------------------+----------------+------------------------------------------------------+------------+---------------------------+

Transport
---------

+------------------------------------------------------------------+--------------------------+----------------------------------------------------------+------------+---------------------------+
| CF Standard Name                                                 | CMIP6 Name               | Description                                              | MIP Table  | Dimensions                |
+==================================================================+==========================+==========================================================+============+===========================+
| northward_ocean_freshwater_transport                             | fwt_north                | Total freshwater transport                               | Omon       | (time, depth, lat, lon)   |
| northward_ocean_freshwater_transport_due_to_gyre                 | fwt_north_gyre           | Gyre component of freshwater transport                   | Omon       | (time, depth, lat, lon)   |
| northward_ocean_freshwater_transport_due_to_overturning          | fwt_north_ovt            | Overturning component of freshwater transport            | Omon       | (time, depth, lat, lon)   |
| northward_ocean_heat_tranpsport                                  | fht_north                | Total northward heat transport                           | Omon       | (time, depth, lat, lon)   |
| ocean_volume_transport_across_line                               | vol_transport            | Volume transport across a defined line or section        | Omon       | (time, depth, lat, lon)   |
| ocean_meridional_overturning_mass_streamfunction                 | moc                      | Overturning streamfunction (mass)                        | Omon       | (time, depth, lat)        |
| ocean_meridional_overturning_streamfunction                      | mosf                     | General overturning streamfunction                       | Omon       | (time, depth, lat)        |
+------------------------------------------------------------------+--------------------------+----------------------------------------------------------+------------+---------------------------+
