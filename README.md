# AI Packet Detector

## Overview

AI Packet Detector is a **real-time network monitoring tool** that detects anomalous network packets using **machine learning**. It includes:

- **Automated anomaly detection** using a trained RandomForest model.
- **Web dashboard** for viewing alerts and managing email notifications.
- **Exporting and emailing** logs periodically for network security monitoring.
- **Customizable recipient management** with a log of email updates.

## Features

- **Real-time packet monitoring** using Scapy.
- **Machine learning-based anomaly detection**.
- **Web dashboard** to view alerts and configure settings.
- **Email alerts for suspicious activity**.
- **Automatic export of alerts to JSON/CSV**.
- **User-configurable email recipients**.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Required dependencies (install with the command below):
  ```sh
  pip install -r requirements.txt
  ```

### Running the Application

1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/AIPacketDetector.git
   cd AIPacketDetector
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the application:
   ```sh
   python ai_packet_detector.py
   ```
4. Open the web dashboard at `http://localhost:5000`.

## Usage

### Web Dashboard

- View **live alerts** of detected anomalies.
- **Enable/disable email notifications**.
- **Add or update email recipients**.
- **View and clear recipient change logs**.

### Automatic Exports

- Logs are exported **every 10 minutes**.
- Exported files are saved as **JSON** and **CSV**.
- If email notifications are enabled, logs are sent to recipients.

### API Endpoints

| Endpoint                      | Method | Description                 |
| ----------------------------- | ------ | --------------------------- |
| `/`                           | GET    | Access web dashboard        |
| `/toggle_email_notifications` | POST   | Toggle email notifications  |
| `/update_recipients`          | POST   | Update email recipients     |
| `/recipient_log`              | GET    | View recipient change logs  |
| `/clear_recipient_log`        | POST   | Clear recipient change logs |

## Customization

- Modify `EXPORT_INTERVAL` in `ai_packet_detector.py` to change the export frequency.
- Add additional **packet features** for model training in `detect_anomalies()`.
- Customize **email settings** in `send_email_with_attachment()`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome! Feel free to submit issues and suggest improvements.

