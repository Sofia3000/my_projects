from abc import ABC, abstractmethod

class Logger(ABC):
    """Abstract base class defining the logger interface."""
    @abstractmethod
    def log(self, data: str) -> None:
        """Log the provided string data."""

class ConsoleLogger(Logger):
    def log(self, data: str) -> None:
        """Log message to the console (standard output)."""
        print(data)

class FileLogger(Logger):
    def log(self, data: str) -> None:
        """Log message to a file named 'data.log'. Overwrites file each time."""
        with open('data.log', 'w') as fhand:
            fhand.write(data)

class Printer(ABC):
    @abstractmethod
    def create_logger(self) -> Logger:
        """Return logger object"""

    def print_message(self, message: str) -> None:
        """
        Validates the message and logs it using a Logger instance
        """
        # Check type
        if not isinstance(message, str):
            raise TypeError('Message must be a string')
        
        # Check value
        if not message.strip():
            raise ValueError('Message can not be empty')
        
        # Log message
        logger = self.create_logger()
        logger.log(message)
        print('Message was logged successfully')

class ConsolePrinter(Printer):
    "Uses a console logger to output messages."
    def create_logger(self):
        return ConsoleLogger()
    
class FilePrinter(Printer):
    "Uses a file logger to output messages."
    def create_logger(self):
        return FileLogger()

def main():
    # Test Printers
    console_printer = ConsolePrinter()
    file_printer = FilePrinter()

    print("Тестування ConsolePrinter:")
    console_printer.print_message("Hello, Console!")

    print("\nТестування FilePrinter:")
    file_printer.print_message("Hello, File!")

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()