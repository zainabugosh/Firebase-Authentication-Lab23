from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyAW7Rc6pksoMmbFMZJxx7Q7VpjWmxfaLEs",
  "authDomain": "test-390f8.firebaseapp.com",
  "projectId": "test-390f8",
  "storageBucket": "test-390f8.appspot.com",
  "messagingSenderId": "362241665308",
  "appId": "1:362241665308:web:86929ab39f335ffc3bf2d9",
  "measurementId": "G-GD2022T6MS",
  "databaseURL": "https://test-390f8-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")
	


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		bio=request.form['bio']
		Username=request.form['Username']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user={'name':Username,'email':email,'bio':bio,'password':password}
			UID = login_session['user']['localId']
			db.child("Users").child(UID).set(user)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signup.html")

@app.route('/all_tweets')
def tweeta():
	tweeta=db.child("tweets").get().val(	)
	return render_template("tweets.html",tweeta=tweeta)


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		tex=request.form["text"]
		title=request.form["title"]
		
		try:
			UID = login_session['user']['localId']
			tweet={'uid':UID,'text':tex,"titel":title}
			db.child("tweets").push(tweet)
		except:
			return redirect(url_for('add_tweet'))
	return render_template("add_tweet.html")


if __name__ == '__main__':
	app.run(debug=True)