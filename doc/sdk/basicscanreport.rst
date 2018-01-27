Basic Scan Report Example
=========================
This sample invokes and displays the results of an aggressive Nmap scan with the corresponding operating
system where this execution is being performed by invoking the Nmap service via DXL.

For more information see:
    https://nmap.org

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The DXL Nmap Service Python is running (see :doc:`running`)

Setup
*****
Modify the example to include the targets and options in the file you want to scan.

For example:

    .. code-block:: python

        # Define elements to be analysed
        target1 = '200.17.2.2'
        target2 = '200.17.2.3'
        target_list = [target1, target2]

        # Define options to execute the tool
        option = " -O -A"

Where `"target_#"` parameter represent the element to be analysed and `"option"` is the parameter to
execute Nmap tool
You can look for more information about Nmap tool in `Nmap page <https://nmap.org/book/man-briefoptions.html>`_


Running
*******

To run this sample execute the ``sample/basic/basic_aggressive_scan_report.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_scan_report.py


The output should be similar to the following:

    .. code-block:: python

        Response for nmapservice_requesthandler:

        Response:
        {
            "100": "------------------------------------------",
            "101": "Nmap scan report for 10.87.242.195. Host status: up",
            "102": "Operating System: Linux",
            "103": "Port:    22/tcp Status: open Service: ssh",
            "104": "------------------------------------------"
        }


Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # Connect to the fabric
        client.connect()

        logger.info("Connected to DXL fabric.")

        # Send request that will trigger request callback
        # 'nmapservice_requesthandler'
        request_topic = "/opendxl-nmap/service/scan/report"
        req = Request(request_topic)

        MessageUtils.dict_to_json_payload(req, {"target" : target_list, "option": option})
        res = client.sync_request(req, timeout=100)

        if res.message_type is not Message.MESSAGE_TYPE_ERROR:
            # Display results
            print "Response for nmapservice_requesthandler: '{0}'".format(MessageUtils.json_payload_to_dict(res))
        else:
            print "Error invoking service with topic '{0}': {1} ({2})".format(
                request_topic, res.error_message, res.error_code)

Once a connection is established to the DXL fabric, a request message is created with a topic that targets the remote commands of the DXL Nmap Service.

The final step is to display the contents of the returned dictionary (``dict``) which contains the results of the
aggressive scan report.
