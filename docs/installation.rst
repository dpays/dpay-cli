Installation
============
The minimal working python version is 2.7.x. or 3.4.x

dpaycli can be installed parallel to python-dpay.

For Debian and Ubuntu, please ensure that the following packages are installed:
        
.. code:: bash

    sudo apt-get install build-essential libssl-dev python-dev

For Fedora and RHEL-derivatives, please ensure that the following packages are installed:

.. code:: bash

    sudo yum install gcc openssl-devel python-devel

For OSX, please do the following::

    brew install openssl
    export CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"
    export LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"

For Termux on Android, please install the following packages:

.. code:: bash

    pkg install clang openssl-dev python-dev

Signing and Verify can be fasten (200 %) by installing cryptography:

.. code:: bash

    pip install -U cryptography
    
Install dpaycli by pip::

    pip install -U dpaycli

Sometimes this does not work. Please try::

    pip3 install -U dpaycli

or::

    python -m pip install dpaycli

Manual installation
-------------------
    
You can install dpaycli from this repository if you want the latest
but possibly non-compiling version::

    git clone https://github.com/holgern/dpaycli.git
    cd dpaycli
    python setup.py build
    
    python setup.py install --user

Run tests after install::

    pytest
    
    
Installing dpaycli with conda-forge
--------------------------------

Installing dpaycli from the conda-forge channel can be achieved by adding conda-forge to your channels with::

    conda config --add channels conda-forge
    
Once the conda-forge channel has been enabled, dpaycli can be installed with::

    conda install dpaycli

Signing and Verify can be fasten (200 %) by installing cryptography::

    conda install cryptography

Enable Logging
--------------

Add the following for enabling logging in your python script::

    import logging
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

When you want to see only critical errors, replace the last line by::

    logging.basicConfig(level=logging.CRITICAL)
