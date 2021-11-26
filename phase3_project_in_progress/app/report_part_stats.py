from flask import Flask, render_template, request, session
from app import app
import runSQL


@app.route('/report_part_stats', methods = ['GET', 'POST'])
def part_stats():
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']

    #return render_template('index.html')
    query = '''SELECT VendorName,  SUM(QuantityUsed * Price) AS TotalCost,
            SUM(QuantityUsed) AS NumberOfPart
            FROM Parts GROUP BY VendorName
            ORDER BY TotalCost DESC;'''


    raw= runSQL.readSQL(query)
    raw = list(raw)

    res = []
    for row in raw:
        tmp = []
        tmp.append(row[0])
        tmp.append('$ ' + str(row[1]))
        tmp.append(row[2])
        res.append(tmp)

    col = ('Vendor Name', 'Total Cost', 'Number of Part')


    return render_template('report_part_stats.html', col = col, res = res)