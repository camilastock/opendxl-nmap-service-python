import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlclient.message import Message, Request
from dxlbootstrap.util import MessageUtils

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Define elements to be analysed
target_1 = 'host_1'
target_2 = 'host_2'
target_list = [target_1, target_2]

# Define options to execute the tool
option = " -O -A"

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    # Send request that will trigger request callback 'nmapservice_requesthandler'
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