from flask import Flask, render_template, request, redirect, url_for, flash
import openpyxl
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Load the Excel file
file_path = os.path.join(os.path.dirname(__file__), 'ManaloK9-Tracker.xlsx')
try:
    wb = openpyxl.load_workbook(file_path)
    sheet = wb['Sheet1']
except Exception as e:
    print(f"Error loading Excel file: {e}")
@app.route('/new')
def new():
    return render_template('index.html')

@app.route('/record')
def record():
    # Read the Excel data
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    return render_template('record.html', data=data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        form_data = request.form.to_dict()
        required_fields = ['status', 'source_of_booking', 'date', 'name', 'reservation_date', 'contact', 'in', 'out', 'day', 'night', 'adult', 'children', 'student', 'videoke', 'room', 'room_number', 'cottage_no', 'pax', 'receptionist', 'downpayment', 'gcash', 'full_payment']

        # Check if all required fields are filled
        if not all([form_data.get(field) for field in required_fields]):
            flash('Please fill in all fields')
            return render_template('index.html', form_data=form_data)

        # Find the first empty row in the sheet
        next_row = sheet.max_row + 1

        # Append data to the next empty row
        for col_num, field in enumerate(required_fields, start=1):
            sheet.cell(row=next_row, column=col_num, value=form_data.get(field))

        wb.save(file_path)

        print("Data saved successfully!")

        flash('Data saved successfully!')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An error occurred: {e}")
        print(f"Error submitting data: {e}")
        return render_template('index.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
