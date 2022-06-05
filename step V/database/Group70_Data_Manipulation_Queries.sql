/*
Table page population queries:
*/
--Populate Patients page from Patients Table
SELECT patient_id, last_name as 'Last Name', first_name as 'First Name', age as Age, 
gender as Gender, height as 'Height (in)', weight as 'Weight (lbs)' FROM Patients;

--Populate Foods page from Foods Table
SELECT food_id, food_name as 'Food Name', amount as 'Serving Size (g)', phosphorous_content as 'Phosphorous Content (mg)',
sodium_content as 'Sodium Content (mg)', calories as 'Calories', potassium_content as 'Potassium Content (mg)' FROM Foods;

--Populate Lab Results page from Lab_Results Table
SELECT Lab_Results.lab_id, CONCAT(Patients.first_name, " ", Patients.last_name) as "Patient Name", Dialysis_Forms.name as "Dialysis Type",
Lab_Results.phosphorus_lab as "Phosphorous Lab (mg/dL)", Lab_Results.potassium_lab as "Potassium Lab (mEq/L)", Lab_Results.sodium_lab as "Sodium Lab (mEq/L)", 
Lab_Results.dialysis_adequacy_lab as "Dialysis Adequacy (Kt/v)", Lab_Results.lab_results_time as "Time" FROM Lab_Results
LEFT JOIN Patients on Lab_Results.Patients_patient_id = Patients.patient_id 
LEFT JOIN Dialysis_Forms on Lab_Results.Dialysis_Forms_dialysis_id = Dialysis_Forms.dialysis_id;

--Populate Dialysis Forms page from Dialysis_Forms Table
SELECT dialysis_id, name, location_type, adequacy_standard FROM Dialysis_Forms;

--Populate Patients_food page from Patients_Food Table
SELECT Foods.food_name as "Food Name", CONCAT(Patients.first_name, " ", Patients.last_name) as "Patient Name",
Patients_food.patient_food_time as "Time consumed" from patients_food
JOIN Foods on Patients_food.Foods_food_id = Foods.food_id
JOIN Patients on Patients_Food.Patients_patient_id = Patients.patient_id;


/*
Editing: selecting a single data point to populate the edit forms:
*/
--Find existing data to populate the edit Patients form
SELECT patient_id, last_name, first_name, age, gender, height, weight FROM patients
WHERE patient_id = :patient_id_from_patients_page;

--Find existing data to populate the edit Foods form
SELECT food_id, name, amount, phosphorous_content, sodium_content, calories, potassium_content FROM foods
WHERE food_id = :food_id_from_foods_page;

--Find existing data to populate the edit Lab_Results form
SELECT lab_id, phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time FROM lab_results
WHERE lab_id = :lab_id_from_labs_page;

--Find existing data to populate the edit Dialysis_Forms form
SELECT dialysis_id, name, location_type, adequacy_standard FROM dialysis_forms
WHERE dialysis_id = :dialysis_id_from_dialysis_types_page;

--Find existing data to populate the edit Patients_Food form
SELECT Foods_food_id, Patients_patient_id, patient_food_time FROM Patients_Food WHERE patients_food_id = 
:patient_food_id_input;

/*
Editing:
Update queries: sample queries to get existing data for an entry to populate the edit screens
*/
--update an entry in Lab_Results:
UPDATE Lab_Results
SET phosphorus_lab = :phos_lab_from_update_form, potassium_lab = :potassium_lab_from_update_form, sodium_lab = :sodium_lab_from_update_form, 
dialysis_adequacy_lab = :dialysis_adequacy_from_update_form, lab_results = :lab_time_from_update_form
WHERE lab_id = :lab_id_from_input_form;

--update an entry in Dialysis_Forms:
UPDATE Dialysis_Forms
SET name = :dialysis_name_from_update_form, location_type = :location_type_from_update_form, adequacy_standard = :adequacy_standard_from_update_form
WHERE dialysis_id = :dialysis_id_from_input_form;

--update an entry in Patients:
UPDATE Patients
SET last_name = :last_name_from_update_form, first_name = :first_name_from_update_form, age = :age_from_update_form, gender = :gender_from_update_form, 
height = :height_from_update_form, weight = :weight_from_update_form
WHERE patient_id = :patients_id_from_update_form;

--update an entry in Foods:
UPDATE Foods
SET food_name = :food_name_from_update_form, phosphorous_content = :phosphorous_content_from_update_form, sodium_content = :sodium_content_from_update_form,
calories = :calories_from_update_form, potassium_content = :potassium_content_from_update_form, amount = :amount_from_update_form
WHERE food_id = :food_id_from_update_form;

