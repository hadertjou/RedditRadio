# RedditRadio



Reddit Radio uses the PRAW reddit API to crawl reddit for posts in logical order. All posts are saved in MySQL database. When they are called to be read, they are deleted from db.

Vocalization uses ResponsiveVoice API.

____________________________________

Development version of RedditRadio. To run, clone to a new directory. It is recommended that you work in a Virtualenv.

After install and activating a virtualenv, run:

pip install -r requirements.txt

This will install proper versions of all dependencies. You must also install Redis message broker and Celery message queue. 

In __init__.py, edit config variables for Celery and MySQL.

Start celery worker with:

celery worker -A app.celery

and Redis Server.

run.py starts application at localhost 127.0.0.1:5000





