from flask import Flask, request, jsonify, render_template
import openpyxl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is in the "templates" folder

@app.route('/submit', methods=['POST'])
def submit_form():
    form_data = request.form
    data_to_save = [
        form_data.get('status'),
        form_data.get('date'),
        form_data.get('name'),
        form_data.get('contact'),
        form_data.get('reservationDate'),
        form_data.get('in'),
        form_data.get('out'),
        form_data.get('day'),
        form_data.get('night'),
        form_data.get('receptionist'),
        form_data.get('adult'),
        form_data.get('children'),
        form_data.get('student'),
        form_data.get('videoke'),
        form_data.get('room'),
        form_data.get('roomNumber'),
        form_data.get('cottage'),
        form_data.get('noPax'),
        form_data.get('downpayment'),
        form_data.get('gcash'),
        form_data.get('fullPayment'),
        form_data.get('total')
    ]

    # Save to Excel
    file_name = "ManaloK9-Tracker.xlsx"
    try:
        workbook = openpyxl.load_workbook(file_name)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()

    sheet = workbook.active

    if sheet.max_row == 1:  # Add headers if the sheet is empty
        headers = [
            "Status", "Date", "Name", "Contact", "Reservation Date",
            "Check-In", "Check-Out", "Day", "Night", "Receptionist",
            "Adult", "Children", "Student", "Videoke", "Room",
            "Room #", "Cottage", "No. Pax", "Downpayment", "GCash (Reference#)",
            "Full Payment", "Total"
        ]
        sheet.append(headers)

    sheet.append(data_to_save)
    workbook.save(file_name)

    return jsonify({"message": "Data saved successfully!", "data": get_excel_data(file_name)})

def get_excel_data(file_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(row)

    return data

if __name__ == "__main__":
    app.run(debug=True)
