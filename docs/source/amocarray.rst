:mod:`amocarray API`
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   readers
   read_move
   read_rapid
   read_osnap
   read_samba
   plotters
   writers
   tools
   standardise
   utilities

Load and process transport estimates from major AMOC observing arrays.

readers
=======

Shared utilities and base classes for AMOC readers.

.. automodule:: amocarray.readers
   :members:
   :undoc-members:

Submodules
^^^^^^^^^^

read_rapid
~~~~~~~~~~
Reader for RAPID-MOCHA-WBTS array data at 26°N.

.. automodule:: amocarray.read_rapid
   :members:
   :undoc-members:

read_osnap
~~~~~~~~~~
Reader for OSNAP (Overturning in the Subpolar North Atlantic Program) data.

.. automodule:: amocarray.read_osnap
   :members:
   :undoc-members:

read_move
~~~~~~~~~
Reader for MOVE (Meridional Overturning Variability Experiment) data.

.. automodule:: amocarray.read_move
   :members:
   :undoc-members:

read_samba
~~~~~~~~~~
Reader for SAMBA (South Atlantic MOC Basin-wide Array) data.

.. automodule:: amocarray.read_samba
   :members:
   :undoc-members:

standardise
===========
Functions to apply naming conventions, units, and metadata standards to datasets.

.. automodule:: amocarray.standardise
   :members:
   :undoc-members:

plotters
========
Tools for visualising AMOC time series and transport data.

.. automodule:: amocarray.plotters
   :members:
   :undoc-members:

writers
=======
.. automodule:: amocarray.writers
   :members:
   :undoc-members:

tools
=====
Helper functions for data manipulation, unit conversion, and clean-up.

.. automodule:: amocarray.tools
   :members:
   :undoc-members:

utilities
=========
Shared utilities for downloading, reading, and parsing data files.

.. automodule:: amocarray.utilities
   :members:
   :undoc-members:
