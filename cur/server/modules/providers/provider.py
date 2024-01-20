class MailServiceProvider:
    """
    A class representing an email service provider configuration.

    This class uses the Singleton design pattern to ensure that only one instance
    is created for each unique set of SMTP and IMAP/POP3 server configurations.

    Attributes:
    - smtp_server (str): The SMTP server address for sending emails.
    - smtp_port (int): The SMTP server port number.
    - imap_server (str): The IMAP server address for receiving emails.
    - pop3_server (str): The POP3 server address for receiving emails.

    Methods:
    - __new__(cls, smtp_server, smtp_port, imap_server, pop3_server): Creates a new instance or returns an existing one.
    - __init__(self, smtp_server, smtp_port, imap_server, pop3_server): Initializes the provider with server configurations.
    """

    _instances = {}
    def __new__(cls, smtp_server, smtp_port, imap_server, pop3_server):
        """
        Creates a new instance or returns an existing one based on server configurations.

        Args:
        - smtp_server (str): The SMTP server address for sending emails.
        - smtp_port (int): The SMTP server port number.
        - imap_server (str): The IMAP server address for receiving emails.
        - pop3_server (str): The POP3 server address for receiving emails.

        Returns:
        - instance: An instance of MailServiceProvider.

        Note:
        If an instance with the same server configurations exists, it is returned.
        Otherwise, a new instance is created and stored for future use.
        """
        key = (smtp_server, smtp_port, imap_server, pop3_server)
        if key not in cls._instances:
            instance = super(MailServiceProvider, cls).__new__(cls)
            cls._instances[key] = instance
            return instance
        return cls._instances[key]

    def __init__(self, smtp_server, smtp_port, imap_server, pop3_server):
        """
        Initializes the provider with server configurations.

        Args:
        - smtp_server (str): The SMTP server address for sending emails.
        - smtp_port (int): The SMTP server port number.
        - imap_server (str): The IMAP server address for receiving emails.
        - pop3_server (str): The POP3 server address for receiving emails.

        Note:
        This method is called when a new instance is created, but it only initializes
        the instance if it's the first time for the given server configurations.
        """
        if not hasattr(self, '_initialized'):
            self.smtp_server = smtp_server
            self.smtp_port = smtp_port
            self.imap_server = imap_server
            self.pop3_server = pop3_server
            self._initialized = True
