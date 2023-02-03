#!/usr/bin/env python3

#create a table Pathways and load a file into the table using load data local infile

import pymysql

#establish the connection
connection = pymysql.connect(
	host='bioed.bu.edu', 
	user='username',
	password='password', 
	db='username',
	port = 4253,
	local_infile=1)  #needed for load data local infile


# get cursor
cursor = connection.cursor()

# MySQL queries
query1 = "drop table if exists Pathways;" 

query2 = """
	create table Pathways (
		path_id integer not null,
		pathname varchar(100),
		primary key (path_id)
	) engine=innodb;
	"""
query3 = "LOAD DATA LOCAL INFILE 'pathways.tab' into table Pathways (path_id, pathname);"

#next query is to test that the load worked.  Not necessary for the homework
query4 = "select * from Pathways limit 10;"

# Execute the mySQL queries

#drop table
try: 
	cursor.execute(query1)
except pymysql.Error as e: 
	print(e,query1)

#create table
try: 
	cursor.execute(query2)
except pymysql.Error as e: 
	print(e,query2)

#commit change
connection.commit()

#load data infile
try: 
	cursor.execute(query3)
except pymysql.Error as e: 
	print(e,query3)

#commit change
connection.commit()

#next block is to test that the load worked.  Not necessary for the homework
try: 
	cursor.execute(query4)
except pymysql.Error as e: 
	print(e,query4)
	
results = cursor.fetchall() 

for row in results:
	print(row)
#end testing

#close connection	
cursor.close()
connection.close()

