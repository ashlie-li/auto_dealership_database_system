from flask import Flask, render_template,request,jsonify
from flask_mysqldb import MySQL,MySQLdb
from app import app


mysql=MySQL(app)


@app.route('/search')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) AS TotalVehiclesForSale FROM Vehicles WHERE Vehicles.Vin NOT IN (SELECT Vin FROM SalesEvents)")
    data = cur.fetchall()[0]['TotalVehiclesForSale']
    cur.close()
    return render_template('search.html',data=data)


@app.route("/searchdata", methods=["POST", "GET"])
def searchdata():
    if request.method == 'POST':
        search_word = request.form['query']
        color = request.form['color']
        madeYear = request.form['year']
        manufacturer = request.form['manufacturer']
        vehicle_type = request.form['vehicle_type']
        min = request.form['min']
        max = request.form['max']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        prefix = False

        query = f"SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,InvoicePrice,Description,VehicleColors.Colors " \
                "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin "
        if vehicle_type != '':
            if vehicle_type == 'car':
                query = f"SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,InvoicePrice,Description,VehicleColors.Colors " \
                        "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin RIGHT JOIN Cars ON Vehicles.Vin = Cars.Vin "
            elif vehicle_type == 'convertible':
                query = f"SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,InvoicePrice,Description,VehicleColors.Colors " \
                        "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin RIGHT JOIN Convertibles ON Vehicles.Vin = Convertibles.Vin "
            elif vehicle_type == 'truck':
                query = f"SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,InvoicePrice,Description,VehicleColors.Colors " \
                        "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin RIGHT JOIN Trucks ON Vehicles.Vin = Trucks.Vin "
            elif vehicle_type == 'van':
                query = f"SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,InvoicePrice,Description,VehicleColors.Colors " \
                        "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin RIGHT JOIN VanMiniVans ON Vehicles.Vin = VanMiniVans.Vin "
            elif vehicle_type == 'suv':
                query = f"SELECT Vehicles.Vin,ModelYear,Manufacturer,ModelName,InvoicePrice,Description,VehicleColors.Colors " \
                        "FROM Vehicles LEFT JOIN VehicleColors ON Vehicles.Vin = VehicleColors.Vin RIGHT JOIN SUVs ON Vehicles.Vin = SUVs.Vin "
        if color != '':
            query = query + "WHERE Colors = '{}'"
            prefix = True
            query = query.format(color)
        if madeYear != '':
            if prefix:
                query = query + "AND ModelYear = '{}'"
            else:
                query = query + "WHERE ModelYear = '{}'"
                prefix = True
            query = query.format(madeYear)
        if manufacturer != '':
            if prefix:
                query = query + "AND Manufacturer = '{}'"
            else:
                query = query + "WHERE Manufacturer = '{}'"
                prefix = True
            query = query.format(manufacturer)
        if min != '':
            if prefix:
                query = query + "AND InvoicePrice >= '{}'"
            else:
                query = query + "WHERE InvoicePrice >= '{}'"
                prefix = True
            query = query.format(min)
        if max != '':
            if prefix:
                query = query + "AND InvoicePrice <= '{}'"
            else:
                query = query + "WHERE InvoicePrice <= '{}'"
                prefix = True
            query = query.format(max)
        if search_word != '':
            if prefix:
                query = query + "AND (Manufacturer LIKE '{}' OR ModelYear LIKE'{}' OR ModelName LIKE '{}' OR Description LIKE '{}')"
            else:
                query = query + "WHERE (Manufacturer LIKE '{}' OR ModelYear LIKE'{}' OR ModelName LIKE '{}' OR Description LIKE '{}')"
            query = query.format(search_word,search_word,search_word,search_word)
        cur.execute(query)
        programming = cur.fetchall()
        return jsonify({'data': render_template('result.html', programming=programming)})


if __name__ == "__main__":
    app.run(debug=True)
