from flask import Flask,render_template, request, json, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import database.db_connector as db
import os

host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")
app.config['MYSQL_USER'] =  os.environ.get("340DBUSER")
app.config['MYSQL_PASSWORD'] = passwd = os.environ.get("340DBPW")
app.config['MYSQL_DB'] = os.environ.get("340DB")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['SECRET_KEY'] = '7aa2bbaca21981ea2d0729fd9fb29565be20bb4541d81db437eb91ac85134ea4'

bootstrap = Bootstrap(app)
mysql = MySQL(app)
db_connection = db.connect_to_database()


# patients_headings= ("patient_id", "last_name","first_name", "age", "gender", "height", "weight")
# patients_data= (
#     ("1", "Smith", "Arlene", "55", "F", "64", "145"),
#     ("2", "Rogers", "Christopher", "63", "M", "72", "180"),
#     ("3", "Harrison", "Kayla", "68", "F", "65", "125"),
#     ("4", "Jackson", "Henry", "74", "M", "75", "200"),
#     ("5", "Wonders", "Brenda", "91", "F", "60", "92")
# )

# foods_headings=("food_id", "name", "amount", "phosphorus_content", "sodium_content", "calories", "potassium_content")
# foods_data= (
#     ("1", "Milk, Whole", "128", "251", "94.6", "152", "374"),
#     ("2", "Beef,loin, top loin steak", "284", "585", "128", "423", "801"),
#     ("3", "Chicken, breast", "174", "419", "81.8", "275", "597"),
#     ("4", "Yogurt, Greek, nonfat", "156", "212", "56.2", "92", "220"),
#     ("5", "Kale", "100", "55", "53", "43", "348")
#     )

# dialysis_headings=("dialysis_id", "name","location_type", "adequacy_standard", "kidney_doctor")
# dialysis_data=(
#     ("1", "hemodialysis FMC", "incenter", "1.2", "Dr. House"),
#     ("2", "peritoneal Baxter", "home", "1.7", "Dr. Grey")
# )

# labs_headings=("lab_id", "phosphorus_lab","potassium_lab", "sodium_lab", "dialysis_adequacy_lab", "lab_results_time")
# labs_data=( 
#     ("1", "3.5", "3.4", "135", "1.2","2022-05-07 23:22:05" ),
#     ("2", "5.5", "3", "142", "1.7","2022-05-08 18:36:10"),
#     ("3", "6.5", "2.8", "146", "1.1","2022-05-01 20:20:06" ),
#     ("4", "10.5", "6.6", "144", "0.6","2022-05-07 18:01:55"),
#      ("5", "7.2", "4.5", "134", "2.2","2022-05-11 10:19:25")
# )

class NewPatient(FlaskForm):
    lname = StringField('Last Name', validators = [DataRequired()])
    fname = StringField('First Name', validators = [DataRequired()])
    age = IntegerField('Age', validators = [DataRequired()])
    gender = StringField('Gender')
    height = IntegerField('Height (inches)', validators = [DataRequired()])
    weight = IntegerField('Weight (lbs)', validators = [DataRequired()])
    submit = SubmitField('Submit')

