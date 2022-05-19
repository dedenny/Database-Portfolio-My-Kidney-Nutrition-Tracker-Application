from flask import Flask,render_template, request, json, redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

patients_headings= ("patient_id", "last_name","first_name", "age", "gender", "height", "weight")
patients_data= (
    ("1", "Smith", "Arlene", "55", "F", "64", "145"),
    ("2", "Rogers", "Christopher", "63", "M", "72", "180"),
    ("3", "Harrison", "Kayla", "68", "F", "65", "125"),
    ("4", "Jackson", "Henry", "74", "M", "75", "200"),
    ("5", "Wonders", "Brenda", "91", "F", "60", "92")
)

foods_headings=("food_id", "name", "amount", "phosphorus_content", "sodium_content", "calories", "potassium_content")
foods_data= (
    ("1", "Milk, Whole", "128", "251", "94.6", "152", "374"),
    ("2", "Beef,loin, top loin steak", "284", "585", "128", "423", "801"),
    ("3", "Chicken, breast", "174", "419", "81.8", "275", "597"),
    ("4", "Yogurt, Greek, nonfat", "156", "212", "56.2", "92", "220"),
    ("5", "Kale", "100", "55", "53", "43", "348")
    )

dialysis_headings=("dialysis_id", "name","location_type", "adequacy_standard")
dialysis_data=(
    ("1", "hemodialysis FMC", "incenter", "1.2"),
    ("2", "peritoneal Baxter", "home", "1.7")
)

labs_headings=("lab_id","patient_id","phosphorus_lab","potassium_lab", "sodium_lab", "dialysis_adequacy_lab", "lab_results_time")
labs_data=( 
    ("1", "1","3.5", "3.4", "135", "1.2","2022-05-07 23:22:05"),
    ("2", "2","5.5", "3", "142", "1.7","2022-05-08 18:36:10"),
    ("3", "3","6.5", "2.8", "146", "1.1","2022-05-01 20:20:06"),
    ("4", "4","10.5", "6.6", "144", "0.6","2022-05-07 18:01:55"),
     ("5", "5","7.2", "4.5", "134", "2.2","2022-05-11 10:19:25")
)

patients_foods_headings=("patient_id", "Last Name", "First Name", "Food Name", "Patient Food Time")
patients_foods_data=(
("1", "Smith", "Arlene","Milk, Whole", "2022-05-10 15:40:11"),
("2", "Rogers", "Christopher","Beef,loin, top loin steak", "2022-05-20 18:32:04"),
("3", "Harrison", "Kayla","Chicken, breast", "2022-05-15 12:08:12"),
("4", "Jackson", "Henry","Yogurt, Greek, nonfat", "2022-05-11 15:07:55"),
("5", "Wonders", "Brenda", "Kale", "2022-05-16 10:22:28")
)

@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/patients")
def patients_view():
    return render_template("patients.html", patients_headings=patients_headings, patients_data=patients_data)

@app.route("/foods")
def foods_view():
    return render_template("foods.html", foods_headings=foods_headings, foods_data=foods_data)

@app.route("/lab_results")
def labs_view():
    return render_template("lab_results.html", labs_headings=labs_headings, labs_data=labs_data)

@app.route("/dialysis_forms")
def dialysis_forms_view():
    return render_template("dialysis_forms.html", dialysis_headings=dialysis_headings, dialysis_data=dialysis_data)

@app.route("/patients_foods")
def patients_foods_view():
    return render_template("patients_foods.html", patients_foods_headings=patients_foods_headings, patients_foods_data=patients_foods_data)
