from abc import ABC, abstractmethod

class Window(ABC):
    """Interface for a window component"""
    @abstractmethod
    def get_bg_color(self) -> int:
        """Returns background color code."""

    @abstractmethod
    def get_title(self) -> str:
        """Returns the title text for the window."""

class Text(ABC):
    """Interface for a text component"""
    @abstractmethod
    def get_text_color(self) -> int:
        """Returns text color code."""

    @abstractmethod
    def get_text(self) -> str:
        """Returns the content text."""

class LightWindow(Window):
    """Light-themed window implementation."""
    def get_bg_color(self) -> int:
        return 47 # White background

    def get_title(self) -> str:
        return "Light Window"

class DarkWindow(Window):
    """Dark-themed window implementation."""
    def get_bg_color(self) -> int:
        return 40 # Black background
    
    def get_title(self) -> str:
        return "Dark Window"

class LightText(Text):
    """Text component for light theme."""
    def get_text_color(self) -> int:
        return 34 # Blue text
    
    def get_text(self) -> str:
        return "This is a light-themed interface."

class DarkText(Text):
    """Text component for dark theme."""
    def get_text_color(self) -> int:
        return 36 # Cyan text
    
    def get_text(self) -> str:
        return "This is a dark-themed interface."

class ThemeFactory(ABC):
    """Abstract factory for creating themed UI components."""
    @abstractmethod
    def create_window(self) -> Window:
        pass

    @abstractmethod
    def create_text(self) -> Text:
        pass

class LightTheme(ThemeFactory):
    """Factory for creating light-themed UI components."""
    def create_window(self) -> Window:
        return LightWindow()

    def create_text(self) -> Text:
        return LightText()
    
class DarkTheme(ThemeFactory):
    """Factory for creating dark-themed UI components."""
    def create_window(self) -> Window:
        return DarkWindow()

    def create_text(self) -> Text:
        return DarkText()

def render_ui(factory: ThemeFactory):
    """
    Renders UI components using the given theme factory.
    Applies text and background color using ANSI escape codes.
    """
    window = factory.create_window()
    text = factory.create_text()
    # Display window title and text with proper styling
    print(f"\033[{text.get_text_color()};{window.get_bg_color()}m{window.get_title()}")
    print(f"{text.get_text()}\033[0m")
  
def main():
    # Test Factories 
    print("Light theme")
    render_ui(LightTheme())
    print('-'*40)
    print("Dark theme")
    render_ui(DarkTheme())

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()