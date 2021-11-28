from flask import Flask, render_template, request

app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CS6400'
app.config['MYSQL_DB'] = 'cs6400_demodata'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['SECRET_KEY'] = 'my_keys'


from app import report_part_stats, report_average_time, report_sales_by_color, report_monthly_sales, \
                report_below_cost_sales, report_sales_by_type, report_sales_by_manufacturer, \
                report_repair_by_manu, report_customer_income, login, search, add_vehicle, vehicle_detail,\
                search_add_customer,add_sales, main_menu, testing, logout, add_repair2, test_export

if __name__ == '__main__':
    app.run(debug = True, port = 5000)