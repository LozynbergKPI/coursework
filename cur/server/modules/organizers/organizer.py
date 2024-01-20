import email
import imaplib
from cur.server.modules.decorators.decorator import track_execution_time
from cur.server.modules.emailClients.email_client import EmailClient


class MailManager(EmailClient):
    """
    A class representing a mail manager for reading, classifying, and moving emails.

    Inherits from EmailClient.

    Methods:
    - connect_to_server(self): Connects to the IMAP server for reading emails.
    - read_emails(self): Reads and displays emails from the inbox.
    - classify_and_move_emails(self): Classifies and moves emails to specific folders.
    - create_folder_if_not_exists(self, server, folder_name): Creates a folder on the server if it doesn't exist.
    """
    @track_execution_time
    def connect_to_server(self):
        """
        Connects to the IMAP server for reading emails.
        """
        try:
            print("Підключення до IMAP серверу...")

            with imaplib.IMAP4_SSL(self.provider.imap_server) as server:
                server.login(self.user_email, self.user_password)
                server.select('inbox')
        except Exception as e:
            print(f"Помилка підключення до IMAP серверу: {e}")

    def read_emails(self):
        """
        Reads and displays emails from the inbox.
        """
        print("Підключення до IMAP серверу...")

        try:

            with imaplib.IMAP4_SSL(self.provider.imap_server) as server:
                server.login(self.user_email, self.user_password)
                server.select('inbox')

                typ, messages = server.search(None, 'ALL')
                if typ != 'OK':
                    print("Не удалось найти сообщения.")
                    return

                for num in messages[0].split()[:5]:
                    typ, data = server.fetch(num, '(RFC822)')
                    if typ != 'OK':
                        continue

                    msg = email.message_from_bytes(data[0][1])
                    print(f"Письмо от: {msg['from']}")
                    print(f"Тема: {msg['subject']}")
                    print("Содержание:")
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                print(part.get_payload(decode=True).decode())
                    else:
                        print(msg.get_payload(decode=True).decode())

        except Exception as e:
            print(f"Ошибка при чтении писем: {e}")


    def classify_and_move_emails(self):
        """
        Classifies and moves emails to specific folders.
        """
        print("Класифікація та переміщення листів...")
        try:
            with imaplib.IMAP4_SSL(self.provider.imap_server) as server:
                server.login(self.user_email, self.user_password)
                server.select('inbox')
                typ, messages = server.search(None, 'ALL')

                if typ != 'OK':
                    print("No messages to classify.")
                    return

                for num in messages[0].split():
                    typ, data = server.fetch(num, '(RFC822)')
                    if typ != 'OK':
                        continue

                    msg = email.message_from_bytes(data[0][1])
                    subject = msg['subject'].lower()


                    if 'important' in subject:
                        self.create_folder_if_not_exists(server, 'Important')
                        server.copy(num.decode('utf-8'), 'Important')
                        server.store(num, '+FLAGS', '\\Deleted')
                    elif 'work' in subject:
                        self.create_folder_if_not_exists(server, 'Work')
                        server.copy(num.decode('utf-8'), 'Work')
                        server.store(num, '+FLAGS', '\\Deleted')

                server.expunge()
        except Exception as e:
            print(f"Ошибка при классификации и перемещении писем: {e}")

    def create_folder_if_not_exists(self, server, folder_name):
        """
        Creates a folder on the server if it doesn't exist.

        Args:
        - server: The IMAP server connection.
        - folder_name (str): The name of the folder to create.
        """
        print(f"Створення папки '{folder_name}', якщо вона не існує...")