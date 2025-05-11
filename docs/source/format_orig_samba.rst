.. _array-samba:
SAMBA Original Data Format
----------------------

Note that the longer datasets (e.g., MOC_TotalAnomaly_and_constituents.asc) is from Meinen et al. (2018) and the shorter dataset (e.g., Upper_Abyssal_Transport_Anomalies.txt) is from Kersalé et al. (2020).

Upper_Abyssal_Transport_Anomalies.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Variables in Upper_Abyssal_Transport_Anomalies.txt
   :widths: 12 22 14 10 70
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``TIME``
     - ``TIME``
     - (1404,)
     - datetime
     -
       - **type**: datetime
   * - ``UPPER_TRANSPORT``
     - ``TIME``
     - (1404,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Upper-cell volume transport anomaly (relative to record-length average of 17.3 Sv)
   * - ``ABYSSAL_TRANSPORT``
     - ``TIME``
     - (1404,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Abyssal-cell volume transport anomaly (relative to record-length average of 7.8 Sv)


MOC_TotalAnomaly_and_constituents.asc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Variables in MOC_TotalAnomaly_and_constituents.asc
   :widths: 12 22 14 10 70
   :header-rows: 1

   * - Name
     - Dimensions
     - Shape
     - Units
     - Description
   * - ``TIME``
     - ``TIME``
     - (2964,)
     - datetime
     -
       - **type**: datetime
   * - ``MOC``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: MOC Total Anomaly (relative to record-length average of 14.7 Sv)
   * - ``RELATIVE_MOC``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Relative (density gradient) contribution
       - **description**: Relative (density gradient) contribution to MOC anomaly
   * - ``BAROTROPIC_MOC``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Reference (bottom pressure gradient) contribution to MOC anomaly
   * - ``EKMAN``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Ekman (wind) contribution to the MOC anomaly
   * - ``WESTERN_DENSITY``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Western density contribution to the MOC anomaly
   * - ``EASTERN_DENSITY``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Eastern density contribution to the MOC anomaly
   * - ``WESTERN_BOT_PRESSURE``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Western bottom pressure contribution to the MOC anomaly
   * - ``EASTERN_BOT_PRESSURE``
     - ``TIME``
     - (2964,)
     - Sv
     -
       - **standard_name**: ``Transport_anomaly``
       - **long_name**: Transport anomaly
       - **description**: Eastern bottom pressure contribution to the MOC anomaly
