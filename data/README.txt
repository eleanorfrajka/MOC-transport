# Title
Atlantic Meridional Overturning Circulation (AMOC) Heat Transport Time Series between April 2004 and December 2020 at 26.5°N

## Authors
- W.E. Johns<sup>1</sup> (https://orcid.org/0000-0002-1093-7871)
- S. Elipot<sup>1</sup> (https://orcid.org/0000-0001-6051-5426)
- D.A. Smeed<sup>2</sup> (https://orcid.org/0000-0003-1740-1778)
- B. Moat<sup>2</sup> (https://orcid.org/0000-0001-8676-7779)
- B. King<sup>2</sup> (https://orcid.org/0000-0003-1338-3234)
- D.L. Volkov<sup>3</sup> (https://orcid.org/0000-0002-9290-0502)
- R.H. Smith<sup>3</sup> (https://orcid.org/0000-0001-9824-6989)

### Affiliations
- <sup>1</sup> Rosenstiel School of Marine, Atmospheric, and Earth Science, University of Miami, Miami, Florida, USA
- <sup>2</sup> National Oceanography Centre, Southampton, United Kingdom
- <sup>3</sup> NOAA Atlantic Oceanographic and Meteorological Laboratory, Miami

## Corresponding author
William E. Johns <bjohns@earth.miami.edu> 

## Abstract
The RAPID-MOCHA-WBTS (RAPID-Meridional Overturning Circulation and Heatflux Array-Western Boundary Time Series) program has produced a continuous heat transport time series of the Atlantic Meridional Overturning Circulation (AMOC) at 26N that started in April 2004. This release of the heat transport time series covers the period from April 2004 to December 2020.The 26N AMOC time series is derived from measurements of temperature, salinity, pressure and water velocity from an array of moored instruments that extend from the east coast of the Bahamas to the continental shelf off Africa east of the Canary Islands. The AMOC heat transport calculation also uses estimates of the heat transport in the Florida Strait derived from sub-sea cable measurements calibrated by regular hydrographic cruises. The component of the AMOC associated with the wind driven Ekman layer is derived from ERA5 reanalysis. This release of the data includes a document with a brief description of the heat transport calculation of the AMOC time series and references to more detailed description in published papers. 

The 26N AMOC heat transport time series and the data from the moored array are curated by the Rosential School of Marine, Atmospheric and Earth Science at the University of Miami. The RAPID-MOCHA-WBTS program is a joint effort between the NSF (Principal Investigators Bill Johns and Shane Elipot, Uni. Miami) in the USA, NERC in the UK (PI Ben Moat, David Smeed, and Brian King, NOC) and NOAA (PIs Denis Volkov and Ryan Smith).

## Publication Date
2023

## DOI
https://doi.org/10.17604/3nfq-va20

## Description of the datasets
We provide a MAT-file and NetCDF file containing the dataset. The file mocha_mht_data_ERA5_v2020.nc comprises the heat transport results calculated for each component of AMOC from data obtained as part of the RAPID-MOCHA-WBTS array project. The resolution of the data is every 12 hours. All necessary metadata is included in the NetCDF data files. The MAT-file is identical to the NetCDF file, but without the metadata.

## Methodology/Supporting Information
Changes from the methodology used in Johns et al. (2011) are described in McCarthy et al. (2015), and updated as follows:
1. For this calculation we use ERA5 wind stress to calculate Ekman transports, instead of the previous ERA interim (ERA-I) winds which were converted to stress estimates via a bulk formula.
2. The Ekman heat transport is now calculated using these winds and the interior ocean temperature profiles derived from ARGO, where the Ekman transport is assumed to be confined to the upper 50m of the water column. Thus the Ekman layer temperature is a weighted average of the upper 50 m temperatures. Previously we had used Reynolds SST's in the interior and assumed the Ekman layer temperature to be equal to the Reynolds SST. Differences between the two methodologies are negligible.
3. The mid-ocean eddy heat flux Q_eddy is derived from an objective analysis of available Argo data profiles in the interior and T/S profiles from the RAPID moorings. Meridional velocity anomalies across the section are derived from this OA using a geostrophic approximation relative to 1000m. Previously, Q_eddy had been calculated from a "piecewise" mooring approach using only the mooring data across the section, as described in Johns et al. (2011). The two approaches agree within error bars and are consistent with the range of estimates available from trans-basin hydrographic sections along 26°N.
4. The interior zonal average temperature transport (Q_int) now uses a time varying interior temperature field derived from the Argo and mooring data as above, merged into a seasonal temperature climatology below 2000m based on the EN4 database. In Johns et al. (2011), the interior zonal mean temperature field was taken from only the seasonally varying RAPID HydroBase climatology.
5. The estimates of the temperature transport of the Florida Current now include an interannually-varying flow-weighted temperature (FWT) anomaly, in addition to the seasonal climatology of FWT used previously. Both the seasonal FWT of the Florida Current and its interannual anomaly are calculated from the 101 available synoptic sections across the Florida Current at 27°N collected by the NOAA WBTS program during the period of the RAPID observations (2004-2020). The climatological seasonal cycle of the Florida Current FWT is estimated as a two harmonic (annual and semiannual) fit of the section-derived FWT estimates, and the interannual anomaly of FWT is calculated as a running 3-year average of the FWT anomalies with respect to the climatological seasonal cycle

## Variables in mocha_mht_data_ERA5_v2020.nc file:
	- Q_eddy 	=  interior gyre component due to spatially correlated v'T' variability across the interior, derived from an objective analysis of interior ARGO T/S data merged with the mooring T/S data from moorings, and smoothly merged into the EN4 climatology along 26.5°N below 2000m (W)
	- Q_ek 	= Ekman heat transports (W)
	- Q_fc	= Florida Straits heat transports (W)
	- Q_gyre	= Basinwide gyre heat transports, as classically defined (e.g. see Johns et al., 2011) (W)
	- Q_int 	= Heat transport for the rest of the interior to Africa (but only represents the contribution by the zonal mean v and T) (W)
	- Q_mo 		= The sum of all the three interior components between the Bahamas and Africa (Q_int + Q_wedge + Q_eddy) (W)
	- Q_ot 	    = Basinwide overturning heat transports, as classically defined (e.g. see Johns et al., 2011) (W)
	- Q_sum	= Net meridional heat transport (W)
	- Q_wedge	= Heat transport for the "western boundary wedge" off Abaco (W)
	- T_basin	= time-varying basinwide mean potential temperature profile (degrees C)
	- T_basin_mean	= time-mean basinwide mean potential temperature profile (degrees C)
	- T_fc_fwt	= time-varying Florida Current flow-weighted potential temperature (degrees C)
	- V_basin	= time-varying basinwide mean transport profile (Sv/m)
	- V_basin_mean	= time-mean basinwide mean transport profile (Sv/m)
	- V_fc	= time-varying Florida Current transport profile (Sv/m)
	- V_fc_mean	= time-mean Florida Current transport profile (Sv/m)
	- trans_ek	= time-varying Ekman transport (Sv, calculated from ERA-I winds)
	- trans_fc	= time-varying Florida Current transport (Sv, from the cable)
	- maxmoc	= time-varying maximum value of MOC streamfunction (Sv)
	- moc	= time-varying MOC streamfunction vs. depth (Sv)
	- z	= the depth array that corresponds to the profile variables (m)
	- time	= seconds since 1970-1-1 00:00:00 UTC
	- julian_day	= julian days since 1950-1-1 00:00:00 UTC
	- year	= corresponding year of the measurements
	- month	= corresponding month of the measurements
	- day	= corresponding day of the measurements
	- hour	= corresponding hour of the measurements

	Note: The .nc file includes a series of attributes containing the metadata

## Variables in mocha_mht_data_ERA5_v2020.mat file:
	- Same as above

## Keywords:
Atlantic meridional overturning circulation, ocean transport, ocean circulation, heat transport, mesoscale ocean circulation

## Scientific discipline: 
ocean science, physical oceanography, ocean circulation

## License
Open Data Commons Attribution License (ODC-By) (https://opendatacommons.org/licenses/by/1-0/)

## Suggested citation
Johns W.E., Elipot S., Smeed D.A., Moat B., King B., Volkov D.L., Smith R.H., (2023). Atlantic Meridional Overturning Circulation (AMOC) Heat Transport Time Series between April 2004 and December 2020 at 26.5°N (v.2020) [Dataset]. University of Miami Libraries. https://doi.org/10.17604/3nfq-va20