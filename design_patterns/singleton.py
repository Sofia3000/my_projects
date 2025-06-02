class IDGenerator:
    # IDGenerator instance reference
    _instance = None
    # Flag to ensure one-time initialization
    _initialized = False

    def __new__(cls):
        # Create instance if it doesn't exist yet
        if not cls._instance:
            cls._instance = super(IDGenerator, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Initialize only once
        if not self._initialized:
            # Set start value for id
            self._id = 0
            self._initialized = True

    def get_next_id(self):
        # Return new id
        self._id += 1
        return self._id
    
    def reset(self):
        # Reset id
        self._id = 0

def main():
    # Create two generators
    gen1 = IDGenerator()
    gen2 = IDGenerator()

    # Compare gen1 and gen2
    print("gen1 is gen2:", gen1 is gen2)

    # Generate id 4 times
    print("gen1 ID 1:", gen1.get_next_id())
    print("gen2 ID 2:", gen2.get_next_id())
    print("gen1 ID 3:", gen1.get_next_id())
    print("gen2 ID 4:", gen2.get_next_id())

    # Reset id
    gen1.reset()

    # Generate one id
    print("After reset:")
    print("gen2 ID 1 again:", gen2.get_next_id())

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()