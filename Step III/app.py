from flask import Flask,render_template, request, json, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from wtforms import StringField, SubmitField, IntegerField, FloatField, DateTimeField, SelectField
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

# Consider making a new file for these form definitions & adding an import statement

class NewPatient(FlaskForm):
    lname = StringField('Last Name', validators = [DataRequired()])  # Consider adding Length Validator to match the max length dictated by MySQL
    fname = StringField('First Name', validators = [DataRequired()])
    age = IntegerField('Age', validators = [DataRequired()])
    gender = StringField('Gender')
    height = IntegerField('Height (inches)', validators = [DataRequired()])
    weight = IntegerField('Weight (lbs)', validators = [DataRequired()])
    submit = SubmitField('Create New Patient')

class EditPatient(FlaskForm): # possible to find a way to populate this with existing data?
    pat_id = IntegerField('Patient ID', validators = [DataRequired()])   
    lname = StringField('Last Name', validators = [DataRequired()])
    fname = StringField('First Name', validators = [DataRequired()])
    age = IntegerField('Age', validators = [DataRequired()])
    gender = StringField('Gender')
    height = IntegerField('Height (inches)', validators = [DataRequired()])
    weight = IntegerField('Weight (lbs)', validators = [DataRequired()])
    submit = SubmitField('Edit Patient')

class NewLabResult(FlaskForm):
    phos_lab = FloatField('Phosphorous Lab')
    pot_lab = FloatField('Potassium Lab')
    sod_lab = IntegerField('Sodium Lab')
    dial_lab = FloatField('Dialysis Adequacy Lab')
    lab_time = DateTimeField('Lab Results Time')
    pat_id = SelectField('Patient Select') # how to show this as a list of existing patients? Ideally by name rather than id
    dial_id = SelectField('Dialysis Type Select') 
    submit = SubmitField('Create New Lab Result')

class EditLabResult(FlaskForm):
    lab_id = IntegerField('Lab ID')
    phos_lab = FloatField('Phosphorous Lab')
    pot_lab = FloatField('Potassium Lab')
    sod_lab = IntegerField('Sodium Lab')
    dial_lab = FloatField('Dialysis Adequacy Lab')
    lab_time = DateTimeField('Lab Results Time')
    pat_id = SelectField('Patient Select') 
    dial_id = SelectField('Dialysis Type Select') 
    submit = SubmitField('Edit Lab Result')

class NewFood(FlaskForm):
    food_name = StringField('Food Name', validators = [DataRequired()])
    phosphorous_content = IntegerField('Phosphorous Content') # need to add units
    sodium_content = IntegerField('Phosphorous Content')
    calories = IntegerField('Calories')
    potassium_content = IntegerField('Potassium Content')
    amount = IntegerField('Serving Size')

class EditFood(FlaskForm):
    food_id = IntegerField('Food ID', validators = [DataRequired()])  # find a way to get rid of this, just use food_name?? (consider duplicate names)
    food_name = StringField('Food Name', validators = [DataRequired()])
    phosphorous_content = IntegerField('Phosphorous Content') # need to add units
    sodium_content = IntegerField('Phosphorous Content')
    calories = IntegerField('Calories')
    potassium_content = IntegerField('Potassium Content')
    amount = IntegerField('Serving Size')

class NewDialysisForm(FlaskForm):
    name = StringField('Name of Dialysis Type', validators = [DataRequired()])
    location_type = StringField('Location Type', validators = [DataRequired()])
    adequacy_standard = FloatField('Adequacy Standard', validators = [DataRequired()])

class EditDialysisForm(FlaskForm):
    dialysis_id = IntegerField('Dialysis ID', validators = [DataRequired()])
    name = StringField('Name of Dialysis Type', validators = [DataRequired()])
    location_type = StringField('Location Type', validators = [DataRequired()])
    adequacy_standard = FloatField('Adequacy Standard', validators = [DataRequired()])

class NewPatientFood(FlaskForm):  # why are we using a composite primary key??
    food_id = IntegerField('Food ID', validators = [DataRequired()])
    patient_id = IntegerField('Food ID', validators = [DataRequired()])
    food_time = DateTimeField('Consumption Time', validators = [DataRequired()])

