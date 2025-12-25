import sys
import os

# Ensure project root is in python path
current_dir = os.getcwd()
sys.path.append(current_dir)
print(f"Added {current_dir} to sys.path")

try:
    print("Attempting to import GuidelinesLoader...")
    from backend.data_processing.loaders.guidelines_loader import GuidelinesLoader
    print("Import successful!")
    
    print("Attempting to instantiate GuidelinesLoader...")
    loader = GuidelinesLoader()
    print("Instantiation successful!")
    
except Exception as e:
    print(f"Error caught: {e}")
    import traceback
    traceback.print_exc()
