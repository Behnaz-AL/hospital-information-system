
import streamlit as st
import pandas as pd
import pyodbc

st.set_page_config(
    page_title="Hospital Information System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Replace with your actual SSMS server name
SERVER = "localhost"

# Use the exact driver name from pyodbc.drivers()
DRIVER = "ODBC Driver 18 for SQL Server"


DATABASES = {
    "Patients": {
        "database": "PatientsDB",
        "table": "Patients",
        "fields": {
            "Name": "text",
            "Age": "int",
            "Gender": "text",
            "Phone": "text",
            "Diagnosis": "text"
        }
    },
    "Doctors": {
        "database": "DoctorsDB",
        "table": "Doctors",
        "fields": {
            "Name": "text",
            "Specialty": "text",
            "Phone": "text",
            "Department": "text"
        }
    },
    "Appointments": {
        "database": "AppointmentsDB",
        "table": "Appointments",
        "fields": {
            "PatientID": "int",
            "DoctorID": "int",
            "AppointmentDate": "text",
            "Reason": "text",
            "Status": "text"
        }
    },

    "Prescriptions": {
        "database": "PrescriptionsDB",
        "table": "Prescriptions",
        "fields": {
            "PatientID": "int",
            "MedicineName": "text",
            "Dosage": "text",
            "PrescriptionDate": "text",
            "Notes": "text"
        }
    }

}

def connect(database):
    connection_string = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string, timeout=5)


def read_data(database, table):
    with connect(database) as conn:
        if database == "AppointmentsDB":
            query = """
                SELECT
                    a.ID,
                    a.PatientID,
                    p.Name AS Patient,
                    a.DoctorID,
                    d.Name AS Doctor,
                    a.AppointmentDate,
                    a.Reason,
                    a.Status
                FROM AppointmentsDB.dbo.Appointments a
                LEFT JOIN PatientsDB.dbo.Patients p
                    ON a.PatientID = p.ID
                LEFT JOIN DoctorsDB.dbo.Doctors d
                    ON a.DoctorID = d.ID
                ORDER BY a.ID
            """
            return pd.read_sql_query(query, conn)

        return pd.read_sql_query(
            f"SELECT * FROM dbo.[{table}] ORDER BY ID",
            conn
        )



def save_data(database, table, fields, df, selected):
    columns = list(fields.keys())
    assignments = ", ".join(f"[{c}] = ?" for c in columns)

    with connect(database) as conn:
        cursor = conn.cursor()

        for _, row in df.iterrows():
            values = []

            for column in columns:
                value = row[column]

                if pd.isna(value):
                    raise ValueError(f"{column} cannot be empty.")

                if fields[column] == "int":
                    if float(value) != int(value):
                        raise ValueError(f"{column} must be a whole number.")

                    value = int(value)

                    if selected == "Patients" and column == "Age" and value < 1:
                        raise ValueError("Patient age must be greater than zero.")


                elif fields[column] == "float":
                    value = float(value)

                else:
                    value = str(value).strip()
                    if not value:
                        raise ValueError(
                            f"{column} cannot be empty."
                        )

                values.append(value)

            cursor.execute(
                f"UPDATE dbo.[{table}] SET {assignments} WHERE ID = ?",
                *values,
                int(row["ID"])
            )

        conn.commit()


def add_record(database, table, fields, values):
    columns = list(fields.keys())
    column_sql = ", ".join(f"[{c}]" for c in columns)
    placeholders = ", ".join("?" for _ in columns)

    with connect(database) as conn:
        conn.cursor().execute(
            f"INSERT INTO dbo.[{table}] "
            f"({column_sql}) VALUES ({placeholders})",
            *values
        )
        conn.commit()


def delete_record(database, table, record_id):
    with connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"DELETE FROM dbo.[{table}] WHERE ID = ?",
            int(record_id)
        )

        conn.commit()

col_title, col_database = st.columns([3, 1])

with col_title:
    st.title("🏥 Hospital Information System")
    st.caption("Manage patients, doctors, appointments, and prescriptions")

with col_database:
    selected = st.selectbox(
        "Choose a Service",
        list(DATABASES.keys())
    )

config = DATABASES[selected]
database = config["database"]
table = config["table"]
fields = config["fields"]

st.subheader(f"📋 {selected}")

