Para usar el LimeSDR en el PC se require lo siguiente:
* ``sudo add-apt-repository -y ppa:myriadrf/drivers``
* ``sudo apt-get update``
* ``sudo apt-get install limesuite liblimesuite-dev limesuite-udev limesuite-images``
* ``sudo apt-get install soapysdr-tools soapysdr-module-lms7``

* ``sudo apt-get install soapysdr soapysdr-module-lms7``


* ``sudo apt-get install libboost-all-dev swig``
* ``git clone https://github.com/myriadrf/gr-limesdr``

* ``cd gr-limesdr``
* ``mkdir build``
* ``cd build``
* ``cmake ..``
* ``make``
* ``sudo make install``
* ``sudo ldconfig``
