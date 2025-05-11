.. _convert-move:
MOVE conversion thoughts
----------------------

MOVE provides the TRANSPORT_TOTAL which corresponds to the MOC, but also things like transport_component_internal (``TIME``,), transport_component_internal_offset (``TIME``,), and transport_component_boundary (``TIME``,).  This would be similar to RAPID's version of "interior transport" and "western boundary wedge", but it's not so clear how to make these similarly named.

- **Notes**: Similar in structure to RAPID layer decomposition but naming is inconsistent between RAPID and MOVE.


Potential reformats:
~~~~~~~~~~~~~~~~~~~~~

- **Overturning:**
  - ``MOC``: time series (dimension: ``TIME``)

- **Component transports:**

  - Dimensions: ``TIME``, ``N_COMPONENT`` (13779, 3)

  - Coordinates: ``LATITUDE``, ``LONGITUDE_BOUNDS`` (scalar, x2), ``TIME`` in datetime.  ``N_COMPONENT`` for the number of components.

  - Variables: ``TRANSPORT`` (``TIME``, ``N_COMPONENT``) -  This would also have ``TRANSPORT_NAME`` (``N_COMPONENT``, string) to indicate what the component is (e.g. `transport_component_internal`, `transport_component_internal_offset`, `transport_component_boundary`, etc).
