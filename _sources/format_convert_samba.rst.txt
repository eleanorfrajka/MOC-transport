.. _convert-samba:
SAMBA conversion thoughts
----------------------

SAMBA (Upper_Abyssal_Transport_Anomalies.txt) has two main variables which are (``TIME``,), named 'upper-cell volume transport anomaly' which suggests a quantity TRANSPORT_ANOMALY (``N_LEVELS``, ``TIME``), where we would then have again a DEPTH_BOUND (``N_LEVELS``, 2).

But the other SAMBA product (MOC_TotalAnomaly_and_constituents.asc) also has a "Total MOC anomaly" (``MOC``), a "Relative (density gradient) contribution" which is like MOVE's internal or RAPID's interior.  There is a "Reference (bottom pressure gradient) contribution" which is like MOVE's offset or RAPID's compensation.  An Ekman (all have this--will need an attribute with the source of the wind fields used), and also a separate **"Western density contribution"** and **"Eastern density contribution"** which are not available in the RAPID project, and are not the same idea as the OSNAP west and OSNAP east, but could suggest an (``N_PROF``=2, ``TIME``) for west and east.



Potential reformats:
~~~~~~~~~~~~~~~~~~~~~

- **Overturning:**

  - ``MOC``: time series (dimension: ``TIME``)

**Note:** Check the readme to see what the relationship is between the upper, abyssal and MOC transports.


- **Component transports:**

  - Dimensions: ``TIME``, ``N_COMPONENT`` (1404, 7)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  ``N_COMPONENT`` for the number of components.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_COMPONENT``) -  This would also have ``TRANSPORT_NAME`` (``N_COMPONENT``, string) to indicate what the component is (e.g. `RELATIVE_MOC`, `BAROTROPIC_MOC`, `EKMAN`, `WESTERN_DENSITY`, etc).

**Note:** It would be good to verify how these components should (or shouldn't) add up to the total transports.
