from app import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, Unicode
#db.session.add(tbl_user('nametest', 'usernametest', 'emailtest'))

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=True)
	email = db.Column(db.Unicode(255), unique=True)
	password = db.Column(db.Unicode(255), unique=True)
	paragraphs = db.relationship('Paragraph', backref='writer', lazy='dynamic')

	def __init__(self, username, email, password):
		#self.id = id
		self.username = username
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User %r>' % (self.username)

class Paragraph(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.UnicodeText)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	#username = db.Column(db.varchar(255))

	def __init__(self, text):#, user_id):
		#self.id = id
		self.text = text
		#self.user_id = user_id
		

	def __repr__(self):
		return '<Text %r>' % (self.text)