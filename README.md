---

# RFID-Based Attendance System

## Overview
The **RFID-Based Attendance System** is a comprehensive attendance management solution that leverages RFID technology to enable secure and efficient attendance tracking. This system includes three primary modules — Admin, Teacher, and Student — each with unique privileges and functionalities tailored to their role.

---

## Modules

### 1. Admin Module
The **Admin Module** provides advanced privileges to manage the entire system, including user approvals, class, subject, and department setup, and full attendance visibility.

**Admin Features:**
- View, Approve, or Remove user requests.
- Manage classes, subjects, departments, and courses:
  - Add, remove, or edit classes.
  - Add, remove, or edit subjects.
  - Add, remove, or edit departments.
  - Add, remove, or edit courses.
- Assign teachers to classes.
- View/edit all user information in the system.
- View attendance records for every class.

### 2. Teacher Module
The **Teacher Module** allows instructors to mark and manage attendance records, update student information, and configure schedules and subjects.

**Teacher Features:**
- Register or login to the system.
- Mark and view attendance.
- Update student information.
- Assign subjects to teachers.
- Set up semester subjects.
- Set/Edit timetable.
- Approve student registration requests.

### 3. Student Module
The **Student Module** provides a straightforward interface for students to manage their profiles and view or mark their attendance using RFID.

**Student Features:**
- Register and login to the system.
- Edit or view profile information.
- View attendance.
- Mark attendance via RFID.

---

## System Requirements

- Hardware: RFID Reader, RFID Tags, Computer with compatible software.
- Software: Python, Django, DRF, ArduinoIDE.
- Internet Browser: Chrome, Firefox, or any other modern web browser.

---

## Installation Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/rfid-attendance-system.git
   cd rfid-attendance-system
   ```

2. **Install dependencies:**
   - Follow the software dependency installation guides or use:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure Database:**
   - Set up your MySQL (or preferred database) and update the database settings in the configuration file (`settings.py` or equivalent).

4. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**
   - Open your web browser and go to `http://localhost:8000`.

---

## Screenshots

   - **Admin Module**: 

   - **Teacher Module**: 

   - **Student Module**: 


---

## Usage Guide

1. **Admin Login**:
   - Admin can log in using their credentials to manage the system. 
   - Manage users and all their data
   
2. **Teacher Login**:
   - Teachers can register, log in, and use the dashboard to mark attendance and manage classes.

3. **Student Login**:
   - Students can register, log in, view attendance records, and mark their attendance using RFID.

---

## Contributing
Feel free to fork the repository, submit issues, and make pull requests to enhance the functionality of this RFID-based attendance system.
---