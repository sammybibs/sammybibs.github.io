
###This import needed to parse templates
from flask import render_template

###Add support for POST calls
from flask import request
from flask import Flask, redirect, url_for, request

###Base import
from flask import Flask

###Import for the files updates needed
import os
from datetime import date

###Helpfull needed imports
import logging
import yaml
import re
import socket

###Allow us to reload modules
import importlib

###To convert strings to dicts.
import ast

###Sets the app up
app = Flask(__name__, template_folder='templates', static_folder='StaticFiles')


#####Use logging andremvoe print statements.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

"""
0. all dnac_data thats yaml then cast to a list needs to be all dict lookups.


1. Need to add buttin for DNAC UFDF Fields update with SNMP...

2. Have the initial homepage of the server ask for the password and cache it for that session in a variable.
2a. If you hardcore a password in yml that will be preferd

3. If the yml file has a integer in ip index 0 then use that, else resolve hostname.
3a. (Later add full check for valid IP & if fail connect try dns, and catch exertions)

4. allow only change the 2nd dnac server, where the sandbox is static.
"""

#Need to set the execute in the same folder for relative paths to use
os.chdir((os.path.dirname(os.path.abspath(__file__))))



####Two needed DNAC functions

def get_dnac(node):
   ip_regex = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
   if node == 'sandbox':
      with open('Dnac_data.yml', 'r') as file:
         node = yaml.safe_load(file)['server']['sandbox']
   elif node == 'lab':
      with open('Dnac_data.yml', 'r') as file:
         node = yaml.safe_load(file)['server']['lab']
   else:
      raise NameError(f'No server found, valid is "sandbox" or "lab"')
   #
   if not re.match(ip_regex, node['IP']):
      try:
         node['IP'] = socket.getaddrinfo(node['Host'], 443)[0][4][0]
      except:
         print('No IP and unresolvable hostname')
         raise NameError(f'No IP and unresolvable hostname')
   #
   DNAC_DATA = [node['IP'], node['Port'], node['Username'], node['Password']]
   return(DNAC_DATA)


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


####The web/flask functions
@app.route('/',methods = ['POST', 'GET'])
def index():
   logging.info('Homepage opened')
   size = 0
   datestamp = 'Missing'
   if request.method == 'GET':
      if len(os.listdir('cache')) != 0:
         size = sum([os.path.getsize(x) for x in os.scandir('cache')])//1024
         datestamp = str(date.fromtimestamp(os.path.getmtime('cache')))
      return render_template('dnac_sys_data.html', data=DNAC_data, size=size, cache_timestamp=datestamp)



@app.route('/update',methods = ['POST', 'GET'])
def update_system():
   if request.method == 'POST':
      IP = "'"+request.form.get("IPAddress")+"'"
      PORT = "'"+request.form.get("port")+"'"
      USER = "'"+request.form.get("Username")+"'"
      ####Need to add a check to see if the three above varaibles have an ', if they do error messsage
      ####And re-do
      #
      with open('DNAC_data.py', 'r') as input:
         with open("temp.txt", "w") as output:
            # iterate all lines from file
            for line in input:
                  # if line starts with substring 'shown below' then don't write it in temp file
                  if not line.strip("\n").startswith('def dnac_server(PASSWORD='):
                     output.write(line)
                  else:
                     output.write("def dnac_server(PASSWORD='Not Cached',IP="+IP+",PORT="+PORT+",USER="+USER+"):\n")
      # replace file with original name
      os.replace('temp.txt', 'DNAC_data.py')
      importlib.reload(DNAC_data)
      return index()
   if request.method == 'GET':
      return render_template('dnac_update.html', data=DNAC_data)


@app.route('/flush',methods = ['POST', 'GET'])
def flush_system():
   if request.method == 'POST':
      return 'This is an unuset toilet flush_system, post'
   if request.method == 'GET':
      os.chdir('cache')
      #return os.listdir()
      for file in os.listdir():
         os.remove(file)
      os.chdir("..")
      return redirect(url_for('index'))
      #return os.listdir()


