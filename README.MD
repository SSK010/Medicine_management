# Medicine Stock & Patient Management System

## Overview
This system is designed to manage medicine stock and patient records efficiently. It includes functionalities for:
- Medicine stock management
- Patient vitals tracking
- Intake & output recording
- Patient daily checklist
- Notes and updates
- User authentication with different roles (Admin, Doctor, Nurse, Guest)

## Installation

### Requirements
Ensure you have the following installed:
- Python 3.x
- Flask
- SQLite
- Twilio (for SMS alerts)
- bcrypt (for password hashing)

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/medicine-management.git
   cd medicine-management
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```sh
   python create_db.py
   python update_db.py
   ```

4. Run the application:
   ```sh
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Features
- **Medicine Management**: Add, view, update, and administer medicines.
- **Patient Vitals**: Record blood pressure, pulse, SpO₂, temperature, and SMBG levels.
- **Intake & Output**: Track daily fluid intake and output.
- **Checklist & Notes**: Maintain a daily routine checklist and record notes.
- **User Roles**:
  - **Admin**: Full access to all features.
  - **Doctor**: View vitals, administer medicines, add notes.
  - **Nurse**: View vitals, administer medicines, update checklist.
  - **Guest**: Read-only access.

## Configuration
- Update `config.py` with your database path and Twilio credentials.
- Modify `routes.py` and 'app.py' to set up additional routes or customize functionalities.

## License
This project is licensed under the GPL-3.0 License.

## Contact
For any issues, please create an issue in the repository or reach out to `kulkarni.shrivatsa05@gmail.com`.