class EditPatientFood(FlaskForm):  
    food_id = IntegerField('Food ID', validators = [DataRequired()])
    patient_id = IntegerField('Food ID', validators = [DataRequired()])
    food_time = DateTimeField('Consumption Time', validators = [DataRequired()])


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


@app.route("/foods", methods=["POST", "GET"])
def foods_view():
    if request.method == "GET":
        query = 'SELECT food_id, food_name, amount, phosphorous_content, sodium_content, calories, potassium_content FROM Foods;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("foods.html", foods = results)

@app.route("/lab_results", methods=["POST", "GET"])
def labs_view():
    form = NewLabResult()
    if request.method == "GET":
        query = "SELECT lab_id, phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time FROM Lab_Results;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("lab_results.html",form=form, lab_data = results)
    if request.method == 'POST':
        phos_lab = request.form['phos_lab']
        pot_lab = request.form['pot_lab']
        sod_lab = request.form['sod_lab']
        dial_lab = request.form['dial_lab']
        lab_time = request.form['lab_time']
        pat_id = request.form['pat_id']
        dial_id = request.form['dial_id']
        for x in (phos_lab,pot_lab, sod_lab, dial_lab, lab_time, pat_id, dial_id):
            if x == '':
                x = 'NULL'
        query = """INSERT INTO lab_results (phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time
Patients_patient_id,Dialysis_Forms_dialysis_id) VALUES
(%s, %s, %s, %s, %s
%s, %s);"""
        db.execute_query(db_connection = db_connection, query = query, query_parms = (phos_lab,pot_lab, sod_lab, dial_lab, lab_time, pat_id, dial_id))
        return redirect(url_for('labs_view'))

@app.route("/dialysis_forms", methods=["POST", "GET"])
def dialysis_forms_view():
    if request.method == "GET":
        query = 'SELECT dialysis_id, name, location_type, adequacy_standard FROM Dialysis_Forms;'
        cursor = db.execute_query(db_connection=db_connection,query=query)
        results = cursor.fetchall()
        return render_template("dialysis_forms.html", dialysis_data = results)

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
        return render_template("edit_patient.html", form=form, patient_id=patient_id)
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
        # cur = mysql.connection.cursor()
        # cur.execute(query, (last_name, first_name, age, gender, height, weight, pat_id))
        # mysql.connection.commit()
        db.execute_query(db_connection=db_connection, query=query, query_params=(last_name, first_name, age, gender, height, weight, pat_id))
    return redirect(url_for("patients_view"))

@app.route("/delete_lab_results/<int:lab_id>")
def delete_lab_results(lab_id):
    query = "DELETE FROM Lab_Results WHERE lab_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (lab_id,))
    mysql.connection.commit()
    return redirect(url_for("labs_view"))

@app.route("/update_lab_results/<int:lab_id>", methods=["POST","GET"])
@app.route("/update_lab_results/", methods=["POST","GET"])
def update_lab_result(lab_id=None):
    form = EditLabResult()
    if request.method == "GET":
        return render_template("edit_lab_results.html", form=form)
    if request.method == "POST":
        phos_lab = request.form['phos_lab']
        pot_lab = request.form['pot_lab']
        sod_lab = request.form['sod_lab']
        dial_lab = request.form['dial_lab']
        lab_time = request.form['lab_time']
        pat_id = request.form['pat_id']
        dial_id = request.form['dial_id']
        query = """UPDATE Lab_Results
SET phosphorus_lab = %s, potassium_lab = %s, sodium_lab = %s, 
dialysis_adequacy_lab = %s, lab_results = %s
WHERE lab_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (phos_lab,pot_lab, sod_lab, dial_lab, lab_time, pat_id, dial_id))
        mysql.connection.commit()
    return redirect(url_for("labs_view"))

db_connection.ping(True)

if __name__ == "__main__":
    query = 'SELECT food_id, food_name, amount, phosphorous_content, sodium_content, calories, potassium_content FROM Foods;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    print(results)
