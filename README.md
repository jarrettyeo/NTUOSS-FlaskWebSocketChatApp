# NTUOSS Flask Websockets Chat App Workshop
#### Create your Instant Messaging app using blazing-fast websockets in 2 hours or less!

*by [Jarrett Yeo](https://github.com/jarrettyeo) for NTU Open Source Society*

*Date last updated: 30 January 2018*

___

## **Overview**

This workshop will teach you how to create your own websocket-connected, eventlet-networked, and ngrok-tunnelled Flask chat app. The client will be in Javascript while the server will be powered by (Python) Flask.

## **Workshop Structure**

Here's what we'll be doing (after hearing a story on websockets):

1. We'll create a "Hello World!" Flask app,
2. and another one for (Flask) websockets,
3. and finally our fast and beautiful Instant Messaging app as promised.
4. Then we'll end off the workshop by exposing your app to the whole world using ```ngrok``` so that you can have fun hopping onto one another's chat app and getting to know more friends!

___

## Questions

If you have a question regarding any of the instructions here, feel free to raise your hand any time during the pre-workshop or email your questions to [me](mailto:shanwei96@gmail.com).

## Errors

For errors, typos or suggestions, please do not hesitate to [post an issue](https://github.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/issues/new). Thank you!

## **Disclaimer**

Neither the author nor NTU OSS claims or owns the appended resources. We also do not accept any responsibility for things that happen to your machine or you because of this tutorial.

___

## **Introduction to Websockets**

#### *Before We Begin*

Please bear with the introduction for a while. We would like to help you understand in just 5 minutes (I promise) the story of websockets, so that we can all appreciate its use cases and existence.

#### *Traditional Data Polling*

Before we can appreciate websockets, let's take a look at the traditional forms of data polling first - [Reading 1](https://stackoverflow.com/a/12855533).

#### *Websockets & Its Advantages*

In short, websockets allows you to send messages to your server and receive event-driven responses without the need for constantly polling your server for a reply. It is an "advanced technology that allows for full-duplex / bi-directional realtime communication between server and client".

#### *Websockets v. Long-Polling*

In long-polling, you keep the connection alive and wait continuously until the server sends data back to you, and thereafter you open a new connection to do the same. In websockets, upon establishing a connection, data is sent right away in both directions (without the client waiting for a response from the server).

#### *Websockets: Advantages (over Long-Polling)*

- Realtime 2-way communication
- Recovers a broken connection better
- Potentially lower latency
- Potentially lower data usage

#### *Websockets: Disadvantages*

- Requires an explicit action to close connection
- Can potentially generate high bandwidth consumption since an active connection is maintained throughout communication
- Not all web browsers support websockets, though most do now other than Opera Mini.

#### *So which is better? When should I use websockets?*

This is a very difficult question to answer.

In websockets, the server keeps a connection alive. In long-polling, the server keeps polling for new data. Again, it highly depends on what you want to do, because different usages can cause one to be less expensive than the other (in terms of setup, costs, bandwidth, resource in general and so on).

It all boils down to your usage - what are you building? If you creating a realtime 2-way web app or game that requires a high frequency of data exchange, Websockets is probably the better choice. An Instant Messaging Chat app like ours? Perfect use case for websockets!

Apparently, Slack, Trello and Stackoverflow (Push Notifications) all use websockets, with Facebook and Google and the like looking at pushing this technology into its products.

For more use cases of websockets, you can take a look at [Reading 2](https://www.infoworld.com/article/2609720/application-development/9-killer-uses-for-websockets.html).

#### *You mentioned websockets is supported by most browsers, but not all. How do I utilise websockets on my Flask web app then?*

We will be using the Flask-SocketIO library. More on this later.

___

# **Step 1 - Hello World Flask App**

## **Overview**

We will be building our websockets chat app with Flask, a popular web framework on Python (second to Django, but whatever). Let's  get our Flask app up and running first just to make everyone can do so:

## **DIY 1A - Installing Dependencies**

Phew, now that we have gotten the story of websockets out of the way, let's finally get our hands dirty. Have the following dependencies installed first:

Windows: ```$ pip install flask flask-socketio eventlet```
(Windows users please open cmd with admin privileges - we will only be issuing this reminder once!)

Mac: ```$ sudo pip3 install flask flask-socketio eventlet```
(Mac users please key in your password when prompted - your password will not show as you type it, so just do it carefully and hit ```enter``` when you are done - again we will only be issuing this reminder once!)

> **Mac Users, please note:**<br>
> If you encounter the following error when installing ```eventlet```: ```error: command '/usr/bin/clang' failed with exit status 1``` or the message that ```The "clang" command requires the command line developer tools, would you like to install now?```, please install clang as prompted by the Command Line Developer Tools program: click "Install", "Agree", "Continue on Battery Power" if applicable. Then, re-run the above pip install command again.

You MUST install ```eventlet```, we'll explain thoroughly later.

## **DIY 1B - Run Your Flask App**

On your Desktop, create a folder called ```CloudChat``` (this will be our working directory). Download ```hello_flask.py``` by right-clicking and saving the file [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/master/hello_flask.py) into said folder.

## **Checkpoint 1**

So you should have ```hello_flask.py``` in your ```CloudChat``` folder inside the ```CloudChat``` folder.

Your file directory should look like this:

```
/CloudChat
	/hello_flask.py
```

Then open your terminal and enter the following commands:

**Windows**
```
cd Desktop
cd CloudChat
python hello_flask.py
```

**Mac**
```
cd Desktop
cd CloudChat
python3 hello_flask.py
```

You should see this on your terminal:

```
* Restarting with stat
* Debugger is active!
* Debugger PIN: 244-459-407
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

 That means you're good to go! You can open up your browser (Chrome would be good), and navigate to ```http://127.0.0.1:5000/```. You should see ```Hello World!``` on the web page.

![1a.PNG](screenshots/1a.PNG?raw=true)

Notice how your terminal returns you the log of the endpoints accessed by your visitors. Try refreshing the page and see what happens. Do you notice a new log entry is created whenever you hit the page?

```
127.0.0.1 - - [30/Jan/2018 00:23:21] "GET / HTTP/1.1" 200 -
```

Once you are satisfied with your creation, hit ```CTRL``` + ```C``` a couple of times to quit the web app. Sometimes it takes a while for your terminal to kill the web app, so let's be patient if that happens.

## **Explaining Flask (```hello_flask.py```): A 5-min Crash Course**

```
from flask import Flask
```
Imports the ```Flask``` module

```
app = Flask(__name__)
```
Creates an instance of the class ```Flask``` for our web app called ```app```

```
__name__
```
A special variable that gets as value the string ```__main__``` when you’re executing the script (more on this later)

```
app.debug = True
```
is just a configuration for the Flask app. This sets our Flask app in debug mode so that we can, well, debug errors.

```
@app.route('/')
```
A decorator used to bind a function to a URL endpoint. It is also called a view or routing. Basically it tells Flask what to do when people hit that specified endpoint. If you have a domain ```http://www.example.com```, ```@app.route('/')``` is a view for ```http://www.example.com/```, while ```@app.route('/index')``` will be the view for ```http://www.example.com/index```.

```
def index():
```
The so-called function name of the view above

```
return "Hello World!"
```
What will be executed when someone access the endpoint correspondingly.

```
if __name__ == '__main__':
    app.run(debug=True)
```
Python assigns the name ```__main__``` to this script when it is executed. If the script is imported from another script, the script keeps it given name (e.g. another_script.py). In our case here, we are executing the script, thus ```__name__``` will be equal to ```__main__```. Since this if conditional is satisfied, the ```app.run()``` method will be executed which, well, runs the app by **starting the default Flask development server** (which is NOT meant for production). This technique allows the programmer to have control over script’s behavior. You can very well not have these two lines of code, but it is good practice and will save you trouble down the road when you have multiple scripts.

[Source 1: Miguel Grinberg](https://flask-socketio.readthedocs.io/en/latest/)

[Source 2](http://pythonhow.com/how-a-flask-app-works/)

For a more comprehensive understanding of how Flask works, check out the docs using [Reading 3](http://flask.pocoo.org/docs/0.12/quickstart/).

___

# **STEP 2 - Hello World Flask App with Web Sockets**

## **Overview**

Cool, now we can begin testing the blazing-fast websockets!

## **DIY 2A - Running Your Websockets Flask App (I)**

Let's download another script called ```hello_sockets.py``` by right-clicking and saving the file [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/master/hello_sockets.py) into our ```CloudChat``` folder.

Next, create a new folder in the ```CloudChat``` folder and name it ```templates```. Download ```hello_sockets.html``` into the ```templates``` folder by right-clicking and saving the file [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/master/templates/hello_sockets.html) into our ```templates``` folder.

## **Checkpoint 2**

So you should now have ```hello_flask.py``` and ```hello_sockets.py``` in your ```CloudChat``` folder.

In the ```templates``` sub-folder inside the ```CloudChat``` folder, it should contain ```hello_sockets.html```.

Your file directory should look like this:

```
/CloudChat
	/hello_flask.py
	/hello_sockets.py

	/templates
		/hello_sockets.html
```

## **DIY 2B - Running Your Websockets Flask App (II)**

Ready? Open your terminal and enter the following commands:
Windows: ```python hello_sockets.py```
Mac: ```python3 hello_sockets.py```

Then, open two browsers side by side and navigate both to ```http://127.0.0.1:5000/```. On both browsers, you can key in any message you wish in either fields and send them using their adjacents buttons ```Send to Self``` and ```Send to All```.

![2a.PNG](screenshots/2a.PNG?raw=true)

What do you notice?

As their names imply, clicking the ```Send to Self``` button fires the ```send_to_self``` event that is defined in ```hello_sockets.py``` which does not have the broadcast function turned on (```broadcast=True```) - thus you only send the message to yourself. ```Send to All``` is basically the opposite. More on ```broadcast``` later.

Once you are satisfied with your creation, hit ```CTRL``` + ```C``` a couple of times to quit the web app. Sometimes it takes a while for your terminal to kill the web app, so let's be patient if that happens.

Now we'll take some time to appreciate the code! Bear with me!

## **Introduction to Flask-SocketIO**

Before we explain anything else, let's introduce you to the magical ```Flask-SocketIO``` library first. ```Flask-SocketIO``` basically allows us to use websockets easily for Flask web apps, but it really is a lot more than that. Miguel Grinberg, the creator of said library, has got everything covered for you when you are using said library. Do let me explain:

First, not only does it enable websockets for Flask, it also works on browsers which do not support websockets by automagically switching to long-polling (and lets you know when it does so too). All this with dead-simple code and without having you to painfully account for such a compatibility (or to fix broken connections as well, I'm looking at you, long-polling).

Second, it supports not one, but three different web servers automagically again without you having to configure anything. ```Flask-SocketIO``` recommends ```eventlet``` as the web server and will use it if you have it installed (that's why we made it a point to do so when we were installing our packages using ```pip```). If not, it switches to ```gevent``` if you have it, and if both aren't available, it **defaults to the Flask developmental server** which is the one we used in ```hello_flask.py``` (and does NOT support websockets, and thus will automatically use long-polling which still works but defeats the purpose of this tutorial).

I'll leave you to marvel at how awesome this library is. It is in fact so easy to use that it is dangerous - you can totally forget about installing ```eventlet``` and your web app will still work in realtime, simply because ```Flask-SocketIO``` has already switched you to long-polling automatically - without you even realizing it.

## **Explaining Flask Sockets (```hello_sockets.py``` and ```hello_sockets.html```): A 5-min Crash Course**

Now that we know ```Flask-SocketIO``` is our current destination in our Pythonic library-hoppping journey, we can explore how it actually works in our code. Understanding how websockets work in the context of Flask is non-trivial but not difficult either.

Let's explore a couple of additions in ```hello_sockets.py``` first:

#### 1. New Additions from Flask

```
from flask import Flask, render_template, session, request
```
A couple more methods that we import from Flask.

```
app.config['SECRET_KEY'] = 'obviously not a good secret key'
```
Additional configuration for us to set the secret key for our Flask ```session```, which is one of the new objects we have imported from Flask, more on this later.

```
return render_template('hello_sockets.html')
```
From the Docs: Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the HTML escaping on your own to keep the application secure. Because of that Flask configures the ```Jinja2``` template engine for you automatically. To render a template you can use the ```render_template()``` method. All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments. In this case, when a user accesses the ```/``` endpoint, Flask will return and render our HTML template ```hello_sockets.html```.

```
session['receive_count'] = session.get('receive_count', 0) + 1
```
Remember we set the secret key of our Flask web app? Think of a session like a cookie, just that Flask signs this cookie cryptographically using your secret key. What this means is that the user could look at the contents of your cookie but not modify it, unless they know the secret key used for signing. Sessions are however not to be used to store highly-sensitive private information, because they still can be decoded fairly easily without your secret key. As an example, ```session['my_session_name'] = "data_that_i_want_to_store"``` creates a session named ```my_session_name``` for a client and stores the string ```data_that_i_want_to_store``` inside it. You can access said session by using the ```get()``` method.

#### 2. New Additions from Python

```
get()
```
This is actually a method in Python and not that in Flask. When ```get()``` is called, Python checks if the specified key exists in the dictionary. If it does, then ```get()``` returns the value of that key. If the key does not exist, then ```get()``` returns the value specified in the second argument to get(). Flask sessions thus store data like a Pythonic dictionary.

## **Quiz 1**

Let's take a look at this ```session.get('receive_count', 0)```. Can you now figure out what this means? You can use [Reading 4](https://blog.miguelgrinberg.com/post/flask-socketio-and-the-user-session) to help you out.

> **Answer:**<br>
> **If Python can find the receive_count key in session, it will use the value as it is. Else, it will just assign it as the value 0 as specified.**

___

```
    import pip

    installed_packages = pip.get_installed_distributions()
    package_names = [package.project_name for package in installed_packages]

    print ('\nEVENTLET STATUS:')

    if not 'eventlet' in package_names:
        print ('eventlet not installed, aborting... please install using $ pip install eventlet\n')
    else:
        print ('eventlet is installed - you are good to go!\n')
```
What on earth is this huge chunk of code residing at the bottom of the script? This snippet just checks whether you have ```eventlet``` installed, and will also echo its status in your terminal. This nasty snippet prevents you from running the app without ```eventlet```. Again, our app can probably work without ```eventlet``` installed and automatically use long-polling, but that's exactly what we do not want it to do. Is the snippet necessary? No. But does it make sure we are all on the same page? Heck yeah, screw long-polling!

#### 3. New Additions from Flask-SocketIO

This is the core of this workshop - let's figure out what everything does:

```
from flask_socketio import SocketIO, emit, disconnect
```
You would've guessed it, we're going to import some modules from the ```flask_socketio``` library.

```
socketio = SocketIO(app)
```
This binds ```socketio``` to our Flask app so that we can manipulate it.

**(A) Receiving Messages**
```
@socketio.on(your_event_name, namespace='/your_name_space')
```
This is the standard SocketIO syntax to define an event handler that allows you to define an event name as well as the namespace as it can run in. It looks pretty similar to the app route decorator in Flask, doesn't it? You can thus think of this as a view that your client accesses, just that instead of accessing a URL endpoint in Flask, you are accessing an event (in a namespace if given). What do all these mean?

**TL;DR** - ```@socketio.on(your_event_name, namespace='/your_name_space')``` is basically an event listener that receives messages; in this case, it just listens when the event ```your_event_name``` is fired and it will run the code under its corresponding function. The most common use in websockets would simply be for the server to listen to an event fired by the client and then do something (usually returning some data back). The reverse also applies.

The first argument to the decorator, ```your_event_name```, is of course, your custom event name.
> **From the docs**<br>
> Event names 'connect', 'disconnect', 'message' and 'json' are special events generated by SocketIO. Any other event names are considered custom events.

The second argument ```namespace='/your_name_space'``` is optional and lets you specify the namespace in which your event will run. Think of namespace as a specific chatroom in which you allow your event to run, i.e. this event will only run in the specified chatroom. If you do not define the namespace, the event will be allowed to be attached to the default global namespace (i.e. any chatroom/namespace will have access to it).

> **From the docs**<br>
> Events can be defined inside a namespace by adding the namespace optional argument to the ```socketio.on``` decorator. Namespaces allow a client to open multiple connections to the server that are multiplexed on a single socket. When a namespace is not specified the events are attached to the default global namespace.<br>
> More accurately, when a namespace is not defined a default global namespace with the name '/' is used. So your events without a namespace defined can access said global namespace if you do not specify a "chatroom name".

## **Quiz 2**

If this event handler, ```@socketio.on('my_event')```, is a custom named event, then why are ```@socketio.on('message')``` and ```@socketio.on('json')``` unnamed events even though they follow the same syntax?
> **Hint:**<br>
> **Check the docs under "Receiving Messages".**<br>

> **Answer:**<br>
> **Events with the reserved event names of ```'message'``` and ```'json'``` are special events generated by SocketIO. Any other event names are considered custom events.**

___

**(B) Sending Messages**

```
send()
emit()
```
SocketIO event handlers defined as shown in the previous section can send reply messages to the connected client using the ```send()``` and ```emit()``` functions. However, in this workshop, to send events between our server and the client, and vice versa, we will be using the ```emit()``` function provided by Flask-SocketIO to send a message (under a custom event name).

The ```emit()``` method can take several arguments. The first is the event name that you want to call. The second is the data that you want to send to the event you called, and is (usually) in JSON format. There are other optional parameters that you can input as well in the arguments that follow, and we will be using the ```broadcast``` parameter - ```broadcast = True``` means that the data you fire will be sent to everyone in the namespace/chatroom.

Example:
```
emit('display_message',
    {
    	'data': 'this is my message',
    	'count': 20,
    },
    broadcast=True)
```

For instance, in this ```emit()``` method, we first call the event ```'display_message'```, and we deliver the data in JSON format and lastly, we broadcast it to the entire namespace/chatroom.

## **Quiz 3**

What is ```send()``` used for, and why do we not use it here?

> **Hint:**<br>
> **Check the docs under "Sending Messages".**

> **Answer:**<br>
> **Well the answer is already found above. ```send()``` is used only for reserved unnamed events only, viz. ```'message'``` and ```'json'```. ```emit()``` on the other hand is for named events. All our events are custom named events, thus we use only ```emit()```.**

## **Quiz 4**

Is it right to say that ```@socketio.on('connect', namespace='/test')``` is an unnamed event? If so, why do we still use ```emit()``` instead of ```send()```?

> **Answer:**<br>
> **Do not be confused. ```emit()``` is for you to call and fire custom named events in its arguments, not the name of the event handler! In this case, we look at ```emit('display_message', {'data': 'Connected', 'count': 0})```, not the event handler. ```display_message``` is a custom-named event, thus it is correct to use ```emit()```. Admittedly, the docs isn't very clear on this.**

___

```
def test_connect():
    emit('display_message', {'data': 'Connected', 'count': 0})
```
Similar to the Flask syntax, the former defines the function name of the event handler above itself, and the latter is whatever code that you want to run when the event handler is fired.

```
socketio.run(app)
```
The eagle-eyed would have noticed that Flask's ```app.run()``` has been replaced by Flask-SocketIO's ```socketio.run(app)```. We'll have Miguel Grinberg explain this:
> Note the way the web server is started. The ```socketio.run()``` function encapsulates the start up of the web server and replaces the ```app.run()``` standard Flask development server start up. **When the application is in debug mode the Werkzeug development server (Flask's default server) is still used and configured properly inside ```socketio.run()```.** In production mode, the ```eventlet``` web server is used if available, else the ```gevent``` web server is used. If ```eventlet``` and ```gevent``` are not installed, the Werkzeug development web server is used.

Wow, wait a minute.

> **When the application is in debug mode the Werkzeug development server (Flask's default server) is still used and configured properly inside ```socketio.run()```.**

We'd better switch off our app's debug mode (by setting ```app.debug = False```) when we are done with exploring how everything works!

#### 4. New File: ```hello_sockets.html``` in ```templates``` folder

Ayy one more file to go through? Goodness gracious. Let's keep this brief and talk just about JS mainly; this file's just HTML and JS and doesn't even have CSS.

```
<script type="text/javascript" src="//code.jquery.com/jquery-1.4.2.min.js"></script>
<script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.5/socket.io.min.js"></script>
```
Our dependencies.

```
(document).ready(function() {
```
We wait for our page to be ready.

```
namespace = '/test';
```
We use ```test``` as our namespace/chatroom name.

```
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
```
We connect to our server. In the entire script, it is worth noting that **this is the only line of code that is "fired" upon page ready**, other than assigning ```namespace``` as ```/test```. This automatically fires the default ```connect``` event.

```
socket.on('connect', function() {
    socket.emit('send_to_self', {data: 'I\'m connected!'});
});
```
Notice how similar this is to our Python file? This is the event handler written in JS that listens to the ```connect``` event, and calls the ```send_to_self``` event defined in ```hello_sockets.py``` and sends the message of ```I'm connected``` along with it.

## **Quiz 5**

Why are there two ```connect``` events? There was one in ```hello_sockets.py``` and another in our client's ```hello_sockets.html``` JS?
> **Hint:**<br>
> **What is logged on the web page when you establish a new connection (by navigating to ```http://127.0.0.1:5000/```)?**<br>
> **Answer:**<br>
> **Turns out you can have have two events with the same name, with one being defined in the server code, and the other in the client code. When such an event is called, both sides will listen to it and fire whatever code is defined for that event! That's why your first two messages will be ```Connected``` that is fired from ```hello_sockets.py``` and ```I'm connected!``` from ```hello_sockets.html```.**

> *Note:*<br>
> *While it may not necessarily be bad practice to share the same function names across multiple languages in the same coding environment, in this case sharing the same event (variable) name can easily lead to confusion. We are just demonstrating the possibility of such a behaviour here, and we recommend that you emit two differently-named events to call two events instead of having them share the same name.*

___

```
socket.on('display_message', function(msg) {
    $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
});
```

Can you figure this out yourself? This is another event handler that listens for the ```display_message``` event to be fired, and executes the following: inserting a new HTML ```<div>``` element which reflects the message received into the client's web page.

```
$('form#push_all').submit(function(event) {
    socket.emit('send_to_all', {data: $('#push_all_data').val()});
    return false;
```

In the above, ```val()``` gets the value of the HTML element. We also use ```return false``` to prevent the entire form to be actually submitted and from the page from refreshing.

> **Note on ```return false```:**<br>
> Often, in event handlers, such as ```onsubmit``` (as is our case), returning false is a way to tell the event to not actually fire. So, say, in the ```onsubmit``` case, using ```return false``` would mean that the form is not submitted. This is particularly good if you want an AJAX form that submits without reloading the page - but also works by submitting and reloading the page when javascript is not available. While easy to implement, it may not be the best method to achieve such an objective, but that is beyond the scope of this tutorial.<br>
> [Source](https://stackoverflow.com/a/855376)


___

# **STEP 3 - Our Final Flask Chat App with Web Sockets**

## **Overview**

Now that we all have a better idea of how Flask-SocketIO works, let's launch a CSS-polished, feature-packed, and production-ready chat app! (Kind of.)

We will be disabling debug mode for our Flask app, so that we can use eventlet and unleash the power of websockets. We will also do a little indirect experiment to see how websockets fare v. long-polling. That'll be Step 4 in just a bit.

## **DIY 3A - Running Your Polished Websockets Flask App (I)**

Let's download our very last script called ```app.py``` by right-clicking and saving the file [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/master/app.py) into our ```CloudChat``` folder.

Next, create a new folder in the ```CloudChat``` folder and name it ```static```. This folder is used to store our static files like JS and CSS. Download 3 things: ```favicon.ico```, ```cloud.PNG``` and ```style.css``` into this ```static``` folder by right-clicking and saving the files [here](https://github.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/raw/master/static/favicon.ico) and [here](https://github.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/raw/master/static/cloud.png) and [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/master/static/style.css) into our ```static``` folder.

Lastly, in our ```templates``` folder found in the ```CloudChat``` folder that we created earlier, download ```app.html``` into this ```templates``` folder by right-clicking and saving the file [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/master/templates/app.html) into our ```templates``` folder.

## **Checkpoint 3**

So you should now have ```hello_flask.py```, ```hello_sockets.py``` and ```app.py``` in your ```CloudChat``` folder.

In the ```static``` sub-folder within ```CloudChat```, you should have ```favicon.ico```, ```cloud.PNG``` and ```style.css```.

Lastly, in the ```templates``` sub-folder of ```CloudChat```, it should contain ```hello_sockets.html``` and ```app.html```.

Your file directory should look something like this:

```
/CloudChat

	/hello_flask.py
	/hello_sockets.py
	/app.py

	/templates
		/hello_sockets.html
		/app.html

	/static
		/favicon.ico
		/style.css
		/cloud.PNG
```

## **DIY 3B - Running Your Polished Websockets Flask App (II)**

Ready? Open your terminal and enter the following commands:
Windows: ```python app.py```
Mac: ```python3 app.py```

Then, open two browsers side by side and navigate both to ```http://127.0.0.1:5000/```. On both browsers, you can enter a unique nickname and start chatting (sadly, with yourself only for now, but we will expose it to the world later, stay tuned)!

![3a.PNG](screenshots/3a.PNG?raw=true)
![3b.PNG](screenshots/3b.PNG?raw=true)

Once you are satisfied with your creation, hit ```CTRL``` + ```C``` a couple of times to quit the web app. Sometimes it takes a while for your terminal to kill the web app, so let's be patient if that happens.

So what's new this time?

Other than a few cosmetic changes by finally having legit CSS, there are a couple of features worthy of mention, such as inputting your nickname, getting your nickname color through a hex operation, and reflecting whether a user is typing or not just like a real chat app!

## **Explanation of ```app.py``` and ```app.html```**

#### **Summary**

Because these new features are beyond the scope of this workshop, we will just be explaining them briefly and verbally. But before that, we invite you to browse through the new files, and figure out how things work out now. The workflow of the Flask websockets should still be the same, just that now we have a bit more JS magic and a few more events (such as ```typing``` and ```stop typing```).

## **DIY 3C - Exploring the Event Sequences & Workflow**

Do try! After ```var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);```, what happens now? Which events fire which events? What triggers these events? Which events reside on server code, and which on client code?

Lastly, and most importantly, we have now disabled debugging mode on our Flask app, and we are now using ```eventlet``` as our server.

___

# **STEP 4 - Exposing our Chat App to the Whole World and to our Friends!**

## **Overview**

Finally! The most exciting part of this workshop so far. We will be using ```ngrok``` to securely tunnel your ```eventlet``` web server to the world!

## **Download ```ngrok```**

Let's download ```ngrok``` [here](https://ngrok.com/download) first and extract the ```ngrok``` executable program into your ```CloudChat``` folder. Mac users, upon unzipping the downloaded zip, can drag ```ngrok``` into the ```CloudChat``` folder.

Alternatively, you can download the ```ngrok``` executable uploaded on this repo, but the most updated one for your machine is probably on ```ngrok```'s main page.

## **Checkpoint 4**

Here's our final checkpoint. Let's check if you have a working directory like this:
```
/CloudChat

	/hello_flask.py
	/hello_sockets.py
	/app.py
	/ngrok

	/templates
		/hello_sockets.html
		/app.html

	/static
		/favicon.ico
		/style.css
		/cloud.PNG
```

![4a.PNG](screenshots/4a.PNG?raw=true)

## **DIY 4A - Running Our Polished App Again**

We'll launch our chat app first:

Windows: ```python app.py```
Mac: ```python3 app.py```

Let's open one browser and navigate to ```127.0.0.1:5000``` just to make sure things are fine. You can enter a nickname and enter the chatroom.

Now is the coolest part yet - publishing your chat app to the whole world by using ```ngrok```! Just double-click the ```ngrok``` executable and a terminal-like program will pop up.

> **Mac users, please note:**<br>
> Getting the message that ```"ngrok" can't be opened because it is from an unidentified developer```? Simply avoid double-clicking the file. Instead, right-click on ```ngrok``` and then click ```Open``` twice.
> If you ngrok opens but only says ```[Process Completed]``` and disallows you from typing anything, there is unfortunately no easy way for you to get rid of this error other than by updating your OS. You will thus be unable to use eventlet, but you can still continue with the workshop and your app can remain fully functional - you just won't be able to securely tunnel it to the world, that's all.

![4b.PNG](screenshots/4b.PNG?raw=true)

## **DIY 4B - Launching on ```ngrok```!**

In ```ngrok```, execute this:

```
ngrok http -bind-tls=false 5000
```

> This gets ngrok to listen on a HTTP-only tunnel endpoint. We need to do this to prevent the ```unsafe script``` warning from flashing when we access this, since ```Flask-SocketIO``` currently only supports websockets over HTTP and not HTTPS. ```ngrok``` by default will forward HTTPS traffic, thus we need to explicitly tell it not to do it and use HTTP instead.

![4i.PNG](screenshots/4i.PNG?raw=true)

Copy the forwarding address. This is your temporary web URL to your chat app that everyone can now access! Try navigating to your ```ngrok.io``` address! Let's share with one another our ```ngrok``` addresses and chat with one another!

How do we know that we are actually utilising websockets? ```ngrok```'s console will tell you so: ```101 Switching Protocols``` is the same as establishing a ```101 Web Socket Protocol Handshake```  according to [here](https://tools.ietf.org/html/rfc6455) and [here](https://ngrok.com/docs#bind-tls) and [here](https://stackoverflow.com/a/22418369).

![4j.PNG](screenshots/4j.PNG?raw=true)

To shut down the ```ngrok``` tunnel, you can hit ```CTRL``` + ```C``` just like how you do the same in your terminal.

___

# **STEP 5 - The Curious Case of Websockets v. Long-Polling**

## **Overview**

Remember we talked about conducting a little experiment? Don't just hear from us, if you would like to find out for yourself how websockets stacks against long-polling, let's do this together!

## **Uninstalling ```eventlet```**

Wait what? Uninstalling ```eventlet```?

That's right. Because there's no other simpler way to do it and because we have run out of time to write a bandwidth connection test, we will be uninstalling ```eventlet``` to see how much higher the consumption of bandwidth for long-polling v. websockets.

Don't worry we can always reinstall later.

## **DIY 5A - Uninstalling ```eventlet```**

In your terminal, execute:

Windows: ```$ pip uninstall eventlet``` and key in ```y``` and hit ```enter``` when prompted
(Windows users please open cmd with admin privileges)

Mac: ```$ sudo pip3 uninstall eventlet``` and key in ```y``` and hit ```enter``` when prompted
(Mac users please key in your password when prompted - your password will not show as you type it, so just do it carefully and hit ```enter``` when you are done)

Download ```bandwidth_test.py``` into your ```CloudChat``` folder by right-clicking [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-FlaskWebSocketChatApp/master/bandwidth_test.py) and saving it.

In your terminal, execute: ```python bandwidth_test.py``` for Windows or ```python3 bandwidth_test.py``` on Mac

Then open ```ngrok```, and execute: ```ngrok http -bind-tls=false 5000```

Copy the ```ngrok.io``` address assigned to you. Open two browsers and navigate to the address. Just try to continuously type some random stuff into the input box for 30 seconds to 1 minute. You should be able to send a few messages before nothing works anymore. You can get your friends to try to access your address but chances are they won't be able to do it. Try refreshing the web page. Do you get this?

![5a.PNG](screenshots/5a.PNG?raw=true)

What? Too Many Connections? Tunnel session violated the rate-limit policy on free accounts?

Let's dive into the problem by taking a look at the logs on our terminal:

![5b.PNG](screenshots/5b.PNG?raw=true)

Goodness gracious - look at the frequency and number of requests you are firing when you use long-polling! No wonder we would have violated the connection rate-limit in such a short span of time. Long-polling, _you gotta up your game_!

## **Results of Bandwidth Connection Comparison**

Websockets, 1. Long-polling, 0.

Websockets is the winner!

## **DIY 5B - One Last Thing: Reinstalling ```eventlet```**

Now let's all remember to reinstall ```eventlet``` so that we can avoid the long-polling disaster for good.

For one last time, execute in your terminal:

Windows: ```$ pip install eventlet``` and key in ```y``` and hit ```enter``` when prompted
(Windows users please open cmd with admin privileges)

Mac: ```$ sudo pip3 install eventlet``` and key in ```y``` and hit ```enter``` when prompted
(Mac users please key in your password when prompted - your password will not show as you type it, so just do it carefully and hit ```enter``` when you are done)

___

# **The End!**

## **Closing Remarks**

That's all we have for this workshop. Go forth and create your realtime duplex web apps with websockets & Flask!

## **More Resources**

If you need more information, it probably is in the Python, Flask, or Flask-SocketIO docs.

___

## **Sources**

- Flask-SocketIO Docs
- Flask Docs
- Miguel Grinberg
- Stackoverflow
- Python Docs
- Github (sirkaiserkai)

## **Acknowledgements**

Explanations of how our code works is largely borrowed directly or indirectly from the docs or its authors.

The files ```hello_sockets.py``` and ```hello_sockets.html``` are largely adapted directly from [this Github repo](https://github.com/sirkaiserkai/Flask-SocketIO-Chat) by user ```sirkaiserkai```.

We claim no credit to any resources not belonging to us in our course of writing and conducting this free workshop.

## **Missing References?**

This workshop is based on extensive research on websockets, Flask, Flask-SocketIO and Python. We had to have so many references to make sure our content is as technically correct as possible; please forgive us if we have accidentally missed referencing a source or two. We promise to update our references accordingly. Cheers!

___

## Test Info

This tutorial has been tested using a Windows 7 computer running Home Premium SP1 and a MacBook Air running OS X Version 10.9.5. Both are run on Python 3.6.3. It is accurate as of 30 January 2018.

## Acknowledgements

Many thanks to [Chang Kai Lin, Ries](https://www.instagram.com/kailinchanggg/) for sacrificing her MacBook Air and loaning it to me indefinitely for testing, and the [NTU Open Source Society](https://github.com/ntuoss) committee for making this happen!

![ntuoss_logo.png](screenshots/ntuoss_logo.png?raw=true)
