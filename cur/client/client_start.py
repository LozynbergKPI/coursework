import socket
import os
from colorama import init, Fore
import pyfiglet

class EmailClient:
    """
    A simple email client for managing email messages through a command-line interface.

    Attributes:
    - host (str): The email server's hostname or IP address.
    - port (int): The port number to connect to on the email server.
    - client (socket.socket): A socket object for communication with the email server.

    Methods:
    - __init__(self, host, port): Initializes the EmailClient instance with the provided host and port.
    - connect(self): Establishes a connection to the email server.
    - send_command(self, command): Sends a command to the email server and returns the response.
    - configure(self): Configures the email client by requesting user input for email provider, user email, and password.
    - run(self): Runs the email client's main loop to process user commands.
    - print_help(): Static method that prints the available commands and their descriptions.
    """

    def __init__(self, host, port):
        """
        Initializes a new EmailClient instance.

        Args:
        - host (str): The hostname or IP address of the email server.
        - port (int): The port number to connect to on the email server.
        """
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        """
        Establishes a connection to the email server using a socket.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def send_command(self, command):
        """
        Sends a command to the email server and receives the response.

        Args:
        - command (str): The command to send to the email server.

        Returns:
        - response (str): The response received from the email server.
        """
        self.client.send(command.encode('utf-8'))
        response = self.client.recv(4096).decode('utf-8')
        return response

    def configure(self):
        """
        Configures the email client by obtaining necessary information from the user, such as email provider,
        user email address, and password.
        """
        init(autoreset=True)
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = pyfiglet.figlet_format("Email Client", font="slant")
        print(f"{Fore.GREEN}{banner.strip()}{Fore.RESET}")

        print(f"{Fore.BLUE}To configure the email client, please provide the following information:")
        provider_name = input(f"{Fore.BLUE}Enter your email provider (e.g., 'gmail'): {Fore.RESET}")
        user_email = input(f"{Fore.BLUE}Enter your full email address (e.g., 'example@gmail.com'): {Fore.RESET}")
        user_password = input(f"{Fore.BLUE}Enter your email account password: {Fore.RESET}")

        explanation = f"{Fore.BLUE}This information is required to set up your email client " \
                      f"so it can connect to your email server and manage your messages. " \
                      f"Please make sure to enter accurate details.{Fore.RESET}"

        response = self.send_command(f"CONFIG {provider_name} {user_email} {user_password}")
        print(explanation)
        print(f"{Fore.YELLOW}{response}{Fore.RESET}")

    def run(self):
        """
        Runs the main loop of the email client, processing user commands until the user decides to exit.
        """
        while True:
            command = input(f"{Fore.BLUE}Enter a command (or 'exit' to quit, 'help' for available commands): {Fore.RESET}")
            if command.lower() == 'exit':
                break
            elif command.lower() == 'help':
                self.print_help()
                continue
            response = self.send_command(command)
            print(f"{Fore.YELLOW}Response: {response}{Fore.RESET}")

        self.client.close()

    @staticmethod
    def print_help():
        """
        Static method that prints the available commands and their descriptions.
        """
        print(f"{Fore.CYAN}Available commands:")
        print(f"{Fore.CYAN}config - Configure email client.")
        print(f"{Fore.CYAN}send - Send an email.")
        print(f"{Fore.CYAN}classify - Classify and move emails.")
        print(f"{Fore.CYAN}save - Save a draft email.")
        print(f"{Fore.CYAN}read - Read emails from inbox.")
        print(f"{Fore.CYAN}exit - Exit the email client.{Fore.RESET}")

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12348
    email_client = EmailClient(HOST, PORT)
    email_client.connect()
    email_client.configure()
    email_client.run()
