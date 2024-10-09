from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  

load_dotenv()

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] =os.getenv('EMAIL_USER')   
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('RECEIVER_EMAIL') 

mail = Mail(app)

@app.route('/api/sendMessage', methods=['POST'])
def send_message():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    msg = Message(subject, recipients=[app.config['MAIL_DEFAULT_SENDER']])
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    
    try:
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        print("Error sending email:", str(e))  # Log the error on the server
        return jsonify({"error": "Failed to send email", "details": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
