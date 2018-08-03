#!/usr/bin/python  

from flask import Flask, render_template, request, Response
from flask import Flask, jsonify, abort, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
from collections import OrderedDict
import json
import hashlib
from dbfunctions import *
 
app = Flask(__name__, static_url_path = "")

auth = HTTPBasicAuth()
 
@app.route("/")
@app.route("/index")
@auth.login_required
def index():
    return render_template('index.html')
 
@app.route("/todos.json")
def todos_json():
	toDos = getAllToDos('')
	resultJsonStr = json.JSONEncoder().encode(toDos) 
	resp = Response(resultJsonStr.encode(), status=200, mimetype='application/json')
	return resp

@app.route("/todos", methods=[ 'POST'])
def todos():
	task = dict(request.form)

	# 'tags' was passed in with the [] appended to it, so need to strip it off
	# to become the item label of 'tags'
	if 'tags[]' in task:
		task['tags'] = task.pop('tags[]')
		
	# 'description' is passed in as an array with a single value
	# Need to convert to just a single value instead of as an array 
	if 'description' in task:
		task['description'] = task['description'][0]
	
	createRecordFromOneToManyDict(**task)
	
	# return the updated task list
	return todos_json()

# following code adapted from example at 
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

@auth.get_password
def get_password(username):
	dbPwd = getPwd(username)
	return dbPwd
 
@auth.hash_password
def hash_pw(password):
	pwd = hashlib.sha512(str.encode(password)).hexdigest()
	return pwd
	
@auth.error_handler
def unauthorized():
	return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

def make_public_task(task):
	new_task = {}
	for field in task:
		if field == 'id':
			new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
		else:
			new_task[field] = task[field]
	return new_task
    
@app.route('/todos/api/v1.0/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
	toDos = getAllToDos("")
	resultJsonStr = json.JSONEncoder().encode(toDos) 
	resp = Response(resultJsonStr.encode(), status=200, mimetype='application/json')
	return resp
 
@app.route('/todos/api/v1.0/tasks/<description>', methods = ['GET'])
@auth.login_required
def get_task(description):
	toDos = getAllToDos(description)

	## the following 'if' check actually won't work. If there is no task in the database with the 
	## provided description, it will return an array with one empty item (empty description and empty tags)
	## so len(toDos) returns 1.

	## For lab, revise the following 'if' statement to make it abort on '404' properly when no tasks with the given
	## descripion can be found, i.e., the return will display {'error': 'Not found'} which is the error handling 
	## behavior defined above.

	if len(toDos) == 1:
	    if toDos[0]['description']=='':
	        abort(404)
	resultJsonStr = json.JSONEncoder().encode(toDos) 
	resp = Response(resultJsonStr.encode(), status=200, mimetype='application/json')
	return resp

# see example at https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask	
# test: curl -u mickey:pwd12345 -i -H "Content-Type: application/json" -X POST -d '{"description":"do dishes", "tags":["chores"]}' http://localhost:8080/todos/api/v1.0/tasks 
@app.route('/todos/api/v1.0/tasks', methods = ['POST'])
@auth.login_required
def create_task():
	desc = request.json['description']
	tags = request.json['tags']
	task = {"description":desc, "tags":tags}
	createRecordFromOneToManyDict(**task)
	return jsonify({'task':make_public_task(task)}) ,201

	## for lab, you are to implement this function, 
	## use the db function of 	createRecordFromOneToManyDict(<the task>) to 
	##		add the task to the database
	## and return the toDo item created with status of 201
 
     
@app.route('/todos/api/v1.0/tasks/<description>', methods = ['DELETE'])
@auth.login_required
def delete_task(description):
	print("to delete: %s" % description)
	deleteToDo(description)
	return jsonify( { 'result': True } )

	
# used for debugging in development only!  NOT for production!!!
if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=5000)