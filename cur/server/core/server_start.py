import socket
import threading
from cur.server.modules.builders.builder import MailClientBuilder, MailProcessor
from cur.server.modules.providers.provider import MailServiceProvider


class EmailServer:
    """
    A simple email server that handles client connections and email operations.

    Attributes:
    - host (str): The hostname or IP address where the server will listen for incoming connections.
    - port (int): The port number to bind the server socket to.
    - provider_name (str): The name of the email service provider.
    - user_email (str): The user's email address.
    - user_password (str): The user's email account password.
    - email_interpreter (MailProcessor): An instance of MailProcessor for handling email operations.

    Methods:
    - __init__(self, host, port, provider_name, user_email, user_password): Initializes the EmailServer instance.
    - _create_email_interpreter(self): Creates an email interpreter based on the provided provider and user credentials.
    - get_provider_config(provider_name): Returns the configuration for a given email service provider.
    - process_command(self, command): Processes incoming client commands and executes corresponding actions.
    - handle_client(self, client_socket): Handles communication with a connected client.
    - start_server(self): Starts the email server and listens for incoming connections.
    """
    def __init__(self, host, port, provider_name, user_email, user_password):
        """
        Initializes a new EmailServer instance.

        Args:
        - host (str): The hostname or IP address where the server will listen for incoming connections.
        - port (int): The port number to bind the server socket to.
        - provider_name (str): The name of the email service provider.
        - user_email (str): The user's email address.
        - user_password (str): The user's email account password.
        """
        self.host = host
        self.port = port
        self.provider_name = provider_name
        self.user_email = user_email
        self.user_password = user_password
        self.email_interpreter = self._create_email_interpreter()

    def _create_email_interpreter(self):
        """
        Creates an email interpreter based on the provided provider and user credentials.

        Returns:
        - MailProcessor: An instance of MailProcessor for handling email operations.
        """
        config = self.get_provider_config(self.provider_name)
        if config:
            client_builder = MailClientBuilder()
            organizer = (client_builder.set_provider(config)
                                       .set_user_email(self.user_email)
                                       .set_user_password(self.user_password))
            return MailProcessor(organizer.build_organizer())
        else:
            raise ValueError(f"Провайдер '{self.provider_name}' не найден.")

    @staticmethod
    def get_provider_config(provider_name):
        """
        Returns the configuration for a given email service provider.

        Args:
        - provider_name (str): The name of the email service provider.

        Returns:
        - MailServiceProvider: The configuration for the specified provider.
        """
        providers = {
            'gmail': MailServiceProvider('smtp.gmail.com', 587, 'imap.gmail.com', 'pop.gmail.com'),
            'ukr.net': MailServiceProvider('smtp.ukr.net', 465, 'imap.ukr.net', 'pop3.ukr.net'),
            'i.ua': MailServiceProvider('smtp.i.ua', 465, 'imap.i.ua', 'pop3.i.ua')
        }
        return providers.get(provider_name.lower())

    def process_command(self, command):
        """
        Processes incoming client commands and executes corresponding actions.

        Args:
        - command (str): The command received from the client.

        Returns:
        - str: The response to be sent back to the client.
        """
        if command.startswith("CONFIG"):
            try:
                _, provider_name, user_email, user_password = command.split(" ", 3)
                config = self.get_provider_config(provider_name)
                if config:
                    client_builder = MailClientBuilder()
                    organizer = (client_builder.set_provider(config)
                                           .set_user_email(user_email)
                                           .set_user_password(user_password))
                    self.email_interpreter = MailProcessor(organizer.build_organizer())
                    return "Configuration successful."
                else:
                    return f"Provider '{provider_name}' not found."
            except Exception as e:
                return f"Error in configuration: {e}"

        elif command.startswith("send email"):
            _, recipient, subject, body = command.split(" ", 3)
            self.email_interpreter.email_organizer.prepare_and_send_message(recipient, subject, body)
            return "Email sent successfully."

        elif command.startswith("classify emails"):
            self.email_interpreter.email_organizer.classify_and_move_emails()
            return "Emails classified."

        elif command.startswith("read emails"):
            self.email_interpreter.email_organizer.read_emails()
            return "Emails read."

        elif command.startswith("save draft"):
            params = command.split(" ", 3)[1:]
            if len(params) >= 3:
                recipient, subject, body = params
                self.email_interpreter.email_organizer.save_draft(recipient, subject, body)
                return "Draft saved."
            else:
                return "Insufficient parameters for 'save draft'."

        else:
            return "Invalid command."

    def handle_client(self, client_socket):
        """
        Handles communication with a connected client.

        Args:
        - client_socket (socket.socket): The socket connected to the client.
        """
        while True:
            request = client_socket.recv(1024)
            if not request:
                break
            response = self.process_command(request.decode('utf-8'))
            client_socket.send(response.encode('utf-8'))
        client_socket.close()

    def start_server(self):
        """
        Starts the email server and listens for incoming connections.
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12348
    PROVIDER_NAME = 'gmail'
    USER_EMAIL = 'your-email@example.com'
    USER_PASSWORD = 'your_password'

    email_server = EmailServer(HOST, PORT, PROVIDER_NAME, USER_EMAIL, USER_PASSWORD)
    email_server.start_server()