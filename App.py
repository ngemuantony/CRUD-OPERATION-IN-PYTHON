from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = '32e3cea25294cca16cbb4401a83f86be'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:antony2002@localhost/crud-operationdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(60))
    phone = db.Column(db.String(20))

    # ---------------- Creating the class constructor or Employee -------------------
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

with app.app_context():
    db.create_all()
# ====================== THE BEGINNING OF ROUTES DEFINITION =================

# ============ root template rendering ===============
@app.route('/')
def index():
    all_data = Employee.query.all()
    return render_template('index.html',employees = all_data)

# =========== Insert route =========================
@app.route('/insert', methods = ['GET','POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Employee(name, email, phone) 
        db.session.add(my_data)
        db.session.commit()

        flash('Employee inserted successfully', category = 'success')

        return redirect(url_for('index'))
    
# ============== Update route ===========================
@app.route('/update', methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = Employee.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()

        flash("Employee Updated successfully", category = 'info')

        return redirect(url_for('index'))
    
# =================== Delete route ===========================
@app.route('/delete/<id>/', methods=['GET','POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully", category='warning')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=8080)