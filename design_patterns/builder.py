from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional, Any

class Report:
    """
    Represents a structured report consisting of a title, content, and footer.
    Stores parts of a report identified by keys and allows combining them
    into a complete textual representation. Only predefined part names
    ('title', 'content', 'footer') are allowed.
    """
    # Allowed part names
    _part_names = ('title', 'content', 'footer')
    
    def __init__(self) -> None:
        self._parts = {}

    def add(self, key: str, value: str) -> None:
        """
        Adds a part to the report by its name and content.
        """
        # Check types
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError('Key and Value must be strings')
        
        # Check key value
        key = key.strip().lower()
        if key not in self._part_names:
            raise ValueError(f'Wrong part name "{key}"')
        
        self._parts[key] = value

    def __str__(self) -> str:
        """
        Return the full report as a string by combining all parts in order.
        Only non-empty parts are included.
        """
        return '\n'.join(self._parts.get(key, '') for key in self._part_names if self._parts.get(key, ''))

# Decorator for text validation
def validate_text(func):
    @wraps(func)
    def wrapper(self, text: str) -> Optional[Any]:
        # Delete whitespaces
        text = text.strip()
        # Call func if text is not empty
        if text:
            return func(self, text)
    return wrapper

class ReportBuilder(ABC):
    """Abstract builder interface for constructing report parts."""
    
    @abstractmethod
    def add_title(self, text: str) -> None:
        pass
    
    @abstractmethod
    def add_content(self, text: str) -> None:
        pass

    @abstractmethod
    def add_footer(self, text: str) -> None:
        pass

    @abstractmethod
    def get_result(self) -> Report:
        pass


# Bulder for plain text 
class PlainTextReportBuilder(ReportBuilder):
    """Builder for constructing report with plain text."""
    def __init__(self):
        self._report = Report()

    @validate_text
    def add_title(self, text: str) -> None:
        """Adds the title section to the report."""
        self._report.add('title', text)
    
    @validate_text
    def add_content(self, text: str) -> None:
        """Adds main content to the report."""
        self._report.add('content', text)

    @validate_text
    def add_footer(self, text: str) -> None:
        """Adds the footer section to the report."""
        self._report.add('footer', text)

    def get_result(self) -> Report:
        """Returns constructed report"""
        report = self._report
        # Reset builder state to allow reuse
        self._report = Report()
        return report

# Bulder for markdown text 
class MarkdownReportBuilder(ReportBuilder):
    """Builder for constructing report with markdown text."""
    def __init__(self):
        self._report = Report()

    @validate_text
    def add_title(self, text: str) -> None:
        """Adds the title section to the report."""
        self._report.add('title', '# '+text)

    @validate_text
    def add_content(self, text: str) -> None:
        """Adds main content to the report."""
        self._report.add('content', text + '\n')

    @validate_text
    def add_footer(self, text: str) -> None:
        """Adds the footer section to the report."""
        self._report.add('footer', '---\n' + text)

    def get_result(self) -> Report:
        """Returns constructed report"""
        report = self._report
        # Reset builder state to allow reuse
        self._report = Report()
        return report

class Director:
    """Constructs a report by delegating part addition to the builder."""
    def __init__(self, builder: ReportBuilder):
        # Check builder's type
        if not isinstance(builder, ReportBuilder):
            raise TypeError('Builder must be instance of ReportBuilder')   
        self._builder = builder
    
    def construct_report(self, title: str, content: str, footer: str) -> None:
        """
        Builds a complete report by calling builder methods 
        in the correct order.
        """
        self._builder.add_title(title)
        self._builder.add_content(content)
        self._builder.add_footer(footer)

# Test Builders   
def main():
    # Test with PlainTextReportBuilder
    print("Testing PlainTextReportBuilder:")
    plain_builder = PlainTextReportBuilder()
    director = Director(plain_builder)

    # Construct the report using the director
    director.construct_report(
        title="Monthly Sales",
        content="Sales increased by 20%.",
        footer="Report generated on 2025-06-04"
    )
    # Get the built report and print it
    simple_report = plain_builder.get_result()
    print(simple_report)
    print("-" * 40)

    # Test with MarkDownReportBuilder
    print("Testing MarkDownReportBuilder:")
    markdown_builder = MarkdownReportBuilder()
    director = Director(markdown_builder)

    # Construct the report using the director
    director.construct_report(
        title="Monthly Sales",
        content="Sales increased by 20%.",
        footer="Report generated on 2025-06-04"
    )
    # Get the built report and print it
    markdown_report = markdown_builder.get_result()
    print(markdown_report)

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()