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
        # Load all rows, skipping the header row
        rows = list(sheet.iter_rows(values_only=True))
        
        # Remove the specified row, adjusting for the header row
        del rows[row + 1]
        
        # Clear the sheet
        sheet.delete_rows(2, sheet.max_row)  # Keep the first row (headers)
        
        # Write the rows back, excluding headers
        for row_data in rows[1:]:
            sheet.append(row_data)
        
        wb.save(file_path)
        
        flash('Record deleted successfully!')
        return redirect(url_for('record'))
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('record'))




@app.route('/new')
def new():
    return render_template('index.html')

@app.route('/record')
def record():
    # Read the Excel data, excluding the header row
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    data = data[1:]  # Exclude the first row (headers)
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

@app.route('/edit/<int:row>', methods=['GET', 'POST'])
def edit(row):
    if request.method == 'POST':
        try:
            # Get form data
            form_data = request.form.to_dict()
            required_fields = ['status', 'source_of_booking', 'date', 'name', 'reservation_date', 'contact', 'in', 'out', 'day', 'night', 'adult', 'children', 'student', 'videoke', 'room', 'room_number', 'cottage_no', 'pax', 'receptionist', 'downpayment', 'gcash', 'full_payment']

            # Update the Excel sheet with the new data
            for col_num, field in enumerate(required_fields, start=1):
                sheet.cell(row=row + 1, column=col_num, value=form_data.get(field))

            wb.save(file_path)

            flash('Data updated successfully!')
            return redirect(url_for('record'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('edit', row=row))
    else:
        # Load the existing data for the row to be edited
        existing_data = [cell.value for cell in sheet[row + 1]]
        return render_template('edit.html', row=row, data=existing_data)

if __name__ == '__main__':
    app.run(debug=True)
