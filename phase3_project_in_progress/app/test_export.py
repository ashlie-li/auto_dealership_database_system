from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os

@app.route('/test_export')
def test_export():
    query = 'select * from customers2;'
    res = runSQL.readSQL(query)
    
    for row in res:
        print(row[0], row[-1])
    return 'testing'