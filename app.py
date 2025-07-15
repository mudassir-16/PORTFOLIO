from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Apna email aur app password yahan daalein
EMAIL_ADDRESS = "mohammadmudassir1604@gmail.com"
EMAIL_PASSWORD = "erpz bdxn zxzh phue"

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Email ka content
    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    # Email setup
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
        print("Email send error:", e)
        return jsonify({"error": "Message send nahi hua!"}), 500

if __name__ == '__main__':
    app.run(debug=True)