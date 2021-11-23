from flask import Flask, render_template, request

app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CS6400'
app.config['MYSQL_DB'] = 'CS6400_try1'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['SECRET_KEY'] = 'my_keys'


from app import report_part_stats, report_average_time, report_sales_by_color, report_monthly_sales, \
                report_repair_by_manu, report_customer_income, login, search, add_vehicle, \
                report_sales_by_type, report_sales_by_manufacturer, report_below_cost_sales

if __name__ == '__main__':
    app.run(debug = True, port = 5000)