from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/<string:Act>/pass/<string:Vin>', methods = ['GET', 'POST'])
def test(Act, Vin):
    if request.method == 'POST' and 'CustomerID' in request.form:
        return "pass done"
    return "pass not done"