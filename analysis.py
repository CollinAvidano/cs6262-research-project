import mysql.connector

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="yourusername",
#     password="yourpassword",
#     database="mydatabase"
# )

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="website_vulnerabilities"
)

cursor = db.cursor()

sql = "select * from ip_address"
cursor.execute(sql)
result = cursor.fetchall()
for x in result:
	print(x)

sql = "select * from website"
cursor.execute(sql)
result = cursor.fetchall()
for x in result:
	print(x)
