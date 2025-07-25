from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file (optional)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Use environment variables for sensitive data
EMAIL_ADDRESS = os.getenv("mohammadmudassir1604@gmail.com")
EMAIL_PASSWORD = os.getenv("erpz bdxn zxzh phue")

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({"error": "Missing name, email, or message"}), 400

    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        return jsonify({"message": "Message successfully sent!"}), 200
    except Exception as e:
        print("Email send error:", str(e))
        return jsonify({"error": "Failed to send message."}), 500

if __name__ == '__main__':
    app.run(debug=True)
