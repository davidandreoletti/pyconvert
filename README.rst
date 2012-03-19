pyconvert

ABOUT
=====

pyconvert is a pure Python application for converting files with my OWN storage requirements (mainly to save disk space).

MOTIVATION:
===========

Save disk space

INSTALLATION:
=============

Installation for end user:
---------------------------

Step: Download sources

``curl -L https://github.com/davidandreoletti/pyconvert/tarball/v0.0.1 2>/dev/null > sources.tar.gz``

``mkdir pyconvert-0.0.1; tar -C pyconvert-0.0.1 --strip-components 1 -xzvf sources.tar.gz``

``cd pyconvert-0.0.1``

Step: Install dependencies

``python setup.py install``

Step: Build application

``./make.sh``

Step: Run application

``./pyconvert-app -h``

Installation for developer:
---------------------------

Step: Checkout project source and move into project directory

``git clone git://github.com/davidandreoletti/pyconvert.git; cd pyconvert``

Step: Install project for development

``python setup.py develop``

Step: Run application

``python main.py -h``

DONE :)


DOCUMENTATION
=============

Documentation is PEP257_ compliant. Hence you will find documentation in python files themselves.

SOURCE
======

Main source repository: https://github.com/davidandreoletti/pyconvert

DEVELOPMENT STATUS
==================

This implementation is in ALPHA version. I only implements features required by my own needs but feel free to extend it.

REQUIREMENTS
============

Developed with Python 2.7.1+. 
Successfully tested on Ubuntu 11.04 with Python 2.7.1+ only.
Handbrake_, FFMPEG_ and ImageMagick_.

CONTRIBUTORS:
=============

I don't expect any contributor for this project but if you would like to contribute, please follow PEP8_.

AUTHOR
======

David Andreoletti <http://davidandreoletti.com> - Original author

.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _PEP257: http://www.python.org/dev/peps/pep-0257/
.. _Handbrake: https://trac.handbrake.fr/wiki/CLIGuide
.. _ImageMagick: http://www.imagemagick.org/script/index.php
.. _FFMPEG: http://ffmpeg.org/ffmpeg.html
