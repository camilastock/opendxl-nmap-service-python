Running
=======

Once the application library has been installed and the configuration files are populated it can be started by
executing the following command line:

    .. parsed-literal::

        python -m dxlnmapservice <configuration-directory>

    The ``<configuration-directory>`` argument must point to a directory containing the configuration files
    required for the application (see :doc:`configuration`).

For example:

    .. parsed-literal::

        python -m dxlnmapservice config

Output
------

The output from starting the service should appear similar to the following:


    .. code-block:: python

        2017-09-18 12:52:04,202 dxlbootstrap.app INFO     Running application ...
        2017-09-18 12:52:04,202 dxlnmapservice.app INFO     On 'run' callback.
        2017-09-18 12:52:04,203 dxlnmapservice.app INFO     On 'load configuration' callback.
        2017-09-18 12:52:04,204 dxlbootstrap.app INFO     Incoming message configuration: queueSize=1000, threadCount=10
        2017-09-18 12:52:04,204 dxlbootstrap.app INFO     Message callback configuration: queueSize=1000, threadCount=10
        2017-09-18 12:52:04,222 dxlbootstrap.app INFO     Attempting to connect to DXL fabric ...
        2017-09-18 12:52:04,241 dxlbootstrap.app INFO     Connected to DXL fabric.
        2017-09-18 12:52:04,241 dxlnmapservice.app INFO     Registering service: nmapservice
        2017-09-18 12:52:04,241 dxlnmapservice.app INFO     Registering request callback: Scan report
        2017-09-18 12:52:04,248 dxlnmapservice.app INFO     On 'DXL connect' callback.

