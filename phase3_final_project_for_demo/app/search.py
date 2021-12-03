from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/search', methods = ['GET', 'POST'])
@app.route('/', methods = ['GET', 'POST'])
def search():
    msg = ''
    if 'role' in session:
        role = session['role']
    else:
        role = ''
        
    query_num_unsold = '''SELECT ((SELECT COUNT(*) FROM Vehicles)-(SELECT COUNT(*) FROM Salesevents)) AS NumUnsold;'''
    num_unsold = drop_year = runSQL.readSQL(query_num_unsold)[0][0]
    
    query_year = '''SELECT DISTINCT ModelYear FROM Vehicles
                    ORDER BY ModelYear DESC;
                    '''                 
    drop_year = runSQL.readSQL(query_year)
    drop_year= [row[0] for row in drop_year]
    
    
    query_manu = '''SELECT ManufacturerName FROM Manufacturer;'''
    drop_manu = runSQL.readSQL(query_manu)
    drop_manu= [row[0] for row in drop_manu]    
    
    query_type = '''SELECT 'Car' AS Type UNION SELECT 'SUV' UNION SELECT 'Truck' 
                    UNION SELECT 'Convertible' UNION SELECT 'Van MiniVan';'''
    drop_type = runSQL.readSQL(query_type)
    drop_type = [row[0] for row in drop_type]    
    
    query_color = '''SELECT Color FROM Colors;'''
    drop_color = runSQL.readSQL(query_color)
    drop_color= [row[0] for row in drop_color]    
    
    if request.method == 'POST':
        ###return request.form
        if role != 'Manager' and role != 'Owner':
            if "".join(request.form.values()) == "":
                alert0 = "You must at least enter one input."
                return render_template('search.html', msg=msg, alert0=alert0, drop_year = drop_year, drop_manu=drop_manu,\
                                       drop_type=drop_type, drop_color=drop_color,role=role, num_unsold=num_unsold)
            

        if request.form["Vtype"] != "":
            Type = request.form["Vtype"]
        else:
            Type = None
            
        if request.form["color"] != "":
            color = request.form["color"]
            color2 = "%"+color+"%"
        else:
            color = None
            color2 = None
            
        if request.form["manu"] != "":
            manu = request.form["manu"]
        else:
            manu = None
        if request.form["year"] != "":
            year = request.form["year"]
        else:
            year = None
        if request.form["minprice"] != "":
            minprice = float(request.form["minprice"])
        else:
            minprice = None
        if request.form["maxprice"] != "":
            maxprice = float(request.form["maxprice"])
        else:
            maxprice = None
        if maxprice and minprice and maxprice < minprice:
            msg = "Invalid Information"
            return render_template('search.html', msg=msg, drop_year = drop_year, drop_manu=drop_manu,\
                       drop_type=drop_type, drop_color=drop_color,role=role, num_unsold=num_unsold)
        if request.form["keyword"] != "":
            kw = request.form["keyword"]
            kw2 = "%"+kw+"%"
        else:
            kw = None
            kw2 = None

        sold_filter = request.form["sold"]
        
        if request.form["Vin_input"] != "":
            Vin = request.form["Vin_input"]
        else:
            Vin = None
            
        if role == 'Manager' or role == 'Owner':
            IsManager = '1'
        else:
            IsManager ='0'

        with open(os.path.join(os.getcwd(), "sql_files", "search.sql"),
          "r", encoding='utf-8') as file:
            tmp = file.readlines();
            
        query = " ".join(tmp).format(t=Type, m=manu, y=year, \
                                maxp=maxprice, minp=minprice, c=color, v=Vin, IsM=IsManager, f=sold_filter)
            
        res = []
        print(query)
        
        search_list = [Type,manu,year,maxprice,minprice,color,color2, kw,kw2,kw2,kw2,kw2,kw,kw2,Vin]
        res = runSQL.readSQL(query, search_list)
        
        
        if res:
            msg =  'Search results:'
            col = ('VIN', 'Type', 'Model Year', 'Manufacturer', 'Model','Color(s)', 'List Price', 'Match')
            return render_template('search.html', msg = msg, res=res, col = col, drop_year = drop_year, drop_manu=drop_manu,\
                                   drop_type=drop_type, drop_color=drop_color, role=role, num_unsold=num_unsold)
        else:
            msg = 'Sorry, it looks like we don’t have that in stock! Please search again.'
            col = []
            return render_template('search.html', msg = msg, drop_year = drop_year, drop_manu=drop_manu, drop_type=drop_type,\
                                   drop_color=drop_color, role=role, num_unsold=num_unsold)
            

    return render_template('search.html', msg=msg, drop_year = drop_year, drop_manu=drop_manu, drop_type=drop_type,\
                           drop_color=drop_color,role=role, num_unsold=num_unsold)
    
