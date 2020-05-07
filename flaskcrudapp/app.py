from flask import Flask,render_template, redirect, flash, request,url_for, session

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
# key for initlize
app.secret_key = 'Secrete_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# for connecting with this database called mysqlphpadmin we must download this pip install Flask-MySQLdb for flask
app.config['SECRET_KEY'] = 'job appli secrate'
db = SQLAlchemy(app)


#Creating formdata table for our cruddata database
class DataForm(db.Model):
    id   = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email   = db.Column(db.String(100))
    phone   = db.Column(db.String(100))
    address   = db.Column(db.String(100))
    position   = db.Column(db.String(100))
    experience   = db.Column(db.Integer)


# parameter passing to the init

    def __init__(self, name, email, phone,lastname, address, position, experience ):
        self.name = name
        self.lastname  = lastname
        self.address = address
        self.position = position
        self.experience = experience
        self.email = email
        self.phone = phone

# this is for home page route
@app.route('/')
def home():
# this is for autofill data for the job form
    if 'name' in session:
        name     = session['name']
        lastname = session['lastname']
        email    = session['email']
        phone = session['phone']
        address = session['address']
        position = session['position']
        experience = session['experience']
        date = session['date']
        # rendering the data to home page
        return render_template('home.html', name = name, lastname=lastname, email=email, phone = phone, address=address,

                           position=position, experience=experience, date = date)
    # if the data is not in seesion then it will show entyform
    else:
        return render_template('home.html')



# this is the admin page route
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    # diplaying the data on the admin page.
    all_data = DataForm.query.all()
    if request.method == 'POST' and 'tag' in request.form: # getting the search query with name
        tag = request.form['tag']
        search = "%{}%".format(tag)
        fulldata = DataForm.query.filter(DataForm.name.like(search))#filter the data for admin page data query.
        return render_template('index.html', employees=fulldata, tag=tag)
    return render_template('index.html', employees = all_data)



# this is reated to the insert data to database
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name        = request.form['name']
        lastname    = request.form['lastname']
        email       = request.form['email']
        phone       = request.form['phone']
        address     = request.form['address']
        position    = request.form['position']
        experience  = request.form['experience']
        date = request.form['date']
# passing the data to the seesion
        session['name'] = name
        session['lastname'] = lastname
        session['email'] = email
        session['phone'] = phone
        session['address'] = address
        session['position'] = position
        session['experience'] = experience
        session['date']  = date
# database adding the data
        my_data = DataForm(name, email, phone, lastname, address, position, experience)
        db.session.add(my_data)
        db.session.commit() # save
        flash('Form Subminted Sucessfully!')
        return redirect(url_for('home'))

# this is route is used for update the database data
@app.route('/update', methods = ['GET', 'POST'])
def update():
    # getting the data from database.
    if request.method == 'POST':
        all_data = DataForm.query.get(request.form.get('id')) # we can the data based on the id
        all_data.note = request.form['note']
        db.session.commit()
        flash('your form was updated')
        return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug = True)



