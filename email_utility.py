import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - '%(message)s')

class EmailUtility:
    def __init__(self, oauth2_url, client_id, client_secret, scope):
        self.oauth2_url = oauth2_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

    def get_oauth2_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope,
        }
        response = requests.post(self.oauth2_url, data=payload)
        response.raise_for_status()
        logging.info('OAuth2 token obtained successfully')
        return response.json()['access_token']

    def send_email_via_api(self, subject, to_email, cc_email, email_content):
        token = self.get_oauth2_token()
        api_url = 'https://dummyapi.example.com/emailnotification'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        data = {
            "from": "noreply@example.com",
            "htmlBody": email_content,
            "subject": subject,
            "to": to_email,
            "cc": cc_email
        }
        response = requests.post(api_url, headers=headers, json=data)

        # Log status code and headers
        status_code = response.status_code
        response_headers = response.headers
        logging.info(f'Status Code: {status_code}')
        logging.info(f'Headers: {response_headers}')

        if response.status_code // 100 != 2:
            logging.error(f'Failed to send email via API: {response.text}')
            response.raise_for_status()
        logging.info('Email sent successfully via API')
