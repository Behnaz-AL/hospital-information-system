
-- Hospital Information System
-- Create the four databases

IF DB_ID('PatientsDB') IS NULL
    CREATE DATABASE PatientsDB;
GO

IF DB_ID('DoctorsDB') IS NULL
    CREATE DATABASE DoctorsDB;
GO

IF DB_ID('AppointmentsDB') IS NULL
    CREATE DATABASE AppointmentsDB;
GO

IF DB_ID('PrescriptionsDB') IS NULL
    CREATE DATABASE PrescriptionsDB;
GO


-- Patients table
USE PatientsDB;
GO

IF OBJECT_ID('dbo.Patients', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Patients (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(100) NOT NULL,
        Age INT NOT NULL,
        Gender NVARCHAR(20) NOT NULL,
        Phone NVARCHAR(30) NOT NULL,
        Diagnosis NVARCHAR(200) NOT NULL
    );
END;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Patients)
BEGIN
    INSERT INTO dbo.Patients (Name, Age, Gender, Phone, Diagnosis)
    VALUES
        ('Anna Smith', 32, 'Female', '0401234567', 'Flu'),
        ('John Brown', 45, 'Male', '0402345678', 'Back pain'),
        ('Sara Wilson', 28, 'Female', '0403456789', 'Migraine');
END;
GO


-- Doctors table
USE DoctorsDB;
GO

IF OBJECT_ID('dbo.Doctors', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Doctors (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(100) NOT NULL,
        Specialty NVARCHAR(100) NOT NULL,
        Phone NVARCHAR(30) NOT NULL,
        Department NVARCHAR(100) NOT NULL
    );
END;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Doctors)
BEGIN
    INSERT INTO dbo.Doctors (Name, Specialty, Phone, Department)
    VALUES
        ('Dr Emily White', 'Cardiology', '0501234567', 'Cardiology'),
        ('Dr James Green', 'Neurology', '0502345678', 'Neurology'),
        ('Dr Olivia Brown', 'General Medicine', '0503456789', 'General Medicine');
END;
GO


-- Appointments table
USE AppointmentsDB;
GO

IF OBJECT_ID('dbo.Appointments', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Appointments (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        PatientID INT NOT NULL,
        DoctorID INT NOT NULL,
        AppointmentDate NVARCHAR(50) NOT NULL,
        Reason NVARCHAR(200) NOT NULL,
        Status NVARCHAR(30) NOT NULL
    );
END;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Appointments)
BEGIN
    INSERT INTO dbo.Appointments
        (PatientID, DoctorID, AppointmentDate, Reason, Status)
    VALUES
        (1, 1, '2026-10-15 10:00', 'Regular check-up', 'Scheduled'),
        (2, 2, '2026-10-16 11:30', 'Headache consultation', 'Scheduled'),
        (3, 3, '2026-10-17 09:00', 'General consultation', 'Completed');
END;
GO


-- Prescriptions table
USE PrescriptionsDB;
GO

IF OBJECT_ID('dbo.Prescriptions', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Prescriptions (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        PatientID INT NOT NULL,
        MedicineName NVARCHAR(100) NOT NULL,
        Dosage NVARCHAR(100) NOT NULL,
        PrescriptionDate NVARCHAR(50) NOT NULL,
        Notes NVARCHAR(300) NOT NULL
    );
END;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Prescriptions)
BEGIN
    INSERT INTO dbo.Prescriptions
        (PatientID, MedicineName, Dosage, PrescriptionDate, Notes)
    VALUES
        (1, 'Paracetamol', '500 mg', '2026-10-14', 'Take when needed'),
        (2, 'Ibuprofen', '200 mg', '2026-10-14', 'Take after food'),
        (3, 'Migraine medication', 'As prescribed', '2026-10-14', 'Follow doctor instructions');
END;
GO

PRINT 'Hospital Information System databases are ready.';
GO
