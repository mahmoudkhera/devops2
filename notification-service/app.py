import os
import smtplib
import logging
from email.message import EmailMessage
from flask import Flask, request, jsonify

# --- Config from environment ---
PORT = int(os.environ.get('PORT', 3002))
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_FROM = os.environ.get('SMTP_FROM', SMTP_USER)

# Validate required secrets at startup
if not SMTP_USER or not SMTP_PASSWORD:
    raise SystemExit('❌ SMTP_USER and SMTP_PASSWORD env vars are required')

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger(__name__)


def send_email(to, subject, message):
    """Send an email via SMTP."""
    msg = EmailMessage()
    msg['From'] = SMTP_FROM
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(message)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    log.info(f'📧 Email sent → {to}: {subject}')


@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json() or {}
    to = data.get('to')
    subject = data.get('subject', 'Notification')
    message = data.get('message', '')

    if not to:
        return jsonify({'sent': False, 'error': '"to" field required'}), 400

    try:
        send_email(to, subject, message)
        return jsonify({'sent': True})
    except Exception as err:
        log.error(f'Email failed: {err}')
        return jsonify({'sent': False, 'error': str(err)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'notification', 'runtime': 'python'})


if __name__ == '__main__':
    log.info(f'📮 SMTP: {SMTP_HOST}:{SMTP_PORT} as {SMTP_USER}')
    log.info(f'🐍 Notification service (Flask) on :{PORT}')
    app.run(host='0.0.0.0', port=PORT)