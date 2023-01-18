<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XKHR6PXZ9V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XKHR6PXZ9V');
</script>


# TABLE OF CONTENTS

- [Flask Back End basics](/Blogger/DNAC_API/1_flask_back_end)
- [DNAC APIs required](/Blogger/DNAC_API/2_DNAC_API)
- [DNAC info Flask](/Blogger/DNAC_API/3_DNAC_into_flask)

### **[The current locally run web application is here](https://www.github.com/sammybibs/DNAC_API_Query/)**

# The background story

As a network engineer who dabbles in python I created this side project to develop my repertoire. The overall goal is to leverage the DNAC API to query data thats not directly accessible via the DNAC GUI. The fuel for this idea came from various DNAC deployments where we are asked *"can DNAC do...."*, where the answer is often *"yes, but.. you need to use the API".*

I am a fan of APIs, only a recent fan mind you and I'm only on this trajectory out of necessity, So as I enhance my skill set to include APIs, python and any other faucets of automation, I'll endeavor to document them as I go. This hopefully will offer others some guidance as you also transition. That and it hopefully will be a nice reminder of where it all started (right here, right now) vs where we end up.


Onto the project, for this to be a bit more 'user friendly' the idea was to front end this with a web page.

After some google fu i came across [flask](https://flask.palletsprojects.com/en/2.2.x/) which after an hour or so I was able to create a basic front end [using this guid](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3). Concurrently I have been tinkering with creating my first webex bot using the [webex bot STK](ttps://developer.cisco.com/codeexchange/github/repo/hpreston/webexteamsbot) & I would like this app to be front ended in one, or both of these formats.

The goals then are to:
1. Create the web front end with flask
2. Run the web front end in AWS
3. See if we can punt this front end functionality into a webex bot running in AWS
4. Package the app into a docker container.


Onto the project, for this to be a bit more 'user friendly' the idea was to front end this with a web page.



