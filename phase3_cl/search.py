from flask import Flask, render_template,request,jsonify
from flask_mysqldb import MySQL,MySQLdb


app = Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='28760039'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='team022'
app.config['MYSQL_CURSORCLASS']='DictCursor'


mysql=MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/searchdata", methods=["POST", "GET"])
def searchdata():
    if request.method == 'POST':
        a = request
        search_word = request.form['query']
        color = request.form['color']
        query = ''
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # query = "SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,Description,VehicleColors.Colors " \
        #         "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin " \
        #         "WHERE Manufacturer LIKE %s OR ModelYear LIKE %s OR ModelName LIKE %s OR Description LIKE %s " \
        #         "ORDER BY Vin DESC LIMIT 20"
        if color != '':
            # query = "SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,Description,VehicleColors.Colors " \
            #         "FROM Vehicles " \
            #         "LEFT JOIN VehicleColors" \
            #         "ON Vehicles.Vin = VehicleColors.Vin" \
            #         "WHERE Colors LIKE %s"
            query = "SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,Description,VehicleColors.Colors " \
                    "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin " \
                    "WHERE Colors LIKE %s AND ModelYear LIKE %s" \
                    "ORDER BY Vin DESC LIMIT 20"

        # cur.execute(query, (format(color)))
            cur.execute(query,(format(color), format(search_word)))
            programming = cur.fetchall()
    return jsonify({'data': render_template('result.html', programming=programming)})


if __name__ == "__main__":
    app.run(debug=True)