@app.route('/cache',methods = ['POST', 'GET'])
def update_cache():
   if request.method == 'POST':
      ##Need a bunch of APIs to download the local needed cache
      Password = request.form.get("Password")
      DNAC_data[3] == (Password)
      token = get_token(DNAC_data)
      ##Get ALL devices in DNAC
      devices = DNAC_API.get_devices(dnacs, token, 'ALL')
      with open('./cache/get_devices.txt', 'w+') as f:
            f.write(str(devices))
      ##Get ALL interfaces as the search string is empty/any
      find_port = DNAC_API.find_port(dnacs, token, devices, "")
      with open('./cache/find_port.txt', 'w+') as f:
            f.write(str(find_port))
      ##GET all the SFP info on ALL nodes
      get_sfp = DNAC_API.get_sfp(dnacs, token, devices)
      with open('./cache/get_sfp.txt', 'w+') as f:
         for line in get_sfp:
            f.write(str(line))
      return index()
   if request.method == 'GET':
      return render_template('cache.html')


##Here we get the dnac login info to get a authC token and then search port descriptions fro strings
@app.route('/description',methods = ['POST', 'GET'])
def dnac_go_interface():
   ###Need to wirtie code for the local cahce to run...
   if request.method == 'POST':
      if len(os.listdir('cache')) != 0:
         if os.path.getsize('cache/find_port.txt') != 0:
            with open('./cache/find_port.txt','rt') as f:
                  searched_data = f.readlines()
                  searched_data = ast.literal_eval(searched_data[0])
            search = request.form.get("Search")
            return render_template('rendered_search.html', search_str=search, found_devices=searched_data)
      else:
      #sudo usertool.pl -p 'admin C1sco123!'
         Password = request.form.get("Password")
         search = request.form.get("Search")
         DNAC_data[3] == Password
         token = get_token(DNAC_data)
         devices = DNAC_API.get_devices(dnacs, token)
         searched_data = DNAC_API.find_port(dnacs, token, devices, search)
         return render_template('rendered_search.html', search_str=search, found_devices=searched_data)
   if request.method == 'GET':
      return render_template('description.html')



##Here we get the dnac login info to get a authC token and then get all the SFP data
@app.route('/sfp',methods = ['POST', 'GET'])
def dnac_get_sfp():
   if request.method == 'POST':
      Password = request.form.get("Password")
      DNAC_data[3] == Password
      token = get_token(DNAC_data)
      devices = DNAC_API.get_devices(dnacs, token)
      searched_data = DNAC_API.get_sfp(dnacs, token, devices)
      return render_template('rendered_sfp.html', sfps=searched_data)
   if request.method == 'GET':
      ##Check to see if there is cached data and a data in the file.
      if len(os.listdir('cache')) != 0:
         if os.path.getsize('cache/get_sfp.txt') != 0:
            searched_data = []
            with open('./cache/get_sfp.txt', 'r') as f:
               for line in f:
                  searched_data.append(line)
            return render_template('rendered_sfp.html', sfps=searched_data)
         else:
            return render_template('dnac_sfp.html')
      else:
         return render_template('dnac_sfp.html')




###This fucntion needs a clenaup and adding to the main web front end.
def get_snmp(dnac_system, token, devices):
    """[summary]
    this will glean the SNMP contact/location from each deivce, then update the UDF fields
    in DNAC with this same data.
    """
    headers = {'content-type': 'application/json'}
    headers['x-auth-token'] = token
    BASE_URL = f'https://{dnac_system[0]}:{dnac_system[1]}'
    ##Get SNMP info
    DEVICE_URL = '/dna/intent/api/v1/network-device/'
    UDF_TAG = '/user-defined-field'
    for DEVICE in devices:
        platform_data = requests.get(BASE_URL+DEVICE_URL+DEVICE, headers=headers, verify=False)
        platform_data = platform_data.json()
        logging.info(f"hostname = {platform_data['response']['hostname']}")
        logging.info(f"platformId = {platform_data['response']['platformId']}")
        logging.info(f"serialNumber = {platform_data['response']['serialNumber']}")
        logging.info(f"snmpContact = {platform_data['response']['snmpContact']}")
        logging.info(f"snmpLocation = {platform_data['response']['snmpLocation']}")
        logging.info()
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
        else:
            continue
        requests.put(BASE_URL+DEVICE_URL+DEVICE+UDF_TAG,data=json.dumps(payload), headers=headers, verify=False)


###Sets up the flask server if this code is called directly
if __name__ == '__main__':
   DNAC_data = get_dnac('lab')
   app.run(host='0.0.0.0', port=81)