--update an entry in the Patients_Food table:
UPDATE Patients_Food
SET Foods_food_id = :food_id_input, Patients_patient_id = :patient_id_input, patient_food_time = :time_input
WHERE patients_food_id = :selected_patients_food_id;


/*
Insert queries:
*/
--Add a patient (with gender specified) to the Patients table
INSERT INTO patients (last_name, first_name, age, gender, height, weight) VALUES
(:lname_input, :fname_input, :age_input, :gender_input, :height_input, :weight_input);
--Add a patient (without gender specified) to the Patients table
INSERT INTO Patients (last_name, first_name, age, gender, height, weight) VALUES 
(:lname_input, :fname_input, :age_input, :height_input, :weight_input);

--Add a new food to the Foods table
INSERT INTO foods (food_name, phosphorous_content, sodium_content, calories, potassium_content, amount) VALUES
(:food_name_input, :phos_content_input, :sodium_content_input, :calories_input, :potassium_content_input, :amount_input);

--Note: because we allowed a lab result without a patient and/or a form of dialysis to be added, multiple insert queries
--were needed for this table

--Add a lab result to the Lab_Results table if patient and dialysis form are both specified
INSERT INTO lab_results (phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time
Patients_patient_id,Dialysis_Forms_dialysis_id) VALUES
(:phos_lab_input, :potassium_lab_input, :sodium_lab_input, :dialysis_adequacy_lab_input, :lab_results_time_input,
:patient_id_input, :dialysis_id_input);

--Add a lab result to the Lab_Results table if no patient is specified:
INSERT INTO Lab_Results (phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time) 
VALUES 
(:phos_lab_input, :potassium_lab_input, :sodium_lab_input, :dialysis_adequacy_lab_input, :lab_results_time_input,
:dialysis_id_input);

--Add a lab result to the Lab_Results table if no dialysis form is specified:
INSERT INTO Lab_Results (phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time, Dialysis_Forms_dialysis_id) 
VALUES 
(:phos_lab_input, :potassium_lab_input, :sodium_lab_input, :dialysis_adequacy_lab_input, :lab_results_time_input,
:patient_id_input);

--add a new form of dialysis to the Dialysis_Forms table
INSERT INTO dialysis_forms (name, location_type, adequacy_standard) VALUES
(:dialysis_name_input, :location_input, :adequacy_standard_input);

--add an entry to the Patients_Food table
INSERT INTO Patients_Food (Foods_food_id, Patients_patient_id, patient_food_time) VALUES 
(:Food_id_input, :patient_id_input, :time_consumed_input);

/*
Delete queries:
*/
--Delete a patient from the Patients table
DELETE FROM Patients WHERE patient_id = :selected_patient_id;
--Delete a food from the Foods table
DELETE FROM Foods WHERE food_id = :food_id_selected_from_patients_page;
--Delete a lab results entry from the Lab_Results table
DELETE FROM Lab_Results WHERE lab_id = :lab_id_selected_from_labs_page;
--Delete a form of dialysis from the Dialysis_Forms table
DELETE FROM Dialysis_Forms WHERE dialysis_id = :dialysis_id_selected_from_dialysis_page;
--Delete an entry from Patients_Food table
DELETE FROM Patients_Food WHERE patients_food_id = :patient_food_id;

/*
Drop-down queries:
*/
--get types of dialysis to populate dialysis type dropdown in the Lab Results Pages
SELECT dialysis_id, name FROM Dialysis_Forms

--get types of dialysis to populate location type dropdown in the Lab Results pages  (Not used)
SELECT dialysis_id, location_type FROM Dialysis_forms

--get patients to populate drop down for patients, used in both the Lab_Results pages and the Patients_Food pages
SELECT patient_id, 
CONCAT(first_name, ' ', last_name) as Name 
FROM Patients;

--get foods to populate foods dropdown, used to add and edit entries in the Patients_Food table
SELECT food_id, food_name FROM Foods;

--get types of dialysis and their id for the lab_results dropdown
SELECT dialysis_id, name FROM Dialysis_Forms;



/*
Other queries:
*/

--Show all the food that a given patient ate on a given date (not used)
SELECT Foods_food_id, DATE(patient_food_time) FROM Patients_Food 
WHERE patients_patient_id = :patients_id_from_patients_food_page 
AND DATE(patient_food_time) = :date_from_patients_food_page;

--Show all the food that a patient has eaten on all dates (not used)
SELECT Patients_Food.Foods_food_id,Foods.food_name, DATE(Patients_food.patient_food_time) FROM Patients_Food 
JOIN Foods ON Patients_food.Foods_food_id = Foods.food_id
WHERE patients_patient_id = :patients_id_from_patients_food_page ;
