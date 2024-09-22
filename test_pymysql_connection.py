import MySQLdb

try:
    connection = MySQLdb.connect(
        host='127.0.0.1',
        port=3306,
        user='hr_user',
        passwd='hr_db_pwd',
        db='hr_db'
    )
    print("Connection successful!")
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    if 'connection' in locals() and connection:
        connection.close()
