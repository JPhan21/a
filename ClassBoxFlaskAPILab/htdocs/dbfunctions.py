# Connect to the database.
import sys
import pymysql
from collections import OrderedDict

# pymysql.connect() makeConnection():
def makeConnection():
	# this dbconfig.txt file must be present in the current dir with 
	# read permission to the account group that can access the dir.  
	# The file is populated with the db connection credential info, 
	# but ignored in the git so won't be part of the git repository.
	# File format is 4 lines:
	# dbname  e.g. amazeriffic
	# db login user name
	# db password
	# host name e.g. localhost, or https://...
   	
	file = open(sys.path[0]+"/dbconfig.txt", "r")   
	dbStr = file.readline().strip() 
	userStr = file.readline().strip() 
	passwdStr = file.readline().strip() 
	hostStr = file.readline().strip() 

	conn = pymysql.connect(
		db=dbStr,
		user=userStr,
		passwd=passwdStr,
		host=hostStr)	 

	return conn

# void createRecordFromOneToManyDict(**dataSet):
# dataset is a dictionary: item 'dictionary' should have a single value as  the value
# item 'tags' is an array of one or more items
def createRecordFromOneToManyDict(**dataSet):
	conn = makeConnection()
	c = conn.cursor()
		
	oneLabel = dataSet['description']	
		
	tags = dataSet['tags']	
	for e in tags:
		query = "CALL create_todos (1, '%s', '%s');" % (oneLabel, e.strip())
		c.execute(query)
			
	conn.commit()
	conn.close()


# [] readRecords():	
def readRecords(description):
	conn = makeConnection()
	c = conn.cursor()	

	# Print the contents of the db table.
	print("call get_todos(1, %s) ;" % description)
	c.execute("call get_todos(1, '%s') ;" % description)	

	# Fetch all the rows in a list of lists.
	results = c.fetchall()

	tasks = []
	for i, r in enumerate(results):
		tasks.append([ r[0], r[1]])
# 		print ("%d: %s, %s <br>" % (i+1,  r[0], r[1]))		# for debug trace

	conn.close()	
	return tasks

# ---- for testing and debugging ----	
# allTasks = fetchRecords()
# 
# print("allTasks:")
# print(allTasks)
#
# ---- end for testing and debugging ----	
 
# [] getAllToDos():
# convert the records from SQL db table into array of dictionaries of 
# task description and the corresponding set of tags - the original node.js code toDos' sturcture:
def getAllToDos(description):
	allTasks = readRecords(description)

	allToDos = []
	task = {}
	tags = []
	desc = ""

	for d in allTasks:
		if d[0] != desc:
			if not(desc == "" and len(tags) == 0):
				aTask = {"description" : desc, "tags" : tags}
				task = OrderedDict(sorted(aTask.items(), key=lambda t: t[0]))
				allToDos.append(task)
				task ={}
				tags = []
			desc = d[0]			
			tags.append(d[1])
		else:
			tags.append(d[1])
	aTask = {"description" : desc, "tags" : tags}
	task = OrderedDict(sorted(aTask.items(), key=lambda t: t[0]))
	allToDos.append(task)
	return allToDos

# void 	deleteToDo(description):
def deleteToDo(description):
	conn = makeConnection()
	c = conn.cursor()
# 	print ("call delete_todo(1, '%s') ;" % description)

	c.execute("call delete_todo(1, '%s') ;" % description)
	conn.commit()
	conn.close()		
	return
	
# str 	getPwd(login):
def getPwd(login):
	conn = makeConnection()
	c = conn.cursor()

	print("login: %s" %login)
	rows_count = c.execute("Call get_userPwd(%s) ;" ,  (login,))
	if rows_count > 0:
		rs = c.fetchall()
		print("rs = %s" % rs)
		for i, r in enumerate(rs):
			pwd = r[0]		
# 		print("pwd = %s" % pwd)
	else:
		pwd = None
# 		print("no rs = %s" % rs)
	conn.close()		
	return pwd
		
		


