from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CS6400'
app.config['MYSQL_DB'] = 'CS6400_try1'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    
    def readSQL(query):
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        cur.close()
        return res

    query = '''SELECT VendorName,  SUM(QuantityUsed * Price) AS TotalCost, 
            SUM(QuantityUsed) AS NumberOfPart
            FROM Parts GROUP BY VendorName
            ORDER BY TotalCost DESC;'''    
    
    raw= readSQL(query)
    raw = list(raw)
    
    res = []
    for row in raw:
        tmp = []
        tmp.append(row[0])
        tmp.append('$ ' + str(row[1]))
        tmp.append(row[2])
        res.append(tmp)
        
    col = ('Vendor Name', 'Total Cost', 'Number of Part')

    
    return render_template('report.html', col = col, res = res)

if __name__ == '__main__':
    app.run(debug = True, port = 5000)