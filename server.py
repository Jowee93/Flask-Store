import peeweedbevolve
from flask import Flask, render_template, request
from models import db

app = Flask(__name__)

@app.before_request # new line
def before_request():
   db.connect()

@app.after_request # new line
def after_request(response):
   db.close()
   return response

# This allows user to run migrate via flask shell
@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    
