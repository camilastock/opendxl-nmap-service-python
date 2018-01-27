from dxlbootstrap.app import Application
from dxlclient.service import ServiceRegistrationInfo
from requesthandlers import *


# Configure local logger
logger = logging.getLogger(__name__)


class NmapService(Application):
    """
    The "DXL Nmap Service" application class.
    """

    # The DXL Nmap service type for the lib-nmap tool
    SERVICE_TYPE = "/opendxl-nmap/service"

    # Custom report option request
    _REQ_SCAN = "{0}/scan/report".format(SERVICE_TYPE)

    def __init__(self, config_dir):
        """
        Constructor parameters:

        :param config_dir: The location of the configuration files for the
            application
        """
        super(NmapService, self).__init__(config_dir, "dxlnmapservice.config")

    @property
    def client(self):
        """
        The DXL client used by the application to communicate with the DXL
        fabric
        """
        return self._dxl_client

    @property
    def config(self):
        """
        The application configuration (as read from the "dxlnmapservice.config" file)
        """
        return self._config

    def on_run(self):
        """
        Invoked when the application has started running.
        """
        logger.info("On 'run' callback.")

    def on_load_configuration(self, config):
        """
        Invoked after the application-specific configuration has been loaded

        This callback provides the opportunity for the application to parse
        additional configuration properties.

        :param config: The application configuration
        """
        logger.info("On 'load configuration' callback.")

    def on_dxl_connect(self):
        """
        Invoked after the client associated with the application has connected
        to the DXL fabric.
        """
        logger.info("On 'DXL connect' callback.")
    
    def on_register_services(self):
        """
        Invoked when services should be registered with the application
        """
        # Register service 'nmapservice'
        logger.info("Registering service: {0}".format("nmapservice"))
        service = ServiceRegistrationInfo(self._dxl_client, self.SERVICE_TYPE)

        # See callback format
        logger.info("Registering request callback: {0}".format("Scan report"))
        self.add_request_callback(service, self._REQ_SCAN, NmapServiceRequestCallback(self, dict), True)

        self.register_service(service)
