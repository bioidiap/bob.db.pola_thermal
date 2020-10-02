.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Thu Apr 16 16:39:01 CEST 2015



.. image:: https://img.shields.io/badge/docs-available-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.pola_thermal/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.pola_thermal/badges/v1.0.5/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.pola_thermal/commits/v1.0.5
.. image:: https://gitlab.idiap.ch/bob/bob.db.pola_thermal/badges/v1.0.5/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.pola_thermal/commits/v1.0.5
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.pola_thermal


=============================
Polarimetric Thermal Database
=============================

This package contains the access API and descriptions for the `Polarimetric Thermal Database`.
The actual raw data for the database should be requested from US Army.
This package only contains the Bob accessor methods to use the DB directly from python, with the original protocol of the database.

The Polarimetrical Thermal Database is for research on VIS-Thermal face recognition.
It includes 60 identities faces captured in both VIS and Thermal.

  Hu, Shuowen, et al. "A Polarimetric Thermal Database for Face Recognition Research." Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshops. 2016.

Installation
------------

Follow our `installation`_ instructions. Then, to install this package, run::
   
   $ conda install bob.db.pola_thermal


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
