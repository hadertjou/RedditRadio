import praw
import pdb
import re
import os
import json
import sys
import time
from app import db, app, celery
#from app.dbProc import insertParagraph, getParagraph
import dbProc
from app.models import Paragraph, User


user_agent = ('StoryTime Reader v1.0 (/u/storytimereader)')
r = praw.Reddit(user_agent = user_agent)
r.config.store_json_result = True
re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)

@celery.task
def readPosts(subname, person, threadCount):
	subreddit = r.get_subreddit(subname)
	tC = threadCount

	firstpage = subreddit.get_hot(limit=tC);
	pp = db.session.query(User).filter_by(username=person).first()
	print "PP: ", pp.username
	print "pp object: ", pp
	for submission in firstpage:
		print "Title: ", submission.title
		print "Text: ", submission.selftext	
		title = Paragraph(text=submission.title)
		print "title text added"
		title.writer = pp
		dbProc.insertParagraph(title)
		print "writer attached"
		if submission.selftext:
			desc = Paragraph(text=submission.selftext)
			desc.writer = pp
			dbProc.insertParagraph(desc)
	
		db.session.commit()
		submission.replace_more_comments(limit=64, threshold=10)
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		#flat_comments.sort(key=lambda comment: comment.score, reverse=True)
		for comment in flat_comments:
			jcomment = comment.body
			commentsend = re_pattern.sub(u'\uFFFD', jcomment)
			#commentsend = commentsend.replace("\\n", "")
			commentsend = re.sub("[\n\r]+", "", commentsend)
			#commentsend = commentsend.encode('ISO8859-1')
			para = Paragraph(text=commentsend.encode('utf8'))
			#para = Paragraph(text=jcomment.encode('utf8', errors='ignore'))
			para.writer = pp
			try:
				dbProc.insertParagraph(para)
			except Exception as e:
				print "exception during paragraph add: ", e
				continue 

		#db.session.commit()

