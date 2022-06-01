import os

from flask import Flask, json, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from jmespath import search
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField, DateTimeField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

import database.db_connector as db

# Configuration

app = Flask(__name__)
bootstarp = Bootstrap(app)
mysql = MySQL(app)
db_connection = db.connect_to_database()

app.config["MYSQL_HOST"] = os.environ.get("340DBHOST")
app.config["MYSQL_USER"] = os.environ.get("340DBUSER")
app.config["MYSQL_PASSWORD"] = passwd = os.environ.get("340DBPW")
app.config["MYSQL_DB"] = os.environ.get("340DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SECRET_KEY"] = "secretkey"

# Forms


class NewPatient(FlaskForm):
    lname = StringField(
        "Last Name", validators=[DataRequired()]
    )  # Consider adding Length Validator to match the max length dictated by MySQL
    fname = StringField("First Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    gender = StringField("Gender")
    height = IntegerField("Height (inches)", validators=[DataRequired()])
    weight = IntegerField("Weight (lbs)", validators=[DataRequired()])
    submit = SubmitField("Create New Patient")


class EditPatient(FlaskForm):  # possible to find a way to populate this with existing data?
    pat_id = IntegerField("Patient ID", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    fname = StringField("First Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    gender = StringField("Gender")
    height = IntegerField("Height (inches)", validators=[DataRequired()])
    weight = IntegerField("Weight (lbs)", validators=[DataRequired()])
    submit = SubmitField("Edit Patient")


class NewLabResult(FlaskForm):
    phos_lab = FloatField("Phosphorous Lab")
    pot_lab = FloatField("Potassium Lab")
    sod_lab = IntegerField("Sodium Lab")
    dial_lab = FloatField("Dialysis Adequacy Lab")
    lab_time = DateTimeField("Lab Results Time", format='%Y-%m-%d %H:%M:%S')
    pat_id = SelectField(
        "Patient Select"
    )  # how to show this as a list of existing patients? Ideally by name rather than id
    dial_id = SelectField("Dialysis Type Select")
    submit = SubmitField("Create New Lab Result")


class EditLabResult(FlaskForm):
    lab_id = IntegerField("Lab ID")
    phos_lab = FloatField("Phosphorous Lab")
    pot_lab = FloatField("Potassium Lab")
    sod_lab = IntegerField("Sodium Lab")
    dial_lab = FloatField("Dialysis Adequacy Lab")
    lab_time = DateTimeField("Lab Results Time", format='%Y-%m-%d %H:%M:%S')
    pat_id = SelectField("Patient Select")
    dial_id = SelectField("Dialysis Type Select")
    submit = SubmitField("Edit Lab Result")


class NewFood(FlaskForm):
    food_name = StringField("Food Name", validators=[DataRequired()])
    amount = IntegerField("Serving Size (grams)")
    phosphorous_content = IntegerField("Phosphorous Content")  # need to add units
    sodium_content = IntegerField("Sodium Content")
    calories = IntegerField("Calories")
    potassium_content = IntegerField("Potassium Content")
    submit = SubmitField("Create New Food")


class EditFood(FlaskForm):
    food_id = IntegerField(
        "Food ID", validators=[DataRequired()]
    )  # find a way to get rid of this, just use food_name?? (consider duplicate names)
    food_name = StringField("Food Name", validators=[DataRequired()])
    phosphorous_content = IntegerField("Phosphorous Content")  # need to add units
    sodium_content = IntegerField("Phosphorous Content")
    calories = IntegerField("Calories")
    potassium_content = IntegerField("Potassium Content")
    amount = IntegerField("Serving Size")
    submit = SubmitField("Update Food")


class NewDialysisForm(FlaskForm):
    name = StringField("Name of Dialysis Type", validators=[DataRequired()])
    location_type = StringField("Location Type", validators=[DataRequired()])
    adequacy_standard = FloatField("Adequacy Standard", validators=[DataRequired()])
    submit = SubmitField("Create New Dialysis Form")


class EditDialysisForm(FlaskForm):
    dialysis_id = IntegerField("Dialysis ID", validators=[DataRequired()])
    name = StringField("Name of Dialysis Type", validators=[DataRequired()])
    location_type = StringField("Location Type", validators=[DataRequired()])
    adequacy_standard = FloatField("Adequacy Standard", validators=[DataRequired()])
    submit = SubmitField("Edit Dialysis Type")


class NewPatientFood(FlaskForm):  # why are we using a composite primary key??
    food_id = SelectField("Food ID", validators=[DataRequired()])
    patient_id = SelectField("Patient ID", validators=[DataRequired()])
    food_time = DateTimeField("Consumption Time", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Create New PatientFood")


class EditPatientFood(FlaskForm):
    food_id = SelectField("Food", validators=[DataRequired()])
    patient_id = SelectField("Patient", validators=[DataRequired()])
    food_time = DateTimeField("Consumption Time", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Edit Patient-Food")

def search_bar(sample_tuple, search_term):
    """
    Recieves a tuple containing dictionary items and a search_term
    Returns a tuple containing dictionary items that have a value that matches the search_term
    """
    search_term = str(search_term)
    res = list()
    for x_dict in sample_tuple:
        for x in x_dict.values():
            if search_term in str(x):
                res.append(x_dict)
                break

    return tuple(res)

# Routes


@app.route("/")
def home():
    return render_template("index.html")


# Patients


@app.route("/patients", methods=["POST", "GET"])
def patients_view():
    q = request.args.get('q')
    gender = None
    form = NewPatient()
    if request.method == "GET":
        query = "SELECT patient_id, last_name, first_name, age, gender, height, weight FROM Patients;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()  # results should be a tuple containing dictionary items
        if q:
            results = search_bar(results,q)
        return render_template("patients.html", form=form, patients=results)
    if request.method == "POST":
        last_name = request.form["lname"]
        first_name = request.form["fname"]
        age = request.form["age"]
        gender = request.form["gender"]
        height = request.form["height"]
        weight = request.form["weight"]
        if gender == "":
            query = "INSERT INTO Patients (last_name, first_name, age, height, weight) VALUES (%s, %s, %s, %s, %s);"
            db.execute_query(
                db_connection=db_connection, query=query, query_params=(last_name, first_name, age, height, weight)
            )
            return redirect(url_for("patients_view"))
        else:
            query = "INSERT INTO Patients (last_name, first_name, age, gender, height, weight) VALUES (%s, %s, %s, %s, %s, %s);"
            db.execute_query(
                db_connection=db_connection,
                query=query,
                query_params=(last_name, first_name, age, gender, height, weight),
            )
            return redirect(url_for("patients_view"))


@app.route("/delete_patient/<int:patient_id>", methods=["POST", "GET"])
def delete_patient(patient_id):
    if request.method == "POST":
        query = "DELETE FROM Patients WHERE patient_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (patient_id,))
        mysql.connection.commit()
        return redirect(url_for("patients_view"))
    else:
        return render_template("delete_patient.html", patient_id=patient_id)

@app.route("/update_patient/<int:patient_id>", methods=["POST","GET"])
@app.route("/update_patient/", methods=["POST","GET"])
def update_patient(patient_id=None):
    form = EditPatient()
    if request.method == "GET":
        return render_template("update_patient.html", form=form, patient_id=patient_id)
    if request.method == "POST":
        pat_id = patient_id
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
        #cur = mysql.connection.cursor()
        #cur.execute(query, (last_name, first_name, age, gender, height, weight, pat_id))
        #mysql.connection.commit()
        db.execute_query(db_connection=db_connection, query=query, query_params=(last_name, first_name, age, gender, height, weight, pat_id))
    return redirect(url_for("patients_view"))

# Foods


@app.route("/foods", methods=["POST", "GET"])
def foods_view():
    form = NewFood()
    if request.method == "GET":
        query = "SELECT food_id, food_name, amount, phosphorous_content, sodium_content, calories, potassium_content FROM Foods;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("foods.html", form=form, foods=results)

    if request.method == "POST":
        food_name = request.form["food_name"]
        amount = request.form["amount"]
        phosphorous_content = request.form["phosphorous_content"]
        sodium_content = request.form["sodium_content"]
        calories = request.form["calories"]
        potassium_content = request.form["potassium_content"]
        amount = request.form["amount"]

        query = "INSERT INTO Foods (food_name, amount, phosphorous_content, sodium_content, calories, potassium_content) VALUES (%s, %s, %s, %s, %s, %s);"
        db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(food_name, amount, phosphorous_content, sodium_content, calories, potassium_content),
        )
        return redirect(url_for("foods_view"))


@app.route("/delete_foods/<int:food_id>", methods=["POST", "GET"])
def delete_foods(food_id):
    if request.method == "POST":
        query = "DELETE FROM Foods WHERE food_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (food_id,))
        mysql.connection.commit()
        return redirect(url_for("foods_view"))
    else:
        return render_template("delete_foods.html", food_id=food_id)

@app.route("/update_food/<int:food_id>", methods=["POST","GET"])
@app.route("/update_food/", methods=["POST","GET"])
def update_food(food_id=None):
    form = EditFood()
    if request.method == "GET":
        return render_template("update_food.html", form=form, food_id=food_id)
    if request.method == "POST":
        food_name = request.form["food_name"]
        amount = request.form["amount"]
        phosphorous_content = request.form["phosphorous_content"]
        sodium_content = request.form["sodium_content"]
        calories = request.form["calories"]
        potassium_content = request.form["potassium_content"]
        amount = request.form["amount"]
        query = """UPDATE Foods
    SET food_name = %s, phosphorous_content = %s, sodium_content = %s, calories = %s, 
    potassium_content = %s, amount = %s
    WHERE food_id = %s;"""
        db.execute_query(db_connection=db_connection, query=query, query_params=(food_name, phosphorous_content, sodium_content, calories, potassium_content, amount, food_id))
    return redirect(url_for("foods_view"))

# Lab Results


@app.route("/lab_results", methods=["POST", "GET"])
def labs_view():
    form = NewLabResult()
    if request.method == "GET":
        query = """
        SELECT Lab_Results.lab_id, CONCAT(Patients.first_name, " ", Patients.last_name) as "Patient Name", Dialysis_Forms.name as "Dialysis Type",
Lab_Results.phosphorus_lab as "Phosphorous Lab", Lab_Results.potassium_lab as "Potassium Lab", Lab_Results.sodium_lab as "Sodium Lab", 
Lab_Results.dialysis_adequacy_lab as "Dialysis Adequacy", Lab_Results.lab_results_time as "Time" FROM Lab_Results
JOIN Patients on Lab_Results.Patients_patient_id = Patients.patient_id 
JOIN Dialysis_Forms on Lab_Results.Dialysis_Forms_dialysis_id = Dialysis_Forms.dialysis_id;"""
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        query2 = """
        SELECT patient_id, 
CONCAT(first_name, ' ', last_name) as Name 
FROM Patients;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        patients_dropdown = cursor.fetchall()   
        # patients_dropdown is a tuple consisting of dictionaries:
        # for example: ({'patient_id': 1, 'Name': 'Arlene Smith'}, {'patient_id': 2, 'Name': 'f f'}, {'patient_id': 3, 'Name': 'Kayla Harrison'}, {'patient_id': 4, 'Name': 'Henry Jackson'}, {'patient_id': 10, 'Name': '6 65'})
        form.pat_id.choices = [(p['patient_id'],p['Name']) for p in patients_dropdown]
        query3 = "SELECT dialysis_id, name FROM Dialysis_Forms;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        dialyis_dropdown = cursor.fetchall()
        form.dial_id.choices = [(d['dialysis_id'],d['name']) for d in dialyis_dropdown]
        return render_template("lab_results.html", form=form, lab_data=results)
    if request.method == "POST":
        phos_lab = request.form["phos_lab"]
        pot_lab = request.form["pot_lab"]
        sod_lab = request.form["sod_lab"]
        dial_lab = request.form["dial_lab"]
        lab_time = request.form["lab_time"]
        pat_id = request.form["pat_id"]
        dial_id = request.form["dial_id"]
        for item in (phos_lab, pot_lab, sod_lab, dial_lab, lab_time, pat_id, dial_id):
            if item == "":
                item = "NULL"
        query = """INSERT INTO Lab_Results (phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time, 
Patients_patient_id, Dialysis_Forms_dialysis_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(phos_lab, pot_lab, sod_lab, dial_lab, lab_time, pat_id, dial_id),
        )
        return redirect(url_for("labs_view"))


@app.route("/delete_labs/<int:lab_id>", methods=["POST", "GET"])
def delete_labs(lab_id):
    if request.method == "POST":
        query = "DELETE FROM Lab_Results WHERE lab_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (lab_id,))
        mysql.connection.commit()
        return redirect(url_for("labs_view"))
    else:
        return render_template("delete_labs.html", lab_id=lab_id)

@app.route("/update_lab_results/<int:lab_id>", methods=["POST","GET"])
@app.route("/update_lab_results/", methods=["POST","GET"])
def update_lab_result(lab_id=None):
    form = EditLabResult()
    if request.method == "GET":
        query2 = """
        SELECT patient_id, 
CONCAT(first_name, ' ', last_name) as Name 
FROM Patients;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        patients_dropdown = cursor.fetchall()  
        form.pat_id.choices = [(p['patient_id'],p['Name']) for p in patients_dropdown]
        query3 = "SELECT dialysis_id, name FROM Dialysis_Forms;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        dialyis_dropdown = cursor.fetchall()
        form.dial_id.choices = [(d['dialysis_id'],d['name']) for d in dialyis_dropdown]
        return render_template("update_lab_results.html", form=form, lab_id=lab_id)
    if request.method == "POST":
        phos_lab = request.form["phos_lab"]
        pot_lab = request.form["pot_lab"]
        sod_lab = request.form["sod_lab"]
        dial_lab = request.form["dial_lab"]
        lab_time = request.form["lab_time"]
        pat_id = request.form["pat_id"]
        dial_id = request.form["dial_id"]
        query = """UPDATE Lab_Results
    SET phosphorus_lab = %s, potassium_lab = %s, sodium_lab = %s, dialysis_adequacy_lab = %s, 
    Lab_Results_time = %s, Patients_patient_id = %s, Dialysis_Forms_dialysis_id = %s
    WHERE lab_id = %s;"""
        db.execute_query(db_connection=db_connection, query=query, query_params=(phos_lab, pot_lab, sod_lab, dial_lab, lab_time, pat_id, dial_id, lab_id))
    return redirect(url_for("labs_view"))

# Dialysis Forms


@app.route("/dialysis_forms", methods=["POST", "GET"])
def dialysis_forms_view():
    form = NewDialysisForm()
    if request.method == "GET":
        query = "SELECT dialysis_id, name, location_type, adequacy_standard FROM Dialysis_Forms;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("dialysis_forms.html", form=form, dialysis_data=results)
    if request.method == "POST":
        name = request.form["name"]
        location_type = request.form["location_type"]
        adequacy_standard = request.form["adequacy_standard"]

        query = "INSERT INTO Dialysis_Forms (name, location_type, adequacy_standard) VALUES (%s, %s, %s);"
        db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(name, location_type, adequacy_standard),
        )
        return redirect(url_for("dialysis_forms_view"))


@app.route("/delete_dialysis_form/<int:dialysis_id>", methods=["POST", "GET"])
def delete_dialysis_form(dialysis_id):
    if request.method == "POST":
        query = "DELETE FROM Dialysis_Forms WHERE dialysis_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (dialysis_id,))
        mysql.connection.commit()
        return redirect(url_for("dialysis_forms_view"))
    else:
        return render_template("delete_dialysis_form.html", dialysis_id=dialysis_id)

@app.route("/update_dialysis_type/<int:dialysis_id>", methods=["POST","GET"])
@app.route("/update_dialysis_type/", methods=["POST","GET"])
def update_dialysis_type(dialysis_id=None):
    form = EditDialysisForm()
    if request.method == "GET":
        return render_template("update_dialysis_type.html", form=form, dialysis_id=dialysis_id)
    if request.method == "POST":
        name = request.form["name"]
        location_type = request.form["location_type"]
        adequacy_standard = request.form["adequacy_standard"]
        query = """UPDATE Dialysis_Forms
    SET name = %s, location_type = %s, adequacy_standard = %s
    WHERE dialysis_id = %s;"""
        db.execute_query(db_connection=db_connection, query=query, query_params=(name, location_type, adequacy_standard, dialysis_id))
    return redirect(url_for("dialysis_forms_view"))

# Patient Foods


@app.route("/patients_foods", methods=["POST", "GET"])
def patients_foods_view():
    form = NewPatientFood()
    if request.method == "GET":
        query = """
        SELECT Patients_Food.patients_food_id as "id", Foods.food_name as "Food Name", CONCAT(Patients.first_name, " ", Patients.last_name) as "Patient Name",
    Patients_Food.patient_food_time as "Time consumed" from Patients_Food
    JOIN Foods on Patients_Food.Foods_food_id = Foods.food_id
    JOIN Patients on Patients_Food.Patients_patient_id = Patients.patient_id;
    """
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        query_foods = "SELECT food_id, food_name FROM Foods;"
        cursor = db.execute_query(db_connection=db_connection, query=query_foods)
        foods_dropdown = cursor.fetchall()
        form.food_id.choices = [(f['food_id'],f['food_name']) for f in foods_dropdown]
        query2 = """
        SELECT patient_id, 
CONCAT(first_name, ' ', last_name) as Name 
FROM Patients;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        patients_dropdown = cursor.fetchall()   
        form.patient_id.choices = [(p['patient_id'],p['Name']) for p in patients_dropdown]
        return render_template("patients_foods.html", form=form, patient_foods=results)
        
    if request.method == "POST":
        food_id = request.form["food_id"]
        patient_id = request.form["patient_id"]
        food_time = request.form["food_time"]

        query = "INSERT INTO Patients_Food (Foods_food_id, Patients_patient_id, patient_food_time) VALUES (%s, %s, %s);"
        db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(food_id, patient_id, food_time),
        )
        return redirect(url_for("patients_foods_view"))

@app.route("/delete_patients_food/<int:patients_food_id>", methods=["POST", "GET"])
def delete_patients_food(patients_food_id):
    if request.method == "POST":
        query = "DELETE FROM Patients_Food WHERE patients_food_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (patients_food_id,))
        mysql.connection.commit()
        return redirect(url_for("patients_foods_view"))
    else:
        return render_template("delete_patient.html", patients_food_id=patients_food_id)


@app.route("/update_patients_food/<int:patients_food_id>", methods=["POST","GET"])
@app.route("/update_patients_food/", methods=["POST","GET"])
def update_patients_food(patients_food_id=None):
    form = EditPatientFood()
    if request.method == "GET":
        query2 = """
        SELECT patient_id, 
CONCAT(first_name, ' ', last_name) as Name 
FROM Patients;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        patients_dropdown = cursor.fetchall()  
        form.patient_id.choices = [(p['patient_id'],p['Name']) for p in patients_dropdown]
        query3 = "SELECT food_id, food_name FROM Foods;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        foods_dropdown = cursor.fetchall()
        form.food_id.choices = [(f['food_id'], f['food_name']) for f in foods_dropdown]
        return render_template("update_patients_food.html", form=form, patients_food_id=patients_food_id)
    if request.method == "POST":
        food_id = request.form["food_id"]
        patient_id = request.form["patient_id"]
        food_time = request.form["food_time"]
        query = """UPDATE Patients_Food
    SET Foods_food_id = %s, Patients_patient_id = %s, patient_food_time = %s
    WHERE patients_food_id = %s;"""
        db.execute_query(db_connection=db_connection, query=query, query_params=(food_id, patient_id, food_time, patients_food_id))
    return redirect(url_for("patients_foods_view"))

# Listener

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9112))
    app.run(port=port, debug=True)


# Code Citation
# https://github.com/osu-cs340-ecampus/flask-starter-app#delete
# https://wtforms.readthedocs.io/en/3.0.x/
# Grinberg, M. (2018). Flask web development: developing web applications with python. " O&#x27;Reilly Media, Inc."