try:

    df = read_data(database, table)

    st.metric("Total Records", len(df))

    search_text = st.text_input(
        "Search records",
        placeholder="Enter a name or keyword...",
        key=f"search_{selected}"
    )

    if search_text.strip():
        mask = df.astype(str).apply(
            lambda column: column.str.contains(
                search_text,
                case=False,
                regex=False,
                na=False
            )
        ).any(axis=1)

        df = df[mask]

    st.caption(f"Records displayed: {len(df)}")

    st.markdown("#### 📑 Records")

    display_df = df.copy()
    display_df.insert(0, "Select", False)

    edited_df = st.data_editor(
        display_df,
        disabled=["ID", "PatientID", "DoctorID", "Patient", "Doctor"],
        column_config={
            "PatientID": None,
            "DoctorID": None
        },
        num_rows="fixed",
        hide_index=True,
        use_container_width=True,
        height=min(250, 38 + 35 * (len(display_df) + 1)),
        key=f"editor_{selected}"
    )

    col_save, col_delete = st.columns(2, gap="small")

    with col_save:
        if st.button("💾 Save Changes", type="primary", use_container_width=True):
            try:
                save_data(
                    database,
                    table,
                    fields,
                    edited_df.drop(
                        columns=["Select", "Patient", "Doctor"],
                        errors="ignore"
                    ),
                    selected
                )
                st.success("Changes saved!")
                st.rerun()
            except Exception as e:
                st.error(f"Could not save: {e}")

    with col_delete:
        if st.button("🗑️ Delete Selected", use_container_width=True):
            selected_rows = edited_df[edited_df["Select"] == True]

            if selected_rows.empty:
                st.warning("Please select at least one record.")
            else:
                try:
                    for record_id in selected_rows["ID"]:
                        delete_record(database, table, record_id)

                    st.success("Selected record(s) deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not delete record: {e}")

    st.divider()
    st.markdown("#### ➕ Add New Record")


    with st.form(f"add_{selected}"):
        values = []

        for column, kind in fields.items():
            if selected == "Appointments" and column == "PatientID":
                patients_df = read_data("PatientsDB", "Patients")
                patient_options = dict(
                    zip(patients_df["Name"], patients_df["ID"])
                )

                if patient_options:
                    patient_names = list(patient_options.keys())
                    selected_patient = st.selectbox(
                        "Patient",
                        patient_names
                    )
                    value = patient_options[selected_patient]
                else:
                    value = st.number_input(
                        "PatientID", min_value=1, step=1
                    )

            elif selected == "Appointments" and column == "DoctorID":
                doctors_df = read_data("DoctorsDB", "Doctors")
                doctor_options = dict(
                    zip(doctors_df["Name"], doctors_df["ID"])
                )

                if doctor_options:
                    doctor_names = list(doctor_options.keys())
                    selected_doctor = st.selectbox(
                        "Doctor",
                        doctor_names
                    )
                    value = doctor_options[selected_doctor]
                else:
                    value = st.number_input(
                        "DoctorID", min_value=1, step=1
                    )

            elif kind == "int":
                min_value = (
                    1 if selected == "Patients" and column == "Age"
                    else 0
                )
                value = st.number_input(
                    column,
                    min_value=min_value,
                    value=min_value,
                    step=1
                )

            elif kind == "float":
                value = st.number_input(
                    column,
                    min_value=0.0,
                    value=0.0
                )

            elif selected == "Patients" and column == "Gender":
                value = st.selectbox(
                    column,
                    ["Female", "Male", "Other"]
                )

            elif selected == "Appointments" and column == "Status":
                value = st.selectbox(
                    column,
                    ["Scheduled", "Completed", "Cancelled"]
                )

            else:
                value = st.text_input(column)

            values.append(value)

        submitted = st.form_submit_button("Add Record")

        if submitted:
            if any(
                isinstance(v, str) and not v.strip()
                for v in values
            ):
                st.error("Please fill in all text fields.")
            else:
                try:
                    add_record(database, table, fields, values)
                    st.success("Record added successfully!")
                    st.toast("New record added!", icon="✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not add record: {e}")
except Exception as e:
    st.error(
        "Connection or database error. Check SERVER, DRIVER, "
        "and SQL Server permissions."
    )
    st.code(str(e))


