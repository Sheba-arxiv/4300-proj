import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = ""
MYSQL_PORT = 3306
MYSQL_DATABASE = "fullnewsdb"

mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded, 
# but if you decide to use SQLAlchemy ORM framework, 
# there's a much better and cleaner way to do this


#Takes in the tuple array of top k searches from the generalized jaccard similarity, and returns the top k titles of articles in an array 
def sql_jaccard_search(top_k_searches):
    titles_arr = []
    for tup in top_k_searches:
        article_index = tup[0]
        sql_article = f"""SELECT title FROM mytable WHERE FIELD1 = {article_index}"""
        data = mysql_engine.query_selector(sql_article)
        titles_arr.append(data)
        
    return titles_arr

    

@app.route("/")
def home():
    return render_template('index.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("text")
    return sql_search(text)

app.run(debug=True)



def sql_search(episode):
    query_sql = f"""SELECT * FROM episodes WHERE LOWER( title ) LIKE '%%{episode.lower()}%%' limit 10"""
    keys = ["id","title","descr"]
    data = mysql_engine.query_selector(query_sql)
    return json.dumps([dict(zip(keys,i)) for i in data])
