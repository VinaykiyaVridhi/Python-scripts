#!/usr/bin/env python3

#Query the miRNA database through the browser using a cgi program

import pymysql
import cgi
import cgitb
from string import Template

#the next line is useful for debugging
#it causes errors during execution to be sent back to the browser
cgitb.enable()

#create the html template
#leave space for the style, title, intro, form, summary, table, error message
html_template = Template(
"""
<html>
    <head>
        <title>${title}</title>
        ${style}
    </head>
    <body>
        <div>${intro}<br></div>
        <div>${form_html}<br></div>
        <div id="summary">${summary}<br><br><div>        
        <div>${table_output}</div>
        <div id="error">${error_message}</div> 
    </body>
</html>
"""
)

#define style css
style="""
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 15px;
            }
            th, tr:nth-child(even) {
                background-color: lightgray;
            }
            #error {
                color: red;
            }
            #summary {
                font-weight: bold;
            }
        </style>
"""

#define the title
title="Gene Targets of microRNAs"

#define the title
intro = """
<h1>Gene targets of microRNAs</h1>
<p>
    This is a solution program for HW 3, BF768 Spring 2022.<br>
    Enter two gene names and this website will return all the microRNAs<br>
    that target both genes along with the targeting scores.
</p>
"""

#define the form
form_html="""
<form name="myForm" action="https://bioed.bu.edu/cgi-bin/gbenson/hw3_for_bioed.py" method="get"> 
    Gene 1 (example AFF4): <input type="text" name="gene1"><br> 
    Gene 2 (example AGAP2): <input type="text" name="gene2"><br> 
    <input type="submit" value="Submit">
</form>
"""

#define the table
table_html = Template(
"""
        <table>
            <thead>
                <tr>
                    <th>miRNA</th>
                    <th>${gene1} targeting score</th>
                    <th>${gene2} targeting score</th>
                </tr>
            </thead>
            <tbody>
            ${body_rows}
            </tbody>
        </table>
"""
)
body_rows = ""
table_output = ""

#define the error message
error_message = ""

#define the summary
summary = ""

# define the query
query1 = """
select m1.name, t1.score, t2.score
from miRNA m1 join targets t1 using(mid) join gene g1 on g1.gid=t1.gid 
join targets t2 using(mid) join gene g2 on g2.gid=t2.gid
where g1.name = %s and g2.name = %s;
""" 

query2 = """
select name 
from gene 
where name = %s
"""
#retrieve form data from the web server
#keep_blank_values allows empty form fields to be detected
form = cgi.FieldStorage(keep_blank_values=True) 

if (form):
#get submitted values
    gene1 = form.getvalue("gene1","") #second string is default if nothing is returned
    gene2 = form.getvalue("gene2","")

    #test that 2 gene names were returned
    if(gene1=="" or gene2==""):
        error_message = " One of your gene names was missing, try again."
    else:       
        #establish the connection on bioed
        connection = pymysql.connect(
            host='bioed.bu.edu', 
            user='username',
            password='password', 
            db='miRNA',
            port = 4253) 

        # get cursor
        cursor = connection.cursor()

        #test first gene name
        try: 
            numrows1 = cursor.execute(query2,[gene1])
        except pymysql.Error as e: 
            print(e,query2)
        
        #test second gene name
        try: 
            numrows2 = cursor.execute(query2,[gene2])
        except pymysql.Error as e: 
            print(e,query2)

        if (numrows1 == 0):
            error_message = "Gene %s does not exist in the database" % (gene1)
        elif (numrows2 == 0):
            error_message = "Gene %s does not exist in the database" % (gene2)
        else: 
        
            # Execute the target search query
            try: 
                numrows = cursor.execute(query1,[gene1, gene2])
            except pymysql.Error as e: 
                print(e,query1)

            results = cursor.fetchall() 
        
            for row in results:
                body_rows += "<tr><td>%s</td><td>%f</td><td>%f</td></tr>" %(row[0],row[1],row[2])

            #close connection   
            cursor.close()
            connection.close()

            table_output = table_html.safe_substitute(gene1=gene1, gene2=gene2, body_rows=body_rows)
            summary = "Gene %s and gene %s are both targeted by %d miRNAs." %(gene1, gene2, numrows)

html_output = html_template.safe_substitute(style=style, title=title, intro=intro, form_html=form_html, summary= summary, table_output=table_output, error_message=error_message)

#next line is always required as first part of html output
print("Content-type: text/html\n")

print(html_output)
