from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Table


# Flask application object
app = Flask(__name__)
# set the URI for the database to use
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root1:root@localhost/example_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# use the application object as a parameter to create an object of class SQLAlchemy
db = SQLAlchemy(app)


# -- MODEL --
# you’ll use the database object to create a database table for students, which is represented by a model
class Students(db.Model):
    __tablename__ = "students"
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    # email = db.Column(db.String(30))

    def __init__(self, name, city, addr, pin, id=None):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        self.id = id


# --VIEW --


@app.route('/')
def show_all():
    return render_template('show_all.html', students=Students.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr'] or not request.form['pin']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
            db.session.add(student)
            db.session.commit()
            db.session.close()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/delete', methods=['GET','PUT'])
def delete():
    if request.method == 'PUT':
        id = request.args.get('id')
        if not id:
            flash('Please enter id of the student', 'error')
        else:
            student_table = Table(
                "students", db.metadata, autoload=True, autoload_with=db.engine
            )
            db.session.execute(
                student_table.delete()
                    .where(student_table.c.student_id == int(id))
            )
            db.session.commit()
            db.session.close()
            flash('Record was successfully deleted')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


# # To create/use the database
# db.create_all()
# # Inserts records into a mapping table
# db.session.add (model object)
# # delete records from a table
# db.session.delete (model object)
# # Filter the record set
# students.query.filter_by(city = ’Tokyo’).all()
