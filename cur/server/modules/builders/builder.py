from cur.server.modules.emailClients.email_client import EmailClient
from cur.server.modules.organizers.organizer import MailManager

class MailClientBuilder:
    """
    A builder class for creating instances of EmailClient and MailManager.

    Methods:
    - __init__(self): Initializes a new MailClientBuilder instance.
    - set_provider(self, provider): Sets the email service provider for the builder.
    - set_user_email(self, user_email): Sets the user's email address for the builder.
    - set_user_password(self, user_password): Sets the user's email account password for the builder.
    - build(self): Builds and returns an EmailClient instance based on the provided parameters.
    - build_organizer(self): Builds and returns a MailManager instance based on the provided parameters.
    """

    def __init__(self):
        """
        Initializes a new MailClientBuilder instance.
        """
        self._provider = None
        self._user_email = None
        self._user_password = None

    def set_provider(self, provider):
        """
        Sets the email service provider for the builder.

        Args:
        - provider: The email service provider.

        Returns:
        - MailClientBuilder: The builder instance with the provider set.
        """
        self._provider = provider
        return self

    def set_user_email(self, user_email):
        """
        Sets the user's email address for the builder.

        Args:
        - user_email (str): The user's email address.

        Returns:
        - MailClientBuilder: The builder instance with the user's email set.
        """
        self._user_email = user_email
        return self

    def set_user_password(self, user_password):
        """
        Sets the user's email account password for the builder.

        Args:
        - user_password (str): The user's email account password.

        Returns:
        - MailClientBuilder: The builder instance with the user's password set.
        """
        self._user_password = user_password
        return self

    def build(self):
        """
        Builds and returns an EmailClient instance based on the provided parameters.

        Returns:
        - EmailClient: An EmailClient instance.
        """
        if not all([self._provider, self._user_email, self._user_password]):
            raise ValueError("Required fields are missing.")
        return EmailClient(self._provider, self._user_email, self._user_password)

    def build_organizer(self):
        """
        Builds and returns a MailManager instance based on the provided parameters.

        Returns:
        - MailManager: A MailManager instance.
        """
        if not all([self._provider, self._user_email, self._user_password]):
            raise ValueError("Required fields are missing.")
        return MailManager(self._provider, self._user_email, self._user_password)

class MailProcessor:
    """
    A class for interpreting and executing email-related commands.

    Attributes:
    - email_organizer (MailManager): An instance of MailManager for email operations.

    Methods:
    - __init__(self, email_organizer): Initializes a new MailProcessor instance.
    - interpret(self, command): Interprets a command and performs the corresponding email operation.
    """

    def __init__(self, email_organizer):
        """
        Initializes a new MailProcessor instance.

        Args:
        - email_organizer (MailManager): An instance of MailManager for email operations.
        """
        self.email_organizer = email_organizer

    def interpret(self, command):
        """
        Interprets a command and performs the corresponding email operation.

        Args:
        - command (str): The command to interpret and execute.
        """
        if "send email" in command:
            self.email_organizer.perform_email_operation()
        elif "classify emails" in command:
            self.email_organizer.classify_and_move_emails()
        elif "save draft" in command:
            self.email_organizer.save_draft("recipient@example.com", "Draft Subject", "Draft Body")
        elif "list folders" in command:
            print("List of folders...")
        elif "read emails" in command:
            self.email_organizer.read_emails()
        else:
            print("Invalid command.")
