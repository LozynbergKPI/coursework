from abc import ABC, abstractmethod

class MailTemplate(ABC):
    """
    An abstract base class representing a template for email operations.

    This class defines the structure for performing email operations, such as connecting to
    the server, preparing a message, sending a message, and disconnecting from the server.

    Attributes:
    - provider: The email service provider configuration.
    - user_email (str): The user's email address.
    - user_password (str): The user's email account password.

    Methods:
    - perform_email_operation(self): Performs a sequence of email operations (template method).
    - connect_to_server(self): Abstract method to connect to the email server.
    - prepare_message(self): Abstract method to prepare an email message.
    - send_message(self): Abstract method to send an email message.
    - disconnect_from_server(self): Abstract method to disconnect from the email server.
    """
    def __init__(self, provider, user_email, user_password):
        """
        Initializes the MailTemplate with provider and user credentials.

        Args:
        - provider: The email service provider configuration.
        - user_email (str): The user's email address.
        - user_password (str): The user's email account password.
        """
        self.provider = provider
        self.user_email = user_email
        self.user_password = user_password

    def perform_email_operation(self):
        """
        Performs a sequence of email operations (template method).

        Subclasses should implement the abstract methods to define the specific
        behavior of connecting to the server, preparing a message, sending a message,
        and disconnecting from the server.
        """
        self.connect_to_server()
        self.prepare_message()
        self.send_message()
        self.disconnect_from_server()

    @abstractmethod
    def connect_to_server(self):
        """
        Abstract method to connect to the email server.

        Subclasses should implement this method with the specific logic for
        connecting to the email server.
        """
        pass

    @abstractmethod
    def prepare_message(self):
        """
        Abstract method to prepare an email message.

        Subclasses should implement this method with the specific logic for
        preparing the email message.
        """
        pass

    @abstractmethod
    def send_message(self):
        """
        Abstract method to send an email message.

        Subclasses should implement this method with the specific logic for
        sending the email message.
        """
        pass

    @abstractmethod
    def disconnect_from_server(self):
        """
        Abstract method to disconnect from the email server.

        Subclasses should implement this method with the specific logic for
        disconnecting from the email server.
        """
        pass
