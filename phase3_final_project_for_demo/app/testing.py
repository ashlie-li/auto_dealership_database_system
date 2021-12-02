from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os


@app.route('/testing')
def testing():
    print(session)
    return render_template('testing.html')
