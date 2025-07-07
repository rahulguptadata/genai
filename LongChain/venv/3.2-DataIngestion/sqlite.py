import sqlite3
#code to connect sqllite
connection = sqlite3.connect("student.db")

#create cursor object to insert an create table
cursor=connection.cursor()

table_info="""
create table STUDENT(NAME Varchar(25),CLASS varchar(25)
,SECTION VARCHAR(25),MARKS INT
)
"""

cursor.execute(table_info)

##insert rows
cursor.execute("Insert into STUDENT values('Krish','Data Science','A',90)")
cursor.execute("Insert into STUDENT values('Rahul','Data Science rahul','A',97)")
cursor.execute("Insert into STUDENT values('Ritisha','Data Science Ritisha','A',100)")
cursor.execute("Insert into STUDENT values('Ritesh','Data Big','A',97)")
cursor.execute("Insert into STUDENT values('Rupali','Data Devops','A',89)")

#isplay all records
print("The inserted records are")

data=cursor.execute("select * from STUDENT")
for row in data:
    print(row)

## commit changes in 
connection.commit()

connection.close()

