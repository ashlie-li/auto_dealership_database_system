from app import app
from flask_mysqldb import MySQL
import MySQLdb

mysql = MySQL(app)

def readSQL(query, inputs = None):
    cur = mysql.connection.cursor()
    res_value = cur.execute(query, inputs)
    mysql.connection.commit()
    res = cur.fetchall()
    cur.close()
    return res

def writeSQL(query, inputs = None):
    cur = mysql.connection.cursor()
    
    try:
        res_value = cur.execute(query, inputs)
        mysql.connection.commit()
        cur.close()
        return 'query is executed'
    except Exception as e:
        print(e)
        cur.close()
        return 'get an error: ' + str(e)
       