class EditPatient(FlaskForm):
    pat_id = IntegerField('Patient ID', validators = [DataRequired()])
    lname = StringField('Last Name', validators = [DataRequired()])
    fname = StringField('First Name', validators = [DataRequired()])
    age = IntegerField('Age', validators = [DataRequired()])
    gender = StringField('Gender')
    height = IntegerField('Height (inches)', validators = [DataRequired()])
    weight = IntegerField('Weight (lbs)', validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patients", methods=["POST", "GET"])
def patients_view():
    gender = None
    form = NewPatient()


    if request.method == "GET":
        query = "SELECT patient_id, last_name, first_name, age, gender, height, weight FROM Patients;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("patients.html", form=form, patients=results)
    if request.method == "POST":
        last_name = request.form['lname']
        first_name = request.form['fname']
        age = request.form['age']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        if gender == '':
            query = "INSERT INTO Patients (last_name, first_name, age, height, weight) VALUES (%s, %s, %s, %s, %s);"
            db.execute_query(db_connection=db_connection, query=query,query_params=(last_name,first_name,age,height,weight))
            return redirect(url_for('patients_view'))
        else:
            query = "INSERT INTO Patients (last_name, first_name, age, gender, height, weight) VALUES (%s, %s, %s, %s, %s, %s);"
            db.execute_query(db_connection=db_connection, query=query,query_params=(last_name,first_name,age,gender,height,weight))
            return redirect(url_for('patients_view'))

    
    
    # form.validate_on_submit():
    #     last_name = form.lname.data
    #     first_name = form.fname.data
    #     age = form.age.data
    #     gender = form.gender.data
    #     height = form.height.data
    #     weight = form.weight.data
    #     if gender == None:
    #         print('adding w/o gender')
    #         query = "INSERT INTO patients (last_name, first_name, age, height, weight) VALUES (%s, %s, %s, %s, %s);"
    #         cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(last_name,first_name, age, height,weight))
    #     else:
    #         print('adding w/ gender')
    #         query = "INSERT INTO patients (last_name, first_name, age, gender, height, weight) VALUES (%s, %s, %s, %s, %s, %s);"
    #         cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(last_name,first_name, age, gender, height,weight))
    #     return redirect('/patients')
    # if request.method == "POST":



@app.route("/foods", methods=["POST", "GET"])
def foods_view():
    if request.method == "GET":
        query = 'SELECT food_id, food_name, amount, phosphorous_content, sodium_content, calories, potassium_content FROM Foods;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("foods.html", foods = results)

@app.route("/lab_results", methods=["POST", "GET"])
def labs_view():
    if request.method == "GET":
        query = "SELECT lab_id, phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time FROM Lab_Results;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("lab_results.html", lab_data = results)

@app.route("/dialysis_forms", methods=["POST", "GET"])
def dialysis_forms_view():
    if request.method == "GET":
        query = 'SELECT dialysis_id, name, location_type, adequacy_standard FROM Dialysis_Forms;'
        cursor = db.execute_query(db_connection=db_connection,query=query)
        results = cursor.fetchall()
        return render_template("dialysis_forms.html", dialysis_data =results)

@app.route("/patients_foods", methods=["POST", "GET"])
def patients_foods_view():
    if request.method == "GET":
        query = """
        SELECT Foods.food_name as "Food Name", CONCAT(Patients.first_name, " ", Patients.last_name) as "Patient Name",
    Patients_Food.patient_food_time as "Time consumed" from Patients_Food
    JOIN Foods on Patients_Food.Foods_food_id = Foods.food_id
    JOIN Patients on Patients_Food.Patients_patient_id = Patients.patient_id;
    """
        cursor = db.execute_query(db_connection=db_connection,query=query)
        results = cursor.fetchall()
        return render_template("patients_foods.html", patient_foods=results)


# @app.route("/delete_patient/<int:patient_id>", methods = ["GET", "POST"])
# def delete_patient(patient_id):
#     query = "DELETE FROM Patients WHERE patient_id = '%s';"
#     cur = mysql.connection.cursor()
#     cur.execute(query, (patient_id))
#     mysql.connection.commit()
#     return redirect(url_for("patients_view"))

@app.route("/delete_patient/<int:patient_id>")
def delete_patient(patient_id):
    query = "DELETE FROM Patients WHERE patient_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (patient_id,))
    mysql.connection.commit()
    return redirect(url_for("patients_view"))

@app.route("/update_patient/<int:patient_id>", methods=["POST","GET"])
@app.route("/update_patient/", methods=["POST","GET"])
def update_patient(patient_id=None):
    form = EditPatient()
    if request.method == "GET":
        return render_template("edit_patient.html", form=form)
    if request.method == "POST":
        pat_id = request.form['pat_id']
        last_name = request.form['lname']
        first_name = request.form['fname']
        age = request.form['age']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        query = """UPDATE Patients
    SET last_name = %s, first_name = %s, age = %s, gender = %s, 
    height = %s, weight = %s
    WHERE patient_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (last_name, first_name, age, gender, height, weight, pat_id))
        mysql.connection.commit()

    return redirect(url_for("patients_view"))