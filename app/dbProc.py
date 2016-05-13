from app import db
from app.models import User, Paragraph


def addUser(un, em, pa):
#if username exists in table
#already created
#exists = User.query.filter_by()
	person = db.session.query(User).filter_by(username=un).first()
	if person:
		return 0
	else: #if unique
		person = User(username=un, email=em, password=pa)
		db.session.add(person)
		db.session.commit()
		return 1

def validateUser(em):
	person = db.session.query(User).filter_by(email=em).first()
	return person

#will insert nmw, passage is a Paragraph object
def insertParagraph(passage):
	db.session.add(passage)
	db.session.commit()

#need to check if None or valid in calling func
def getParagraph(personObj):
#grab ONE pargraph (first())
	para = db.session.query(Paragraph).filter_by(writer=personObj).first()
	return para

def deleteParagraph(para):
	#para.delete()
	db.session.delete(para)
	db.session.commit()

#Gets person OBJECT for use with dbProc and queries using username string
def getPerson(name):
	person = db.session.query(User).filter_by(username=name).first()
	return person

#removes all paragraph entries in DB made by personObj
def flushAll(personObj):
	db.session.query(Paragraph).filter_by(writer=personObj).delete()
	db.session.commit()
	return 0
