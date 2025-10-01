from flask import Flask, request, render_template
from twilio.rest import Client
import csv

app = Flask(__name__)

# 🔐 Twilio credentials (replace with your actual values)
account_sid = 'ACe4ab507579484fe24acb32e2ef42425b'
auth_token = '555cc711b4775e2fa7fc5daca4d875ce'
twilio_number = '+12316557634'

client = Client(account_sid, auth_token)

# 📖 Function to get parent phone number from CSV
def get_parent_phone(student_name):
    with open('students.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['student_name'] == student_name:
                return row['parent_phone']
    return None

# 🏠 Home page
@app.route('/')
def home():
    return render_template('index.html')

# 📩 Attendance submission
@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['student_name']
    status = request.form['status']
    parent_phone = get_parent_phone(student_name)

    if status == 'Absent' and parent_phone:
        message = f"Dear Parent, your child {student_name} was absent today."
        client.messages.create(
            body=message,
            from_=twilio_number,
            to=parent_phone
        )

    return f"✅ Attendance marked for {student_name} as {status}."

# 🚀 Run the app
if __name__ == '__main__':
    app.run(debug=True)