from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, Flask, session
from flask_login import login_required, current_user, LoginManager, UserMixin, login_user, logout_user
import sqlite3
import csv
from fpdf import FPDF
from datetime import datetime
from config import DB_PATH, SECRET_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, ADMIN_PHONE_NUMBER
import os
import bcrypt
import pytz
from twilio.rest import Client  # For sending SMS alerts

routes = Blueprint('routes', __name__)

@routes.route('/dashboard')
@login_required
def dashboard():
    role_redirects = {
        "Admin": "routes.admin_dashboard",
        "Doctor": "routes.doctor_dashboard",
        "Nurse": "routes.nurse_dashboard",
        "Guest": "routes.guest_dashboard"
    }
    return redirect(url_for(role_redirects.get(current_user.role, 'routes.dashboard')))

@routes.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@routes.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@routes.route('/nurse_dashboard')
@login_required
def nurse_dashboard():
    return render_template('nurse_dashboard.html')

@routes.route('/guest_dashboard')
@login_required
def guest_dashboard():
    return render_template('guest_dashboard.html')

@routes.route('/update_stock', methods=['GET', 'POST'])
@login_required
def update_stock():
    # Fetch the medicines from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")  # Adjust based on your actual table schema
    medicines = cursor.fetchall()
    conn.close()
    
    # Pass the medicines data to the template
    return render_template('update_stock.html', medicines=medicines)


@routes.route('/view_stock')
@login_required
def view_stock():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    conn.close()
    return render_template('view_stock.html', medicines=medicines)

@routes.route('/view_vitals')
@login_required
def view_vitals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vitals ORDER BY date DESC")
    vitals_data = cursor.fetchall()
    conn.close()
    return render_template('view_vitals.html', vitals_data=vitals_data)

@routes.route('/add_checklist', methods=['GET', 'POST'])
@login_required
def add_checklist():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        bathing = 'Yes' if 'bathing' in request.form else 'No'
        position_change = 'Yes' if 'position_change' in request.form else 'No'
        feeding = 'Yes' if 'feeding' in request.form else 'No'
        medication_given = 'Yes' if 'medication_given' in request.form else 'No'
        dressing_change = 'Yes' if 'dressing_change' in request.form else 'No'
        restrainer_tied = 'Yes' if 'restrainer_tied' in request.form else 'No'
        restrainer_removed = 'Yes' if 'restrainer_removed' in request.form else 'No'
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM patient_names")
        patient_names = [row[0] for row in cursor.fetchall()]  # Fetch names as a list
        cursor.execute("INSERT INTO patient_checklist (patient_name, bathing, position_change, feeding, medication_given, dressing_change, restrainer_tied, restrainer_removed, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (patient_name, bathing, position_change, feeding, medication_given, dressing_change, restrainer_tied, restrainer_removed, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        flash("✅ Checklist recorded!", "success")
        return redirect(url_for('routes.add_checklist'))
    return render_template('add_checklist.html')

@routes.route('/view_intake_output')
@login_required
def view_intake_output():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ Fetch all intake/output records
    cursor.execute("SELECT * FROM intake_output ORDER BY date DESC")
    intake_output_data = cursor.fetchall()  # Fetch all data as a list

    conn.close()
    return render_template('view_intake_output.html', intake_output_data=intake_output_data)


@routes.route('/add_intake_output', methods=['GET', 'POST'])
@login_required
def add_intake_output():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ✅ Fetch patient names for dropdown
    cursor.execute("SELECT name FROM patient_names")
    patient_names = [row[0] for row in cursor.fetchall()]
    
    conn.close()

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        water_intake = request.form.get('water_intake', 0)
        urine_output = request.form.get('urine_output', 0)
        diaper_change = 'Yes' if 'diaper_change' in request.form else 'No'

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO intake_output (patient_name, water_intake, urine_output, diaper_change, date) VALUES (?, ?, ?, ?, ?)", 
                       (patient_name, water_intake, urine_output, diaper_change, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        flash(f"✅ Intake & Output recorded for {patient_name}.", "success")
        return redirect(url_for('routes.add_intake_output'))

    return render_template('add_intake_output.html', patient_names=patient_names)


@routes.route('/view_checklist')
@login_required
def view_checklist():
    return render_template('view_checklist.html')

@routes.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    return render_template('add_note.html')

@routes.route('/view_notes')
@login_required
def view_notes():
    return render_template('view_notes.html')

@routes.route('/add_medicine', methods=['GET', 'POST'])
@login_required
def add_medicine():
    return render_template('add_medicine.html')

@routes.route('/administer_medicine', methods=['GET', 'POST'])
@login_required
def administer_medicine():
    return render_template('administer_medicine.html')

@routes.route('/add_vitals', methods=['GET', 'POST'])
@login_required
def add_vitals():
    return render_template('add_vitals.html')

@routes.route('/edit_patient_names', methods=['GET', 'POST'])
@login_required
def edit_patient_names():
    return render_template('edit_patient_names.html')

@routes.route('/export_vitals_csv')
@login_required
def export_vitals_csv():
    return send_file("vitals_export.csv", as_attachment=True, mimetype="text/csv")

@routes.route('/export_vitals_pdf')
@login_required
def export_vitals_pdf():
    return send_file("checklist_vitals.pdf", as_attachment=True, mimetype="application/pdf")

@routes.route('/export_checklist_csv')
@login_required
def export_checklist_csv():
    return send_file("checklist_export.csv", as_attachment=True, mimetype="text/csv")

@routes.route('/export_checklist_pdf')
@login_required
def export_checklist_pdf():
    return send_file("checklist_export.pdf", as_attachment=True, mimetype="application/pdf")

@routes.route('/export_intake_output_csv')
@login_required
def export_intake_output_csv():
    return send_file("intake_output_export.csv", as_attachment=True, mimetype="text/csv")

@routes.route('/export_intake_output_pdf')
@login_required
def export_intake_output_pdf():
    return send_file("intake_output_export.pdf", as_attachment=True, mimetype="application/pdf")

@routes.route('/export_stock_csv')
@login_required
def export_stock_csv():
    return send_file("stock_export.csv", as_attachment=True, mimetype="text/csv")

@routes.route('/export_stock_pdf')
@login_required
def export_stock_pdf():
    return send_file("stock_export.pdf", as_attachment=True, mimetype="application/pdf")

@routes.route('/export_notes_csv')
@login_required
def export_notes_csv():
    return send_file("notes_export.csv", as_attachment=True, mimetype="text/csv")

@routes.route('/export_notes_pdf')
@login_required
def export_notes_pdf():
    return send_file("notes_export.pdf", as_attachment=True, mimetype="application/pdf")
