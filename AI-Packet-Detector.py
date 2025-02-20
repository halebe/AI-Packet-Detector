import scapy.all as scapy
import pandas as pd
import numpy as np
import joblib
import time
import smtplib
import csv
import json
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, jsonify, request, send_file
from scapy.layers.inet import IP, TCP, UDP
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
alerts = []
attack_counts = []
recipient_change_log = []
EXPORT_INTERVAL = 600  # Export every 10 minutes
EMAIL_NOTIFICATIONS = True  # Toggle for email notifications
EMAIL_RECIPIENTS = ["admin@example.com"]  # List of recipients

# Load or train model
MODEL_PATH = "packet_anomaly_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("No trained model found. Training a new one...")
    # Sample training data (should be replaced with actual network traffic data)
    data = pd.DataFrame({
        "packet_size": np.random.randint(50, 1500, 1000),
        "src_port": np.random.randint(1024, 65535, 1000),
        "dst_port": np.random.randint(1024, 65535, 1000),
        "protocol": np.random.choice([6, 17], 1000),  # TCP (6) or UDP (17)
        "is_anomaly": np.random.choice([0, 1], 1000, p=[0.95, 0.05])  # 5% anomalies
    })
    
    X = data.drop(columns=["is_anomaly"])
    y = data["is_anomaly"]
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, MODEL_PATH)
    print("New model trained and saved!")

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Network Monitoring Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script>
            async function toggleEmailNotifications() {
                const response = await fetch('/toggle_email_notifications', { method: 'POST' });
                const data = await response.json();
                document.getElementById('emailStatus').innerText = `Email Notifications: ${data.email_notifications ? 'Enabled' : 'Disabled'}`;
            }
            async function updateRecipients() {
                const recipients = document.getElementById('emailRecipients').value.split(',');
                await fetch('/update_recipients', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ recipients })
                });
                alert("Email recipients updated successfully!");
                fetchRecipientLog();
            }
            async function fetchRecipientLog() {
                const response = await fetch('/recipient_log');
                const data = await response.json();
                document.getElementById('recipientLog').innerHTML = data.map(log => `<li class="list-group-item">${log}</li>`).join('');
            }
            async function clearRecipientLog() {
                await fetch('/clear_recipient_log', { method: 'POST' });
                fetchRecipientLog();
            }
            window.onload = fetchRecipientLog;
        </script>
    </head>
    <body class="container mt-4">
        <h1 class="text-center">Network Monitoring Dashboard</h1>
        <p id="emailStatus">Email Notifications: Enabled</p>
        <button class="btn btn-primary" onclick="toggleEmailNotifications()">Toggle Email Notifications</button>
        <br><br>
        <label for="emailRecipients">Update Recipients:</label>
        <input type="text" id="emailRecipients" class="form-control" placeholder="Enter emails, separated by commas">
        <button class="btn btn-secondary mt-2" onclick="updateRecipients()">Update Recipients</button>
        <h3 class="mt-4">Recipient Change Log</h3>
        <ul id="recipientLog" class="list-group"></ul>
        <button class="btn btn-danger mt-2" onclick="clearRecipientLog()">Clear Log</button>
    </body>
    </html>
    '''

@app.route('/toggle_email_notifications', methods=['POST'])
def toggle_email_notifications():
    global EMAIL_NOTIFICATIONS
    EMAIL_NOTIFICATIONS = not EMAIL_NOTIFICATIONS
    return jsonify({"email_notifications": EMAIL_NOTIFICATIONS})

@app.route('/update_recipients', methods=['POST'])
def update_recipients():
    global EMAIL_RECIPIENTS, recipient_change_log
    data = request.json
    if "recipients" in data:
        EMAIL_RECIPIENTS = data["recipients"]
        recipient_change_log.append(f"{time.ctime()}: Recipients updated to {', '.join(EMAIL_RECIPIENTS)}")
    return jsonify({"recipients": EMAIL_RECIPIENTS})

@app.route('/recipient_log')
def recipient_log():
    return jsonify(recipient_change_log)

@app.route('/clear_recipient_log', methods=['POST'])
def clear_recipient_log():
    global recipient_change_log
    recipient_change_log = []
    return jsonify({"message": "Recipient log cleared"})

print("Starting real-time network monitoring...")
threading.Thread(target=export_logs, daemon=True).start()
scapy.sniff(prn=detect_anomalies, store=False)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
