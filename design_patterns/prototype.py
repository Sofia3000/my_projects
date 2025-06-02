from abc import ABC, abstractmethod
import copy

# Prototype Interface
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

# Concrete Prototype
class Document(Prototype):
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    # Clone current object
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nContent: {self.content}"

# Test Document   
def main():
    # Create document template
    template = Document("Report Template", "Content goes here...", "Admin")

    # Create copy with new author
    user_doc1 = template.clone()
    user_doc1.author = "Alice"

    # Create copy with new title and content
    user_doc2 = template.clone()
    user_doc2.title = "Final Report"
    user_doc2.content = "New content"

    # Output all documents
    print("Original template:")
    print(template)

    print("\nCloned Document 1:")
    print(user_doc1)

    print("\nCloned Document 2:")
    print(user_doc2)

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()