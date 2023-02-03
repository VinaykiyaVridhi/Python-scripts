#!/usr/bin/env python3

#read an SQL command from a file and execute the command
#usage ./gary_benson_read_execute.py <database> <username> <password> <queryfile.sql>
#where:
# <database> is the database with the table (usually same as <username>)
# <username> is the user
# <password> is the mysql password
# <queryfile.sql> contains an SQL command
   
import pymysql
import sys
import re #for regular expression search to exclude comment lines in query file, not necessary for solution

def read_query (filename):
#concatenate lines of file into one string
	fh=open(filename,'r');
	query=""
	for line in fh:
		if (not re.search('^--', line)):
			query = query + " " + line.strip()  #add space between sequential lines to avoid merging two words
	return query
	
def execute_query (query, database, username, password):
#connect to database and execute query

	#establish the connection
	connection = pymysql.connect(
		host='bioed.bu.edu',
		user=username,
		password=password, 
		db=database,
		port = 4253)
		
	
	# get cursor
	cursor = connection.cursor()

	#execute query
	try: 
		cursor.execute(query)
	except pymysql.Error as e: 
		print(e, query)
	
	results = cursor.fetchall() 

	cursor.close()
	connection.close()

	return results

#main

# to print usage when invoking only filename; not needed in solution
if len(sys.argv) != 5:
    print ("Usage is: %s database username password queryfile" % sys.argv[0])
    sys.exit(0)

#get command line parameters
database = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
file = sys.argv[4]

#get query
query = read_query(file)

#for testing, not necessary
print(query)

#get results
results = execute_query(query, database, username, password)

#print results
for row in results:
	print(row)
	

