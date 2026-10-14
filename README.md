# Hospital Information System

A simple Hospital Information System developed using Python, Streamlit, and Microsoft SQL Server.

## Features

- Manage patients, doctors, appointments, and prescriptions.
- Connect to multiple SQL Server databases.
- View and search records.
- Add new records.
- Edit existing records.
- Delete selected records.
- Display patient and doctor names for appointments.

## Technologies

- Python
- Streamlit
- Pandas
- PyODBC
- Microsoft SQL Server

## Requirements

- Python
- Microsoft SQL Server
- ODBC Driver 18 for SQL Server

## How to Run

1. Clone or download this repository.
2. Install the required Python packages:

   `pip install -r requirements.txt`

3. Make sure SQL Server is running and the required databases and tables exist.
4. Check the server name and database connection settings in `app.py`.
5. Run the application:

   `python -m streamlit run app.py`

## Databases

The application uses four databases:

- PatientsDB
- DoctorsDB
- AppointmentsDB
- PrescriptionsDB

## Demo Video

Watch the video to see how the Hospital Information System works.
https://lut-my.sharepoint.com/:v:/g/personal/behnaz_alavinezhad_student_lut_fi/IQABJTT6Lo3YTqXBB39EpNNLAaG4wl8sPqsMf1CXaQvimfU?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=Y4IYZc

**Note:** The SQL Server databases must be created and configured separately before running the application.
