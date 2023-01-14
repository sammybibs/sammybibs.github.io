
###This import needed to parse templates
from flask import render_template

###Add support for POST calls
from flask import request
from flask import Flask, redirect, url_for, request

###Base import
from flask import Flask

###Import the local DNAC scripts:
import DNAC_API
import DNAC_data

###Import for the files updates needed
import os
from datetime import date

###Allow us to reload modules
import importlib

###To convert strings to dicts.
import ast

###Sets the app up
app = Flask(__name__, template_folder='templates', static_folder='StaticFiles')



####Need to add buttin for UDF update with SNMP...

#Need to set the execute in the same folder for relative paths to use
os.chdir((os.path.dirname(os.path.abspath(__file__))))

@app.route('/',methods = ['POST', 'GET'])
def index():
   size = 0
   datestamp = 'Missing'
   if request.method == 'GET':
      if len(os.listdir('cache')) != 0:
         size = sum([os.path.getsize(x) for x in os.scandir('cache')])//1024
         datestamp = str(date.fromtimestamp(os.path.getmtime('cache')))
      return render_template('dnac_sys_data.html', data=DNAC_data.dnac_server(), size=size, cache_timestamp=datestamp)


#####Current need to write
###Purge the cache when "flush" is run
###Purge the local cahce when the 'update dnac' is run
###use the local cache for all if its there.. (descriptions)


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
      return render_template('dnac_update.html', data=DNAC_data.dnac_server())


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
      dnacs = DNAC_data.dnac_server(Password)
      token = DNAC_data.get_token(dnacs)
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
         dnacs = DNAC_data.dnac_server(Password)
         token = DNAC_data.get_token(dnacs)
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
      dnacs = DNAC_data.dnac_server(Password)
      token = DNAC_data.get_token(dnacs)
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
        print(f"hostname = {platform_data['response']['hostname']}")
        print(f"platformId = {platform_data['response']['platformId']}")
        print(f"serialNumber = {platform_data['response']['serialNumber']}")
        print(f"snmpContact = {platform_data['response']['snmpContact']}")
        print(f"snmpLocation = {platform_data['response']['snmpLocation']}")
        print()
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
    app.run(host='0.0.0.0', port=81)

