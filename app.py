from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.debug = True # use this when testing
# app.debug = False # use this to fully use websockets
app.config['SECRET_KEY'] = 'obviously not a good secret key'
socketio = SocketIO(app)

usernames = {}
number_of_users = 0


@app.route('/')
def index():
	return render_template('app.html')


# When the client emits 'connection', this listens and executes
# @socketio.on('connection', namespace='/chat')
# def user_connected():
# 	print('User connected')


# When the client emits 'new message', this listens and executes
@socketio.on('new message', namespace='/chat')
def new_message(data):
	emit('new message',
		{ 'username' : session['username'],
	 	'message': data }, broadcast=True ) # When a message is sent with the broadcast option enabled, all clients connected to the namespace receive it, including the sender.


# When client emits 'add user' this listens and executes
@socketio.on('add user', namespace='/chat')
def add_user(data):
	print('Adding User')
	global usernames
	global number_of_users

	session['username'] = data
	usernames[data] = session['username']

	number_of_users += 1;

	emit('login', { 'numUsers' : number_of_users })
	emit('user joined', { 'username' : session['username'], 'numUsers': number_of_users }, broadcast=True)


@socketio.on('typing', namespace='/chat')
def typing_response():
	try:
		emit('typing', { 'username' : session['username'] }, broadcast=True )
	except:
		pass


@socketio.on('stop typing', namespace='/chat')
def stop_typing():
	try:
		emit('stop typing', { 'username' : session['username'] }, broadcast = True)
	except:
		pass


# @socketio.on('disconnect', namespace='/chat')
# def disconnect():
# 	global usernames
# 	global number_of_users


# 	try:
# 		del usernames[session['username']] # deleting the username session as well as the binding from namespace
# 		number_of_users -= 1
# 		emit('user left', { 'username' : session['username'], 'numUsers' : number_of_users}, broadcast=True)

# 	except:
# 		pass



if __name__ == '__main__':

    import pip

    installed_packages = pip.get_installed_distributions()
    package_names = [package.project_name for package in installed_packages]

    print ('\nEVENTLET STATUS:')

    if not 'eventlet' in package_names:
        print ('eventlet not installed, aborting... please install using $ pip install eventlet\n')
    else:
        print ('eventlet is installed - you are good to go!\n')
        socketio.run(app)
