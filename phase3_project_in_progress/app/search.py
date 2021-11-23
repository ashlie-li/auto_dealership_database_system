from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app



@app.route('/search', methods = ['GET', 'POST'])
def search():
    msg = ''

    query0 = '''SELECT DISTINCT ModelYear FROM Vehicles
                    ORDER BY ModelYear DESC;
                    '''

    drop0 = runSQL.readSQL(query0)

    drop = [row[0] for row in drop0]

    if request.method == 'POST' and 'manu' in request.form:
        manu = request.form['manu']

        print(manu)
        if 'year' in request.form:
            year = request.form['year']
        else:
            year = None
        print(year)

        query = '''SELECT * FROM Vehicles WHERE Manufacturer = %s
                    AND CASE WHEN %s IS NOT NULL
                    THEN ModelYear = %s
                    ELSE TRUE END
                    ;'''

        query1 = '''SELECT * FROM Vehicles WHERE Manufacturer = '{a}'
                    AND ModelYear = '{b}';'''.format(a = manu, b = year)

        res = []

        res = runSQL.readSQL(query, [manu, year , year ])
        print(res)

        if res:
            msg =  'Search results:'
            col = ('Vin', 'Manufacturer', 'ModelName', 'ModelYear', 'DateAdded','InvoicePrice', 'Description', 'ClerkUsername')
            return render_template('search.html', msg = msg, res=res, col = col, drop = drop)
        else:
            msg = 'No result, search again.'
            col = []
            return render_template('search.html', msg = msg, drop = drop)


    return render_template('search.html', drop = drop)

