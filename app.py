
import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Patient Management System",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Patient Management System")
st.write("Manage patient records using Streamlit and FastAPI")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Register Patient",
        "View Patients",
        "Search Patient",
        "Update Patient",
        "Delete Patient"
    ]
)

# 1. REGISTER PATIENT
if menu == "Register Patient":

    st.subheader("Patient Registration")

    with st.form("patient_form"):

        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox(
            "Gender", ["Male", "Female", "Other"]
        )
        contact = st.text_input("Contact Number")
        disease = st.text_input("Disease")
        doctor = st.text_input("Doctor Name")

        submit = st.form_submit_button("Register Patient")

        if submit:

            patient_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "contact": contact,
                "disease": disease,
                "doctor": doctor
            }

            try:
                response = requests.post(
                    f"{BASE_URL}/patients/",
                    json=patient_data
                )

                if response.status_code == 200:
                    st.success("Patient registered successfully!")
                    st.json(response.json())
                else:
                    st.error(response.text)

            except requests.exceptions.RequestException:
                st.error("Unable to connect to FastAPI")

# 2. VIEW ALL PATIENTS
elif menu == "View Patients":

    st.subheader("All Patient Records")

    try:
        response = requests.get(f"{BASE_URL}/patients/")

        if response.status_code == 200:

            patients = response.json()

            if patients:
                df = pd.DataFrame(patients)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No patient records found")

        else:
            st.error(response.text)

    except requests.exceptions.RequestException:
        st.error("Unable to connect to FastAPI")

# 3. SEARCH PATIENT
elif menu == "Search Patient":

    st.subheader("Search Patient")

    patient_id = st.number_input(
        "Enter Patient ID",
        min_value=1,
        step=1
    )

    if st.button("Search"):

        try:
            response = requests.get(
                f"{BASE_URL}/patients/{patient_id}"
            )

            if response.status_code == 200:
                st.success("Patient found")
                st.json(response.json())
            else:
                st.error("Patient not found")

        except requests.exceptions.RequestException:
            st.error("Unable to connect to FastAPI")

# 4. UPDATE PATIENT
elif menu == "Update Patient":

    st.subheader("Update Patient Details")

    patient_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1
    )

    name = st.text_input("Updated Name")
    age = st.number_input(
        "Updated Age",
        min_value=1,
        max_value=120
    )
    gender = st.selectbox(
        "Updated Gender",
        ["Male", "Female", "Other"]
    )
    contact = st.text_input("Updated Contact")
    disease = st.text_input("Updated Disease")
    doctor = st.text_input("Updated Doctor")

    if st.button("Update Patient"):

        updated_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "contact": contact,
            "disease": disease,
            "doctor": doctor
        }

        try:
            response = requests.put(
                f"{BASE_URL}/patients/{patient_id}",
                json=updated_data
            )

            if response.status_code == 200:
                st.success("Patient updated successfully!")
                st.json(response.json())
            else:
                st.error(response.text)

        except requests.exceptions.RequestException:
            st.error("Unable to connect to FastAPI")

# 5. DELETE PATIENT
elif menu == "Delete Patient":

    st.subheader("Delete Patient Record")

    patient_id = st.number_input(
        "Enter Patient ID",
        min_value=1,
        step=1
    )

    confirm = st.checkbox(
        "I confirm that I want to delete this patient"
    )

    if st.button("Delete Patient"):

        if confirm:

            try:
                response = requests.delete(
                    f"{BASE_URL}/patients/{patient_id}"
                )

                if response.status_code in [200, 204]:
                    st.success("Patient deleted successfully!")
                else:
                    st.error(response.text)

            except requests.exceptions.RequestException:
                st.error("Unable to connect to FastAPI")

        else:
            st.warning("Please confirm before deleting")