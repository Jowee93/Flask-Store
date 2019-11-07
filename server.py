import peeweedbevolve
from flask import Flask, render_template, request, flash, redirect, url_for, session, escape
from models import *

app = Flask(__name__)
app.secret_key = b'\x92\xceG8\xae\xf5\xf5>\xa0\xed\x028jRT\x8e'

@app.before_request # new line
def before_request():
   db.connect()

@app.after_request # new line
def after_request(response):
   db.close()
   return response

# This allows user to run migrate via flask shell
@app.cli.command(short_help="Migrate to database")
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/store")
def store():
    return render_template('store.html')

@app.route("/store_form", methods=['GET', 'POST'])
def create_store():
    # If form is requested via POST, then server side should use request.form (from body of request).
    # If form is request via GET, then server sid should use request.args (from URL of request)
    if request.method == 'POST':
        # Stores input from form with name = store_name, into class Store to create a new class Store
        s = Store(name=request.form.get("store_name"))
        
        # Adds added store to database. Flash is a function to display message. Needs a secret key
        if s.save():
            flash(f"Successfully added store: {s.name}", "success")
            
            # Redirect is used after a post request / form submission, this to prevent double submission
            return redirect(url_for('store'))
        else:
            # If fail to save, okay to render_template as not submission went through
            return render_template('store.html', name=request.form.get("store_name"))   
        
    else:
        # Stores input from form with name = store_name, into class Store to create a new class Store
        s = Store(name=request.args.get("store_name"))
        
        # Adds added store to database. Flash is a function to display message. Needs a secret key
        if s.save():
            flash(f"Successfully added store: {s.name}", "success")
            
            # Redirect is used after a post request / form submission, this to prevent double submission
            return redirect(url_for('store'))
        else:
            # If fail to save, okay to render_template as not submission went through
            return render_template('store.html', name=request.args.get("store_name"))  
        
        
@app.route("/warehouse")
def warehouse():
    stores = Store.select()
    all_stores = [Store.name for Store in stores]
    return render_template('warehouse.html', store=stores)

@app.route("/warehouse_form", methods=['GET', 'POST'])
def create_warehouse():
    
    
    # If form is requested via POST, then server side should use request.form (from body of request).
    # If form is request via GET, then server sid should use request.args (from URL of request)
    if request.method == 'POST':
        # Stores input from form with name = store_name, into class Store to create a new class Store
        w = Warehouse(location=request.form.get("warehouse_name"))
        
        # Adds added store to database. Flash is a function to display message. Needs a secret key
        if w.save():
            flash(f"Successfully added store: {w.name}", "success")
            
            # Redirect is used after a post request / form submission, this to prevent double submission
            return redirect(url_for('warehouse'))
        else:
            # If fail to save, okay to render_template as not submission went through
            return render_template('warehouse.html', location=request.form.get("warehouse_name"))   
        
    else:
        # Stores input from form with name = store_name, into class Store to create a new class Store
        w = Warehouse(location=request.args.get("warehouse_name"))
        
        # Adds added store to database. Flash is a function to display message. Needs a secret key
        if w.save():
            flash(f"Successfully added warehouse: {w.name}", "success")
            
            # Redirect is used after a post request / form submission, this to prevent double submission
            return redirect(url_for('warehouse'))
        else:
            # If fail to save, okay to render_template as not submission went through
            return render_template('warehouse.html', location=request.args.get("warehouse_name"))  
            

if __name__ == '__main__':
    app.run()
    
