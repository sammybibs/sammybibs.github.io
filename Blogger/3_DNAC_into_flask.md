# Contents
- [Technology covered](#technology-covered-)
- [The background story](#the-background-story-)
- [Web back end baseline](#web-back-end-baseline-)

# Technology covered <a name="technology-covered"></a>
* January 03 2023
* Python
  * Flask
  * jinja2
  * lists
  * dictionaries
  * if/else
  * HTML

<br><br>

# The story <a name="the-background-story"></a>

Now we have a basic flask app and the DNAC APIs we need to use, we will look at combining the two together.

[The full project files are here](/Blogger/DNAC_API/DNAC_Web_Server/)

<br>

# Arranging the folder structure

To make this project portable, so that anyone can copy it and modify it for their own deployment we split the code files into two, where one will take care of accessing DNAC and getting a token, the other will hold all our API calls.

Also remembering that the flask app looks in the *./templates* folder for the HTML file to render, our project folder will look like this:

- DNAC_Web_Server (Project folder)
  - templates (templated folder)
    - index.html (homepage)
    - TBC.html (subsequent pages)
  - DNAC_data.py (DNAC IP/PORT settings and token function)
  - DNAC_API.py (Our DNAC API calls)
  - Web_app.py (Launch code fro the flask app)
  - requirements.txt (project python requirements)

# Setup the DNAC python files

The two DNAC~.py files are created in the directory:

**DNAC_API.py** : this contains our required APIs as functions, i wont re-paste them here as they are mostly the same as our previous post. The main difference is the print statements have been removed & the functions return that data as some sort of object (list/dic] to allow us to pass it the the flask app for rendering in Jinja2)


**DNAC_data.py** : this uses the devnet sandbox DNAC centre & resolves the IP for us.
```python
requests.urllib3.disable_warnings()
DNAC_IP = socket.getaddrinfo("sandboxdnac.cisco.com", 443)[0][4][0]


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
```

<br>


# Setup the flask routes and web pages
The skeleton for flask we build in the first blog post, all we need to do now is create additional functions with the @route property to call the DNAC API functions and render the results:

In the Web_app.py file we need to import the DNAC files for use, as well as some other useful modules:
```python
 ###Import the local DNAC scripts:
import DNAC_API
import DNAC_data

 ###Import for the files updates needed
import os
from datetime import date

 ###Allow us to reload modules
import importlib

 #Used to set the execute in the same folder for relative paths to use
os.chdir((os.path.dirname(os.path.abspath(__file__))))
```



The first webepage

```python
@app.route('/',methods = ['POST', 'GET'])
def index():
   size = 0
   datestamp = 'Missing'
   if request.method == 'GET':
      if len(os.listdir('cache')) != 0:
         size = sum([os.path.getsize(x) for x in os.scandir('cache')])//1024
         datestamp = str(date.fromtimestamp(os.path.getmtime('cache')))
      return render_template('dnac_setup.html', data=DNAC_data.dnac_server(), size=size, cache_timestamp=datestamp)
```