"""This Uses the API to get the follwing data from functions
Devices SNMP server location and contact info
SPFs within each box
finds devices based on a confiured port description
The script is Cisco Confidential information and you should keep it securely
You are granted limited license to modify and enhance the provided Source Code [script] solely for your internal use and only to the extent we expressly permit
The script comes with no warranty of any kind, which means that if there are faults/errors in the script Cisco has no obligation to provide any help to resolve them
"""

__author__ = 'sabibby'
#!/usr/bin/env python3.10

import requests
from requests.auth import HTTPBasicAuth
import json
import socket

requests.urllib3.disable_warnings()
DNAC_IP = socket.getaddrinfo("sandboxdnac.cisco.com", 443)[0][4][0]

###Get/set the stuff we need to use
def dnac_server(PASSWORD='Cisco123!',IP=DNAC_IP,PORT='443',USER='devnetuser'):
    """[summary]
    This is the DNAC info that needs updating
    user will be asked for password on script execution
    """
    DNAC_IP = IP
    DNAC_PORT = PORT
    DNAC_USER = USER
    DNAC_PASSWORD = PASSWORD
    dnac_data = (DNAC_IP,DNAC_PORT,DNAC_USER,DNAC_PASSWORD)
    return dnac_data

def get_token(dnac_system):
    """[summary]
    Here we call up the API to get a token
    """
    url = (f'https://{dnac_system[0]}:{dnac_system[1]}/api/system/v1/auth/token')
    headers = {'content-type': 'application/json'}
    resp = requests.post(url, auth=HTTPBasicAuth(username=dnac_system[2], password=dnac_system[3]), headers=headers,verify=False)
    ####Add in error to catch bad password 
    token = resp.json()['Token']
    return token