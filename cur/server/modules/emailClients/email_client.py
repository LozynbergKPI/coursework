import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from cur.server.modules.decorators.decorator import track_execution_time
from cur.server.modules.templates.template import MailTemplate


class EmailClient(MailTemplate):
    """
    A class representing an email client for sending and managing emails.

    Attributes:
    - user_email (str): The user's email address.
    - user_password (str): The user's email account password.
    - provider (MailServiceProvider): The email service provider configuration.
    - message (MIMEMultipart): The email message to be sent.

    Methods:
    - connect_to_server(self): Connects to the SMTP server for sending emails.
    - prepare_and_send_message(self, recipient, subject, body, attachments=None): Prepares and sends an email message.
    - prepare_message(self, recipient, subject, body, attachments=None): Prepares an email message without sending it.
    - send_message(self): Sends a prepared email message.
    - disconnect_from_server(self): Disconnects from the SMTP server.
    - save_draft(self, recipient, subject, body, attachments=None): Saves an email draft locally.
    - send_email_with_attachments(self, recipient, subject, body, attachments=None): Sends an email with attachments.
    """

    @track_execution_time
    def connect_to_server(self):
        """
        Connects to the SMTP server for sending emails.
        """
        try:
            print("Підключення до SMTP серверу...")

            with smtplib.SMTP(self.provider.smtp_server, self.provider.smtp_port) as server:
                server.starttls()
                server.login(self.user_email, self.user_password)

        except Exception as e:
            print(f"Помилка підключення до SMTP серверу: {e}")



    def prepare_and_send_message(self, recipient, subject, body, attachments=None):
        """
        Prepares and sends an email message.

        Args:
        - recipient (str): The recipient's email address.
        - subject (str): The subject of the email.
        - body (str): The body text of the email.
        - attachments (list of str, optional): List of file paths for email attachments.
        """
        print("Підготовка та відправка повідомлення...")

        self.prepare_message(recipient, subject, body, attachments)
        self.send_message()

    def prepare_message(self, recipient, subject, body, attachments=None):
        """
        Prepares an email message without sending it.

        Args:
        - recipient (str): The recipient's email address.
        - subject (str): The subject of the email.
        - body (str): The body text of the email.
        - attachments (list of str, optional): List of file paths for email attachments.
        """
        print("Підготовка повідомлення...")

        self.message = MIMEMultipart()
        self.message['From'] = self.user_email
        self.message['To'] = recipient
        self.message['Subject'] = subject
        self.message.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                part = MIMEBase('application', "octet-stream")
                with open(file_path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                self.message.attach(part)

    def send_message(self):
        """
        Sends a prepared email message.
        """
        print("Відправлення повідомлення...")

        try:
            with smtplib.SMTP(self.provider.smtp_server, self.provider.smtp_port) as server:
                server.starttls()
                server.login(self.user_email, self.user_password)
                server.sendmail(self.user_email, [self.message['To']], self.message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")


    def disconnect_from_server(self):
        """
        Disconnects from the SMTP server.
        """
        print("Відключення від SMTP сервера...")

    def save_draft(self, recipient, subject, body, attachments=None):
        """
        Saves an email draft locally.

        Args:
        - recipient (str): The recipient's email address.
        - subject (str): The subject of the email draft.
        - body (str): The body text of the email draft.
        - attachments (list of str, optional): List of file paths for email draft attachments.
        """
        print("Збереження чернетки...")

        msg = MIMEMultipart()
        msg['From'] = self.user_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                part = MIMEBase('application', "octet-stream")
                with open(file_path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)

        with open(f"{subject}_draft.eml", "w") as draft_file:
            draft_file.write(msg.as_string())
        print("Draft saved successfully.")


    def send_email_with_attachments(self, recipient, subject, body, attachments=None):
        """
        Sends an email with attachments.

        Args:
        - recipient (str): The recipient's email address.
        - subject (str): The subject of the email.
        - body (str): The body text of the email.
        - attachments (list of str, optional): List of file paths for email attachments.
        """
        print("Відправлення листа з додатками...")

        msg = MIMEMultipart()
        msg['From'] = self.user_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                part = MIMEBase('application', "octet-stream")
                with open(file_path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)

        try:
            with smtplib.SMTP(self.provider.smtp_server, self.provider.smtp_port) as server:
                server.starttls()
                server.login(self.user_email, self.user_password)
                server.sendmail(self.user_email, [recipient], msg.as_string())
            print("Email with attachments sent successfully!")
        except Exception as e:
            print(f"Error sending email with attachments: {e}")