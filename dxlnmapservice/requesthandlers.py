import logging

from dxlclient.callbacks import RequestCallback
from dxlclient.message import Response, ErrorResponse
from dxlbootstrap.util import MessageUtils

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

# Configure local logger
logger = logging.getLogger(__name__)


class NmapServiceRequestCallback(RequestCallback):
    """
    'nmapservice_requesthandler' request handler registered with topic '/opendxl-nmap/service/scan/report'
    """

    def __init__(self, app, params):
        """
        Constructor parameters:

        :param app: The application this handler is associated with
        :param params: The params this application will use
        """
        super(NmapServiceRequestCallback, self).__init__()
        self._app = app
        self._required_params = params

    @staticmethod
    def _get_host_os_info(host):
        """
        Extract host operating system information

        :param host: Host (IP) to scan/analyze
        :return: String with the operating system information running in this host
        """
        if host.os_fingerprinted:
            nmap_match = host.os.osmatches
            match = nmap_match.pop()
            os = match.osclasses
            nmap_os = os.pop()
            output = "Operating System: {0}".format(
                nmap_os.osfamily)
        else:
            output = "No fingerprint available"
        return output

    @staticmethod
    def _get_host_services_info(svc):
        """
        Scan each port, state and service running

        :param svc: Service running in this host
        :return: String with port, state and service name running
        """
        result = "Port: {0:>5s}/{1:3s} Status: {2} Service: {3}".format(
                str(svc.port), svc.protocol, svc.state, svc.service)
        return result

    def _do_nmap_scan(self, req_dict, request):
        """
        Builds a report with the information (output) provided by Nmap tool.

        :param req_dict: The required dictionary with Nmap parameters/information to execute.
        :param request: The request message.
        :return: Nmap tool execute output in a dictionary format.
        """
        # Extract targets and options parameters
        targets = req_dict["target"]
        options = req_dict["option"]

        # Generate a parsed Nmap report
        report = self._generate_nmap_dict_report(targets, options, request)

        return report

    def _generate_nmap_dict_report(self, targets, options, request):
        """
        Executes the Nmap tool to scan/analyze a list of hosts (IPs) with the specific
        (parameters) options.

        :param targets: List of hosts (IPs) to scan/analyze.
        :param options: Options required to execute Nmap tool.
        :param request: The request message.
        :return: The Nmap output information (formatted) based on the original Nmap XML report
        information.
        """

        # Create Nmap process and run it
        nmproc = NmapProcess(targets, options)

        try:
            # Run the Nmap process
            nmproc.run()

            # Generate report
            nmap_report = NmapParser.parse(nmproc.stdout)

            # Parse Nmap report
            parsed_report = self._parse_nmap_xml_report(nmap_report)

            # Return the parse  Nmap report
            return parsed_report
        except Exception as ex:
            logger.exception("Nmap scan failed: {0}".format(nmproc.stderr))
            err_res = ErrorResponse(request, MessageUtils.encode(str(ex)))
            self._app.client.send_response(err_res)

    def _parse_nmap_xml_report(self, nmap_report):
        """
        Parses the original Nmap XML report information in order to extract information
        about each port, state and service running in each host. Also, it extracts the
        operating system information, if applies.

        :param nmap_report: Nmap report based on the Nmap tool execution.
        :return: The XML report information in a dictionary format.
        """
        try:
            # Generate a dictionary with nmap report information
            output = {}
            aux = 100
            output[aux] = "------------------------------------------"

            if len(nmap_report.hosts) == 0:
                output[aux] = "No hosts were found to perform the selected scan/analysis"
            else:
                # Scan each target
                for host in nmap_report.hosts:
                    if len(host.hostnames):
                        host.hostnames.pop()
                    else:
                        # Extract host ip and status information
                        output[aux + 1] = "Nmap scan report for {0}".format(host.address)
                        output[aux + 2] = "Host status: {0}".format(host.status)

                        # Extract host operating system information
                        aux = aux + 3
                        output[aux] = self._get_host_os_info(host)

                        # Scan each port, state and service running
                        for svc in host.services:
                            aux = aux + 1
                            output[aux] = self._get_host_services_info(svc)

                        aux = aux + 1
                        output[aux] = "------------------------------------------"

        except NmapParserException as e:
            logger.info("Exception raised while parsing scan: {0}".format(e.msg))
        return output

    def on_request(self, request):
        """
        Invoked when a request message is received.

        :param request: The request message
        """
        # Handle request
        logger.info("Request received on topic: '{0}' with payload: '{1}'".format(
            request.destination_topic, MessageUtils.decode_payload(request)))

        try:
            # Parameters
            nmap_params = MessageUtils.json_payload_to_dict(request)

            logger.info("[1/2] Requested NMAP action ({0}) for request {1} is under processing...".format(
                MessageUtils.decode_payload(request), request.message_id))
            # Create a report from Nmap tool execution
            nmap_response = self._do_nmap_scan(nmap_params, request)
            logger.info("[2/2] Requested NMAP action was processed successfully for request {0}."
                        " Preparing response...".format(request.message_id))

            # Create response
            res = Response(request)

            # Set payload
            MessageUtils.dict_to_json_payload(res, nmap_response)

            # Send response
            self._app.client.send_response(res)
            logger.info("Sending response for request {0}".format(request.message_id))

        except Exception as ex:
            logger.exception("Error handling request")
            err_res = ErrorResponse(request, MessageUtils.encode(str(ex)))
            self._app.client.send_response(err_res)
