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

@app.route('/delete/<int:row>', methods=['POST'])
def delete(row):
    try:
        sheet.delete_rows(row + 2)  # Adjust for header row
        wb.save(file_path)
        flash('Record deleted successfully!', 'success')
        return redirect(url_for('record'))
    except Exception as e:
        flash(f"An error occurred: {e}", 'error')
        return redirect(url_for('record'))

@app.route('/new')
def new():
    return render_template('index.html')

@app.route('/record')
def record():
    data = [row for row in sheet.iter_rows(values_only=True)][1:]  # Exclude headers
    return render_template('record.html', data=data)

@app.route('/')
def index():
    return render_template('index.html')

def validate_data(form_data):
    try:
        int(form_data['contact'])
        int(form_data['day'])
        int(form_data['night'])
        int(form_data['adult'])
        int(form_data['children'])
        int(form_data['student'])
        int(form_data['pax'])
        float(form_data['downpayment'])
        float(form_data['full_payment'])
    except ValueError:
        return False
    return True

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = request.form.to_dict()
        if not validate_data(form_data):
            flash('Please ensure all numerical fields are valid numbers.', 'error')
            return render_template('index.html', form_data=form_data)

        required_fields = ['status', 'source_of_booking', 'date', 'name', 'reservation_date', 'contact', 
                           'in', 'out', 'day', 'night', 'adult', 'children', 'student', 'videoke', 
                           'room', 'room_number', 'cottage_no', 'pax', 'receptionist', 'downpayment', 
                           'gcash', 'full_payment']

        if not all([form_data.get(field) for field in required_fields]):
            flash('Please fill in all fields.', 'error')
            return render_template('index.html', form_data=form_data)

        next_row = sheet.max_row + 1
        for col_num, field in enumerate(required_fields, start=1):
            sheet.cell(row=next_row, column=col_num, value=form_data.get(field))

        wb.save(file_path)
        flash('Data saved successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An error occurred: {e}", 'error')
        return render_template('index.html', form_data=form_data)

@app.route('/edit/<int:row>', methods=['GET', 'POST'])
def edit(row):
    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            required_fields = ['status', 'source_of_booking', 'date', 'name', 'reservation_date', 'contact', 
                               'in', 'out', 'day', 'night', 'adult', 'children', 'student', 'videoke', 
                               'room', 'room_number', 'cottage_no', 'pax', 'receptionist', 'downpayment', 
                               'gcash', 'full_payment']

            for col_num, field in enumerate(required_fields, start=1):
                sheet.cell(row=row + 1, column=col_num, value=form_data.get(field))

            wb.save(file_path)
            flash('Data updated successfully!', 'success')
            return redirect(url_for('record'))
        except Exception as e:
            flash(f"An error occurred: {e}", 'error')
            return redirect(url_for('edit', row=row))
    else:
        data = [cell.value for cell in sheet[row + 2]]
        fields = ['status', 'source_of_booking', 'date', 'name', 'reservation_date', 'contact', 
                  'in', 'out', 'day', 'night', 'adult', 'children', 'student', 'videoke', 'room', 
                  'room_number', 'cottage_no', 'pax', 'receptionist', 'downpayment', 'gcash', 'full_payment']
        existing_data = {fields[i]: data[i] for i in range(len(fields))}
        return render_template('edit.html', row=row, data=existing_data)

if __name__ == '__main__':
    app.run(debug=True)
