import flask
import sqlite3
from flask import request, jsonify
from setup import connect_db

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#List  all value in database
database = ".\\database\\user_info.db"
connection, cursor = connect_db(database)

connection.close()

@app.route('/history', methods=['GET'])
def history():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()