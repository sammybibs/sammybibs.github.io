# TOC
- [Technology covered](#technology-covered-)
- [The background story](#the-background-story-)
- [Accessing the api](#accessing-the-api-)
- [Use cases](#use-cases-)
  - [Dnac user defined fields update](#dnac-user-defined-fields-update-)
    - [Glean device ids](#glean-device-ids-)
    - [Glean device data](#glean-device-data-)
      - [Summary](#summary-)

# Technology covered <a name="technology-covered"></a>
* DNAC API
* Python
  * Flask
  * jinja2
  * lists
  * dictionaries
  * if/else
  * HTML
* AWS hosted

<br><br>

# The background story <a name="the-background-story"></a>

Wanted to leverage the DNAC API to query data thats not directly accessible via the DNAC GUI

For this to be a bit more 'user friendly' the idea was to front end this with a web page.

After a quick google fu i came across [flask](https://flask.palletsprojects.com/en/2.2.x/) which after an hour or so I was able to [create a basic front end](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3).

Concurrently I have been tinkering with creating my first webex bot using the [webex bot STK](ttps://developer.cisco.com/codeexchange/github/repo/hpreston/webexteamsbot)

The first goal is to create the web front end with flask, then see if we can punt this functionality into a webex bot running in AWS.

<br><br>

# Accessing the API <a name="accessing-the-api"></a>
I'm not going to go into a lot of depth here, as there is a plethora of information out there, but in a bid to not send you on a internet hole ill add the baseice in here. But do have a look at [Cisco DNAC API DevNet page](https://developer.cisco.com/docs/dna-center/#!api-quick-start/api-quickstart) for further reading.

The short of it is we need the information on the target system, and using this we need a token. For this demo ill use the [devnet DENAC alway-on sandbox](https://sandboxdnac.cisco.com/). 

The following four blocks of code will be saved in a single file ```DNAC_data.py```, there broken into four for ease of explanation. 

<br>


The required imports to execute out upcoming functions, the ```requests.urllib3.disable_warnings()``` setting allows browsing the insecure https pages, such as unverified DNAC lab servers.

```python
import requests
from requests.auth import HTTPBasicAuth
import json
import getpass

requests.urllib3.disable_warnings()
```


The first ```dnac_server``` function you should edit the {IP/PORT/Username} with your own lab DNACs data, its use is to return a tuple with the DNA Centre credentials.

```python
def dnac_server(PASSWORD='Not Cached',IP='131.226.217.136',PORT='443',USER='devnetuser'):
    """[summary]
    This is the DNAC info that needs updating
    user will be asked for password "Cisco123!"
    """
    DNAC_IP = IP
    DNAC_PORT = PORT
    DNAC_USER = USER
    DNAC_PASSWORD = PASSWORD
    dnac_data = (DNAC_IP,DNAC_PORT,DNAC_USER,DNAC_PASSWORD)
    #
    return dnac_data
```

Next we need a second function to make the API call to DNAC and get the access token:
```python
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
```

Finally call the functions, here we use the getpass module as this masks user input when prompted for the password. We then pass this to the respective function, then pass the returned DNAC system to the token function.

```python
passkey = getpass.getpass()
dnac_data = dnac_server(PASSWORD=passkey)
print(dnac_data)
token = get_token(dnac_data)
print(token)
```

Now we can see the results of the two functions in action, and we have a usable token for future API calls.
```python
>>> passkey = getpass.getpass()
Password: 
>>> dnac_data = dnac_server(PASSWORD=passkey)
>>> print(dnac_data)
('131.226.217.136', '443', 'devnetuser', 'Cisco123!')
>>> token = get_token(dnac_data)
>>> print(token)
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MDJlNTBiZmI2MDg5YzAwOTMyZjEyMWYiLCJhdXRoU291cmNlIjoiZXh0ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVzIjpbIjVkNDA1ZDRlNzhhMDIzMDA0Yzg3OTg0MSJdLCJ0ZW5hbnRJZCI6IjVkNDA1ZDRkNzhhMDIzMDA0Yzg3OTgzZiIsImV4cCI6MTY3MzQ2MDczNCwiaWF0IjoxNjczNDU3MTM0LCJqdGkiOiIwNWZmZmYwNC05YjRiLTQ5NjctODIxMS00ZjNiYmI1ODY2MjUiLCJ1c2VybmFtZSI6ImRuYWFkbWluIn0.HXdp-JV8Im6fAfFd7md-lQx_ErfezWZAElj7z5je4LsjQVLSuoxXvACRPQbBNygaje8wtkzGTLouF9No7vEncKoTepnbI7koLncm-nJRBcMHZit9bq_15VAfmGZKYwIvwiwDeFbx5pfjbtnYsCihPLwk0jqs6gVS3isGh8y4hicyl5lT8U_yyN2K4EOS_mcLzRyUbDHgNmSK3HCOVA1Ej0RtubZwOy1QFut-V1IceAFVeL3pW-LvPegQj5cbbiZxrgxtfR5iGgT2pP1zDGiCqMmtR1L4K4JrgTrZqFE7LyP1L0bFPmJfsFWqXhiHV1RB9w3QOwA577r5uXZ7oKLZuw
```
<br>


# Use cases <a name="use-cases"></a>

DNAC API info is self documented in DNAC:
* https://**{{YOUR-DNAC-IP}}**/dna/platform/app/consumer-portal/developer-toolkit/apis


## DNAC User Defined Fields update <a name="dnac-user-defined-fields-update"></a>
---

**Requirement:**
* Use DNAC to identify who the device owner and contact details for them.

**Back story:**
* This is a brownfield network, the hostname is already bloated and not practical to use. Today they leverage the ```SNMP name``` and ```SNMP contact``` details on the device to find the owner.

**Solution:**
* leverage the ```user-defined-field``` (UDF) API to post the SNMP data to the DNAC GUI for easy access.
![](images/2023-01-11-17-37-05.png)

**How do we achieve this?** <br>
Working backwards from what we want to do, we need the following data:
0. Push the SNMP data to the UDF in DNAC
1. All SNMP contact and location data on the device.
2. Details of the devices that we want to glean the SNMP data from and post to the UDF fields.

For (1) we can get all this data via an API call to the ```Get Device by ID``` API, specifically **/dna/intent/api/v1/network-device/${id}**. This will provide us with a plethora of usable data about the chassis including the SNMP data. Plus this information is cached within DNAC already, so no need to make any calls direct the device itself.

To achieve the above we need to get (2), what are the devices we want to query and specifically what are the devise IDs (this is a DNAC 36 character value that DNAC uses to ID a node).

<br>

### Glean device IDs <a name="glean-device-ids"></a>
---

So working backwards we first need the device IDs. We can do this with a function that calls the ```Get Device list```, specifically **/dna/intent/api/v1/network-device**. This returns a list of all devices & we can  pass parameters to filter the returned response (such as device type, location, role...)

For our filter I have decided to use the ```ROLE``` field, where the usable options are as per the DNAC inventory 'Device Role' column.
* **[UNKNOWN, ACCESS, CORE, DISTRIBUTION, BODER ROUTER]**

If no role is passed, the function will assume ALL. Now we can use the data from our previous functions and pass them to this function to glean the device ID's (dnac_data & token)

```python
def get_devices(dnac_system, token, role='ALL'):
    """[summary]
    Gets the required devices
    """
    headers = {'content-type': 'application/json'}
    headers['x-auth-token'] = token
    BASE_URL = f'https://{dnac_system[0]}:{dnac_system[1]}'
    DEVICE_URL = '/dna/intent/api/v1/network-device'
    device_data = requests.get(BASE_URL+DEVICE_URL, headers=headers, verify=False)
    device_data = device_data.json()
    if role == 'ALL':
        devices = [i['instanceUuid'] for i in device_data['response']]
    else:
        devices = [i['instanceUuid'] for i in device_data['response'] if i['role'] == role]
    return devices
```

Running this with no role defined we see all nodes are gleaned:
```python
device_list = get_devices(dnac_data, token)
print(device_list)
['redacted-e0ac-4616-81e7-xxxredacted', 'redacted-e0d5-4194-b062-xxxredacted', 'redacted-9024-46c9-8775-xxxredacted', 'redacted-f52a-4869-b447-xxxredacted', 'redacted-1658-459b-9c77-xxxredacted', 'redacted-fdf4-47b9-aa45-xxxredacted', 'redacted-543d-46d2-95c7-xxxredacted', 'redacted-4fc4-4589-a906-xxxredacted', 'redacted-d751-4892-91d0-xxxredacted', 'redacted-7b3d-458b-9212-xxxredacted', 'redacted-d7a3-4912-8cdf-xxxredacted', 'redacted-4ba6-43e3-9793-xxxredacted', 'redacted-e87a-4a48-a8bf-xxxredacted', 'redacted-0881-4926-a348-xxxredacted', 'redacted-7578-444c-8e87-xxxredacted', 'redacted-a518-4866-96f2-xxxredacted', 'redacted-fb0a-453a-b3d4-xxxredacted', 'redacted-1825-4392-a05c-xxxredacted', 'redacted-3d18-42b2-8c47-xxxredacted', 'redacted-0071-46a3-be21-xxxredacted', 'redacted-e20b-46ec-a3d5-xxxredacted', 'redacted-8a6f-4b40-9026-xxxredacted', 'redacted-dc1b-400f-8333-xxxredacted', 'redacted-a1db-4555-a863-xxxredacted', 'redacted-d50e-4a09-ad35-xxxredacted', 'redacted-ed9f-47dc-9612-xxxredacted', 'redacted-afec-4933-a7aa-xxxredacted']
```

Vs running this with the 'ACCESS' filter passed, where we see just the nodes with that classification.
```python
device_list = get_devices(dnac_data, token, role='ACCESS')
print(device_list)
['redacted-4fc4-4589-a906-xxxredacted', 'redacted-7578-444c-8e87-xxxredacted', 'redacted-a518-4866-96f2-xxxredacted', 'redacted-8a6f-4b40-9026-xxxredacted', 'redacted-ed9f-47dc-9612-xxxredacted']
```

<br>

> Side note: I redacted the prefix and suffix out of paranoia, heres how i achieved that with slicing in a for loop.
```python
r = 'redacted'
for i,dev in enumerate(device_list):
    device_list[i] = r+dev[8:-8]+r
print(device_list)
```

<br>

**Result:** Success, we now have the device ID's we can pass to the ```Get Device by ID``` and pull the SNMP data.

<br>

### Glean device data <a name="glean-device-data"></a>
---

Within this function we can do two things:
1. Pass the device ID data to the ```Get Device by ID``` API and glean the SNMP data.
2. Post this SNMP data to the DNAC ```User Defined Fields``` API.

> **Warning:** this post action will only work if the field placeholder is already created in DNAC.. Browse to DNAC, select a device, open the 'user defined field' menu & click ```Manage User Defined Fields```, then ```Create new field``.
> The name we use here is used as the key, when posting the data back to DNAC.

![](images/2023-01-11-19-48-03.png)

```python
def get_snmp(dnac_system, token, devices):
    """[summary]
    this will glean the SNMP contact/location from each device, then update the UDF fields
    in DNAC with this same data.
    """
    headers = {'content-type': 'application/json'}
    headers['x-auth-token'] = token
    BASE_URL = f'https://{dnac_system[0]}:{dnac_system[1]}'
    ##Get SNMP info
    DEVICE_URL = '/dna/intent/api/v1/network-device/'
    UDF_TAG = '/user-defined-field'
    ##Loop over each device passed, glen the data, print the output for debugging
    for DEVICE in devices:
        platform_data = requests.get(BASE_URL+DEVICE_URL+DEVICE, headers=headers, verify=False)
        platform_data = platform_data.json()
        print(f"device-id = {r+DEVICE[8:-8]+r}")
        print(f"hostname = {platform_data['response']['hostname']}")
        print(f"platformId = {platform_data['response']['platformId']}")
        print(f"softwareVersion = {platform_data['response']['softwareVersion']}")
        print(f"snmpContact = {platform_data['response']['snmpContact']}")
        print(f"snmpLocation = {platform_data['response']['snmpLocation']}")
        print()
        ##Check what SNMP variables are present and set the respective needed payloads.
        if platform_data['response']['snmpContact'] and platform_data['response']['snmpLocation']:
            payload = [{"name":"snmpContact","value":platform_data['response']['snmpContact']},
                    {"name":"snmpLocation","value":platform_data['response']['snmpLocation']}]
                    #
        elif platform_data['response']['snmpContact']:
            payload = [{"name":"snmpContact","value":platform_data['response']['snmpContact']}]
            #
        elif platform_data['response']['snmpLocation']:
            payload = [{"name":"snmpLocation","value":platform_data['response']['snmpLocation']}]
            #
        else:
            continue
         ##Make the post call to DNAC with the correct payload to update the GUI UDF page.
        req = requests.put(BASE_URL+DEVICE_URL+DEVICE+UDF_TAG,data=json.dumps(payload), headers=headers, verify=False)
        ##Debugging and demo purposes
        print(req)
```

Now we can use the data from our previous functions (**dnac_data, token & the device_list**) and pass them to this function to glean the device information and updte the DNAC UDF GUI.

First Lets check DNAC and a device to be sure its got no deifned UDF data. We can see below it has none and its a role of access (this mathces our device_data query (*you can validate teh deivce ID by checking the broswer URL also*))
![](images/2023-01-12-08-46-42.png)


Now lets run this function and from the outputs we can see the data we are looking for, where onoly two devices have SNMP data defined.
```python
get_snmp(dnac_data, token, device_list)

device-id = redacted-4fc4-4589-a906-8276redacted
hostname = DNA_9800_WLC.ramblings-one
platformId = C9800-CL-K9
softwareVersion = 16.11.1c
snmpContact = 
snmpLocation = 

device-id = redacted-7578-444c-8e87-fe67redacted
hostname = UK-LAB-FE-01.ramblings-one
platformId = C9300-48U
softwareVersion = 17.6.3
snmpContact = Sam Bibby
snmpLocation = The Lab of doom

<Response [202]>
device-id = redacted-a518-4866-96f2-ff82redacted
hostname = UK-LAB-FE-02.ramblings-one
platformId = C9300-48U
softwareVersion = 17.6.3
snmpContact = The Rambling Frog
snmpLocation = 

<Response [202]>
device-id = redacted-8a6f-4b40-9026-e052redacted
hostname = vFE01.corpnet2.com
platformId = None
softwareVersion = 17.6.1
snmpContact = 
snmpLocation = 

device-id = redacted-ed9f-47dc-9612-5f5credacted
hostname = VIRTUAL_SITE_CP_BN
platformId = CSR1000V
softwareVersion = 17.3.4a
snmpContact = 
snmpLocation = 
```

We can also see from the returned code **202** that everything looks ok **The request has been accepted for processing, but the processing has not been completed.**

If we then revert back to DNAC to see if these SNMP varaibles have been posted to the UDF field withing the GUI..... Well i can tell you it failed, and ill explain why as its a simple error.

If look at the code that generated the put payload below we can see the fields used are *"snmpContact"* & *"snmpLocation"*, where if we check on DNAC (see above screenshot), our UFD "Field Names" are **"SNMP Contact"** & **"SNMP Location"**
```python
        if platform_data['response']['snmpContact'] and platform_data['response']['snmpLocation']:
            payload = [{"name":"snmpContact","value":platform_data['response']['snmpContact']},
                    {"name":"snmpLocation","value":platform_data['response']['snmpLocation']}]
                    #
        elif platform_data['response']['snmpContact']:
            payload = [{"name":"snmpContact","value":platform_data['response']['snmpContact']}]
            #
        elif platform_data['response']['snmpLocation']:
            payload = [{"name":"snmpLocation","value":platform_data['response']['snmpLocation']}]
            #
```


So lets fix that code block & re-run the function.
```python
        if platform_data['response']['snmpContact'] and platform_data['response']['snmpLocation']:
            payload = [{"name":"SNMP Contact","value":platform_data['response']['snmpContact']},
                    {"name":"SNMP Location","value":platform_data['response']['snmpLocation']}]
                    #
        elif platform_data['response']['snmpContact']:
            payload = [{"name":"SNMP Contact","value":platform_data['response']['snmpContact']}]
            #
        elif platform_data['response']['snmpLocation']:
            payload = [{"name":"SNMP Location","value":platform_data['response']['snmpLocation']}]
            #
```

**Omitted deivces with no SNMP DATA to consolidate outputs**
```python
get_snmp(dnac_data, token, device_list)

device-id = redacted-7578-444c-8e87-fe67redacted
hostname = UK-LAB-FE-01.ramblings-one
platformId = C9300-48U
softwareVersion = 17.6.3
snmpContact = Sam Bibby
snmpLocation = The Lab of doom

<Response [202]>
device-id = redacted-a518-4866-96f2-ff82redacted
hostname = UK-LAB-FE-02.ramblings-one
platformId = C9300-48U
softwareVersion = 17.6.3
snmpContact = The Rambling Frog
snmpLocation = 
```
If we head back over to DNAC we can validate that these two devices have the required DATA in the GUI:
![](images/2023-01-12-09-47-04.png)
![](images/2023-01-12-09-47-27.png)

<br>
#### Summary <a name="summary"></a>
---