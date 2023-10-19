from flask import render_template
from . import main


@main.route('/')
def welcome():
    return render_template('base.html')
