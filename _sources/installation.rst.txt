Installation
============

Prerequisites
*************

* OpenDXL Python Client library installed
   `<https://github.com/opendxl/opendxl-client-python>`_

* The OpenDXL Python Client prerequisites must be satisfied
   `<https://opendxl.github.io/opendxl-client-python/pydoc/installation.html>`_

* Python 2.7.9 or higher installed within a Windows or Linux environment
   (Python 3 is not supported at this time)

* Nnmap tool installed within a Windows or Linux environment

  You can look for more information in `<https://nmap.org/download.html>`_

  Note: The environment variable "nmap" must be populated with the fully-qualified location of the Nmap executable/binary.
  For windows operating system, this should be added into the PATH.

  Note: The nmap Python Service would need to be able to execute the nmap tool as the root user.

Installation
************

This distribution contains a ``lib`` sub-directory that includes the application library files.

Use ``pip`` to automatically install the library:

    .. parsed-literal::

        pip install dxlnmapservice-\ |version|\-py2.7-none-any.whl

Or with:

    .. parsed-literal::

        pip install dxlnmapservice-\ |version|\.zip

As an alternative (without PIP), unpack the dxlnmapservice-\version\.zip (located in the lib folder) and run the setup
script:

    .. parsed-literal::

        python setup.py install
