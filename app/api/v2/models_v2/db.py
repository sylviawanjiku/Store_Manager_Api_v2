import psycopg2
id = 4
username = "username"
email ="email"
password = "password"
conn = psycopg2.connect("dbname=Storemanager user=postgres password=root host=localhost")

try:
  
    cursor = conn.cursor()

    cursor.execute())
    rows = cursor.fetchone()
    print(rows)
   
except Exception as e:
        print("connection to database failed",e)
