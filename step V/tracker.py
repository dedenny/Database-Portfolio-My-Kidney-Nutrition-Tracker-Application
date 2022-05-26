import os
import re

from flask import Flask, json, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from jmespath import search
from wtforms import StringField, SubmitField, IntegerField, FloatField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

import database.db_connector as db

# Configuration

app = Flask(__name__)
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
    lab_time = DateTimeField("Lab Results Time")
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
    lab_time = DateTimeField("Lab Results Time")
    pat_id = SelectField("Patient Select")
    dial_id = SelectField("Dialysis Type Select")
    submit = SubmitField("Edit Lab Result")


class NewFood(FlaskForm):
    food_name = StringField("Food Name", validators=[DataRequired()])
    amount = IntegerField("Serving Size")
    phosphorous_content = IntegerField("Phosphorous Content")  # need to add units
    sodium_content = IntegerField("Phosphorous Content")
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


class NewPatientFood(FlaskForm):  # why are we using a composite primary key??
    food_id = IntegerField("Food ID", validators=[DataRequired()])
    patient_id = IntegerField("Patient ID", validators=[DataRequired()])
    food_time = DateTimeField("Consumption Time", validators=[DataRequired()])
    submit = SubmitField("Create New PatientFood")


# class EditPatientFood(FlaskForm):
#     food_id = IntegerField("Food ID", validators=[DataRequired()])
#     patient_id = IntegerField("Food ID", validators=[DataRequired()])
#     food_time = DateTimeField("Consumption Time", validators=[DataRequired()])


# Routes


@app.route("/")
def home():
    return render_template("index.html")


# Patients


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


# Lab Results


@app.route("/lab_results", methods=["POST", "GET"])
def labs_view():
    form = NewLabResult()
    if request.method == "GET":
        query = "SELECT lab_id, phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time FROM Lab_Results;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
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
        query = """INSERT INTO lab_results (phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time
Patients_patient_id,Dialysis_Forms_dialysis_id) VALUES
(%s, %s, %s, %s, %s
%s, %s);"""
        db.execute_query(
            db_connection=db_connection,
            query=query,
            query_parms=(phos_lab, pot_lab, sod_lab, dial_lab, lab_time, pat_id, dial_id),
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


# Patient Foods


@app.route("/patients_foods", methods=["POST", "GET"])
def patients_foods_view():
    form = NewPatientFood()
    if request.method == "GET":
        query = """
        SELECT Foods.food_name as "Food Name", CONCAT(Patients.first_name, " ", Patients.last_name) as "Patient Name",
    Patients_Food.patient_food_time as "Time consumed" from Patients_Food
    JOIN Foods on Patients_Food.Foods_food_id = Foods.food_id
    JOIN Patients on Patients_Food.Patients_patient_id = Patients.patient_id;
    """
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("patients_foods.html", form=form, patient_foods=results)
    if request.method == "POST":
        food_id = request.form["food_id"]
        patient_id = request.form["patient_id"]
        food_time = request.form["food_time"]

        query = "INSERT INTO Dialysis_Forms (food_id, patient_id, food_time) VALUES (%s, %s, %s);"
        db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(food_id, patient_id, food_time),
        )
        return redirect(url_for("patients_foods_view"))


# Listener

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9112))
    app.run(port=port, debug=True)


# Code Citation
# https://github.com/osu-cs340-ecampus/flask-starter-app#delete
