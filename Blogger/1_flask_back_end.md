# TOC
- [technology covered](#technology-covered-)
- [the background story](#the-background-story-)
- [web back end baseline](#web-back-end-baseline-)

# Technology covered <a name="technology-covered"></a>
* Python
  * Flask
  * jinja2
  * lists
  * dictionaries
  * if/else
  * HTML

<br><br>

# The background story <a name="the-background-story"></a>

Wanted to leverage the DNAC API to query data thats not directly accessible via the DNAC GUI

For this to be a bit more 'user friendly' the idea was to front end this with a web page.

After a quick google fu i came across [flask](https://flask.palletsprojects.com/en/2.2.x/) which after an hour or so I was able to [create a basic front end](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3).

Concurrently I have been tinkering with creating my first webex bot using the [webex bot STK](ttps://developer.cisco.com/codeexchange/github/repo/hpreston/webexteamsbot)

The first goal is to create the web front end with flask, then see if we can punt this functionality into a webex bot running in AWS.

<br><br>

# Web back end baseline <a name="web-back-end-baseline"></a>
First lets pull together a base shell to work from, this is called ```Hello_flask.py```
```python
 ###This import needed to parse templates
from flask import render_template

 ###Add support for POST calls
from flask import request
from flask import Flask, redirect, url_for, request

 ###Base import
from flask import Flask

 ###The sets the flask app up
app = Flask(__name__)

 ###Sets up the flask server if this code is called directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
```

<br><br>

Now if we run this code not a lot will happen, as there is no page to render when we browse to the url:

```python
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:81
 * Running on http://192.168.0.81:81
Press CTRL+C to quit
127.0.0.1 - - [11/Jan/2023 14:45:53] "GET / HTTP/1.1" 404 -
```

<br><br>

So we need a page to present at the route "/" page, like an index or readme.

```python
 ###Add some header variables to demo thier usage
dev = 'Sam Bibby'
updated = 'Jan 11th 2023'
purpose = 'learning'

 ###This import & variable used to get todays date
from datetime import datetime
date = datetime.now().strftime('%Y/%m/%d')

 ###The route() decorator, @app.route(), binds a URL to a function.
 ###The URL in thei case is the root of the page '/'
@app.route('/',methods = ['POST', 'GET'])
def index():
   if request.method == 'GET':
      print('jolly')
      return render_template('first_page.html', data=[dev,updated,purpose], timestamp=date)
```

<br><br>

We also need to create a ```first_page.html``` file, this should be saved in the /templates folder where the source code resides, as thats where flask will look.

Note that within the html we can use [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) for data manipulation. Below we create the file ```first_page.html``` as per the route decorator function.

```html
<html>
   <head>
      <h3>Welcome to the Web query engine </h3>
  </head>
   <body>
         Current values set are as follows: <br>
         Developer = {{ data[0] }} <br>
         Updated = {{ data[1] }} <br>
         Purpose = {{ data[2] }} <br><br>

         Todays date is {{ timestamp }} <br><br>
   </body>
</html>
```

<br><br>

Now when we run our code we get the web page presented:

I can see we made a GET request below to "/"
```python
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:81
 * Running on http://192.168.0.81:81
Press CTRL+C to quit
127.0.0.1 - - [11/Jan/2023 14:49:17] "GET / HTTP/1.1" 200 -
```

<br><br>

This calls the route decorator for the "/" path and passes the variables in a ```list``` to the template (notice here you can use GET or POST actions to dictate the returned functionality)
```python
@app.route('/',methods = ['POST', 'GET'])
def index():
   if request.method == 'GET':
      return render_template('first_page.html', data=[dev,updated,purpose], timestamp=date)
```

<br><br>

The template renders with the variables based on the called indexes, and we see in the front end as:
![](images/2023-01-11-14-58-25.png)

We can now add to this via creating interactive objects on the home page that launch other pages, for example a button here to call a new url, that calls a route decorator and renders a new page.

Below we update the file ```first_page.html``` file with a button object that calls the webpage /links
```html
<html>
   <head>
      <h3>Welcome to the Web query engine </h3>
  </head>
   <body>
         Current values set are as follows: <br>
         Developer = {{ data[0] }} <br>
         Updated = {{ data[1] }} <br>
         Purpose = {{ data[2] }} <br><br>

         Todays date is {{ timestamp }} <br><br>

         <form action = "http://localhost:81/links" method = "get">
         <button type="submit">Check My Bios</button>
         ::: See a list of really cool links
         </form><br>
   </body>
</html>
```
![](images/2023-01-11-15-03-48.png)

<br><br>

We add a new route to our ```Hello_flask.py``` file, this will pass a dictionary ```link_me``` that the jinja2 engine can parse when rendering the ```second_page.html``` file.
```python
 ###The route() decorator, @app.route(), binds a URL to a function.
 ###Where The decorator can renders a template with static variables
@app.route('/links')
def links():
   link_me = {"YouTube":"https://www.youtube.com/channel/UCFsz8jHR4Al-BqbfzFkGLPg",
            "Cisco Live":"https://www.ciscolive.com/on-demand/on-demand-library.html?search=bibby#/",
            "Community forums":"https://community.cisco.com/t5/user/viewprofilepage/user-id/194314)",
            "Discord":"https://discordapp.com/users/933769884050018364",
            "Linked in":"https://www.linkedin.com/in/samuel-bibby-22b03751/)"}
   return render_template('second_page.html', hyperlinks=link_me)
```

<br><br>

Then in the /templates folder we create the template thats to be rendered ```second_page.html```. This tempate uses jinja2 to render the items in the passed dictionary, where shown also has one ```if``` statement to highlight the key ```Discord``` in bold.
```
<html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        <ul>
        {% for k,v in hyperlinks.items() %}
        {% if k == "Discord": %}
        <li> This is <a href="{{ v }}">{{ k }}</a> </li>
	    {% else %}
        <li><a href="{{ v }}">{{ k }}</a> </li>
	{% endif %}
	{% endfor %}
	</ul>
    </body>
</html>
```

And front the front end when we click the ```Check My Bios``` button, we are cross launched to the new page thats rendered right before our eyes!:
![](images/2023-01-11-15-14-54.png)

So Viola, this is a basic flask app that we can use to present data in a nicer fashion than asking then to run some CLI.

Next we will look at leveraging API's towards DNAC, then how we can tie them together with flask for a nicer front end.
