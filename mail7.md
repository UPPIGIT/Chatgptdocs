Let's enhance the HTML table to ensure borders are visible. I will use inline styles to ensure compatibility across different email clients, which sometimes ignore CSS styles defined in the `<style>` section.

### Updated `EmailUtility` Class with Improved Table Borders and Inline Styles

```python
import logging
from google.cloud import bigquery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message)s')

class EmailUtility:
    def __init__(self, from_email, smtp_server='smtp.gmail.com', smtp_port=587):
        self.from_email = from_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_simple_email(self, subject, to_email, cc_email, body):
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Cc'] = cc_email
        msg['Subject'] = subject

        email_body = f"""
        <html>
        <body>
            <p>Hi Team,</p>
            <p>{body}</p>
            <p>Please don't reply to this email. It is generated by GCP Composer DAG.</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(email_body, 'html'))

        recipients = [to_email] + [cc_email]

        try:
            logging.info('Connecting to SMTP server')
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.sendmail(self.from_email, recipients, msg.as_string())
                server.quit()
            logging.info('Simple email sent successfully')
        except Exception as e:
            logging.error(f'Failed to send simple email: {e}')

    def send_bq_results_email(self, subject, to_email, cc_email, queries):
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Cc'] = cc_email
        msg['Subject'] = subject

        bigquery_util = BigQueryUtility()

        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <p>Hi Team,</p>
            <p>Please find the below details of data load.</p>
        """

        for title, sql in queries.items():
            try:
                results = bigquery_util.execute_query(sql)
                html_content += bigquery_util.format_results_to_html_table(results, title)
            except Exception as e:
                logging.error(f'Error executing query for {title}: {e}')
                html_content += f'<p>Error executing query for {title}: {e}</p>'
        
        html_content += """
            <p>Please don't reply to this email. It is generated by GCP Composer DAG.</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        recipients = [to_email] + [cc_email]

        try:
            logging.info('Connecting to SMTP server')
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.sendmail(self.from_email, recipients, msg.as_string())
                server.quit()
            logging.info('Email with BigQuery results sent successfully')
        except Exception as e:
            logging.error(f'Failed to send email with BigQuery results: {e}')

class BigQueryUtility:
    def __init__(self):
        self.client = bigquery.Client()

    def execute_query(self, sql):
        logging.info(f'Executing BigQuery SQL: {sql}')
        query_job = self.client.query(sql)
        results = query_job.result()
        logging.info('Query executed successfully')
        return results

    def format_results_to_html_table(self, results, title):
        logging.info(f'Formatting results for table: {title}')
        html = f'<h2 style="color: #4CAF50;">{title}</h2>'
        html += '<table style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border: 1px solid #ddd;">'
        html += '<tr style="background-color: #4CAF50; color: white;">'

        # Table headers
        for field in results.schema:
            html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{field.name}</th>'
        html += '</tr>'

        # Table rows
        for row in results:
            html += '<tr>'
            for field in results.schema:
                html += f'<td style="border: 1px solid #ddd; padding: 8px;">{row[field.name]}</td>'
            html += '</tr>'
        
        html += '</table><br>'
        logging.info(f'Table {title} formatted successfully')
        return html

# Usage example
if __name__ == "__main__":
    email_util = EmailUtility("your_email@gmail.com")

    # Example 1: Sending a simple email
    email_util.send_simple_email(
        subject="Simple Email Subject",
        to_email="recipient@example.com",
        cc_email="cc_recipient@example.com",
        body="This is a simple email body with more detailed information."
    )

    # Example 2: Sending an email with BigQuery results
    queries = {
        "Table1": "SELECT * FROM `your_project.your_dataset.your_table1` LIMIT 10",
        "Table2": "SELECT * FROM `your_project.your_dataset.your_table2` LIMIT 10",
    }

    email_util.send_bq_results_email(
        subject="BigQuery Results",
        to_email="recipient@example.com",
        cc_email="cc_recipient@example.com",
        queries=queries
    )
```

### Explanation of Changes:
1. **Inline Styles for Borders**: Each table, `th`, and `td` element now has inline styles to ensure borders are visible across all email clients.
2. **Table Header Styling**: The header row now has a background color to distinguish it from the rest of the table.
3. **Row Alternation**: Removed alternating row colors for simplicity, but added clear border styling to enhance visibility.

These changes should ensure that the tables in your email have clearly visible borders and look good in most email clients.
