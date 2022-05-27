/*
Page population queries:
*/
--Populate Patients page
SELECT patient_id, last_name, first_name, age, gender, height, weight FROM Patients;

--Populate Foods page
SELECT food_id, food_name, amount, phosphorous_content, sodium_content, calories, potassium_content FROM Foods;

--Populate Lab Results page
SELECT lab_id, phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time FROM Lab_Results;

--Populate Dialysis Forms page
SELECT dialysis_id, name, location_type, adequacy_standard FROM Dialysis_Forms;

--Populate Patients_food page
SELECT Foods.food_name as "Food Name", CONCAT(Patients.first_name, " ", Patients.last_name) as "Patient Name",
Patients_food.patient_food_time as "Time consumed" from patients_food
JOIN Foods on Patients_food.Foods_food_id = Foods.food_id
JOIN Patients on Patients_Food.Patients_patient_id = Patients.patient_id;

/*
Edit queries:
*/
--Get a single patient for edit patient form
SELECT patient_id, last_name, first_name, age, gender, height, weight FROM patients
WHERE patient_id = :patient_id_from_patients_page;

--Get a single food for edit foods form
SELECT food_id, name, amount, phosphorous_content, sodium_content, calories, potassium_content FROM foods
WHERE food_id = :food_id_from_foods_page;

--get a single lab result for edit lab_results form
SELECT lab_id, phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time FROM lab_results
WHERE lab_id = :lab_id_from_labs_page;

--get a single dialysis type for edit dialysis_types form
SELECT dialysis_id, name, location_type, adequacy_standard FROM dialysis_forms
WHERE dialysis_id = :dialysis_id_from_dialysis_types_page;

/*
Insert queries:
*/
--Add a patient
INSERT INTO patients (last_name, first_name, age, gender, height, weight) VALUES
(:lname_input, :fname_input, :age_input, :gender_input, :height_input, :weight_input);

--Add a food
INSERT INTO foods (food_name, phosphorous_content, sodium_content, calories, potassium_content, amount) VALUES
(:food_name_input, :phos_content_input, :sodium_content_input, :calories_input, :potassium_content_input, :amount_input);

--Add a lab_result
INSERT INTO lab_results (phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time
Patients_patient_id,Dialysis_Forms_dialysis_id) VALUES
(:phos_lab_input, :potassium_lab_input, :sodium_lab_input, :dialysis_adequacy_lab_input, :lab_results_time_input
:patient_id_input, :dialysis_id_input);

--add a new form of dialysis
INSERT INTO dialysis_forms (name, location_type, adequacy_standard) VALUES
(:dialysis_name_input, :location_input, :adequacy_standard_input);

/*
Delete queries:
*/
--Delete a patient
DELETE FROM patient WHERE patient_id = :patient_id_selected_from_patients_page;
--Delete from Foods
DELETE FROM Foods WHERE food_id = :food_id_selected_from_patients_page;
--Delete from lab_results
DELETE FROM lab_results WHERE lab_id = :lab_id_selected_from_labs_page;
--Delete from dialysis_forms
DELETE FROM dialysis_forms WHERE dialysis_id = :dialysis_id_selected_from_dialysis_page;

/*
Drop-down queries:
*/
--get types of dialysis to populate dialysis type dropdown
SELECT dialysis_id, name FROM Dialysis_Forms

--get types of dialysis to populate location type dropdown
SELECT dialysis_id, location_type FROM Dialysis_forms

--get patients to populate drop down for patients
SELECT patient_id, 
CONCAT(first_name, ' ', last_name) as Name 
FROM Patients;

--get foods to populate foods dropdown
SELECT food_id, food_name FROM Foods;

--get types of dialysis and their id for the lab_results dropdown
SELECT dialysis_id, name FROM Dialysis_Forms;

/*
Update queries:
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

--update the food in patients_food:
UPDATE Patients_Food
SET Foods_food_id = :Foods_food_id_from_update_form
WHERE food_patient_id = food_patient_id_from_update_form;

--update the patient in patients_food:
UPDATE Patients_Food
SET Patients_patient_id = :Patients_patient_id_from_update_form
WHERE food_patient_id = food_patient_id_from_update_form;

/*
Other queries:
*/
--Associate a person with a food
INSERT INTO Patients_Food (Patients_patient_id, Foods_food_id, patient_food_time) VALUES
(:patient_id_pat_food_input, :food_id_pat_food_input, :datetime_pate_food);

--dissassociate a person with a food
DELETE FROM patients_food WHERE patients_patient_id = :patient_id_selected_from_patient_food_table AND
Foods_food_id = :food_id_selected_from_patient_food_table;

--Show all the food that a given patient ate on a given date
SELECT Foods_food_id, DATE(patient_food_time) FROM Patients_Food 
WHERE patients_patient_id = :patients_id_from_patients_food_page 
AND DATE(patient_food_time) = :date_from_patients_food_page;

--Show all the food that a patient has eaten on all dates
SELECT Patients_Food.Foods_food_id,Foods.food_name, DATE(Patients_food.patient_food_time) FROM Patients_Food 
JOIN Foods ON Patients_food.Foods_food_id = Foods.food_id
WHERE patients_patient_id = :patients_id_from_patients_food_page ;


INSERT INTO Lab_Results 
(phosphorus_lab, potassium_lab, sodium_lab, dialysis_adequacy_lab, lab_results_time,
Patients_patient_id,Dialysis_Forms_dialysis_id) 
VALUES
('.4', 
'.4', 
'4', 
'.4', 
'2022-05-11 10:19:25', 
'10', '1');