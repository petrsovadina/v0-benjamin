import sys
import os

# Add backend to path so we can import app
sys.path.append(os.path.join(os.getcwd(), "backend"))

try:
    from app.core.graph import app
    print("Graph compiled successfully.")
    
    # Optional: visualisation
    try:
        print(app.get_graph().draw_mermaid())
    except Exception as e:
        print(f"Could not draw graph: {e}")
        
except Exception as e:
    print(f"Graph compilation failed: {e}")
    sys.exit(1)
