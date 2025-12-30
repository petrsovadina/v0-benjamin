import sys
import os

# Add project root to path so we can use 'backend.app...' imports
# The script should be run from the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from backend.app.core.graph import app
    print("Graph compiled successfully.")
    
    # Optional: visualisation
    try:
        print(app.get_graph().draw_mermaid())
    except Exception as e:
        print(f"Could not draw graph: {e}")
        
except Exception as e:
    print(f"Graph compilation failed: {e}")
    sys.exit(1)
