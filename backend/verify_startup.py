"""Verification script for backend startup and imports."""
import sys

print("=" * 50)
print("Backend Startup Verification")
print("=" * 50)

# Test 1: State module imports
print("\n[1/4] Testing state module imports...")
try:
    from app.core.state import ClinicalState, ToolCall, ReasoningStep, PatientContext
    print("  ✓ ClinicalState imported")
    print("  ✓ ToolCall imported")
    print("  ✓ ReasoningStep imported")
    print("  ✓ PatientContext imported")
except Exception as e:
    print(f"  ✗ State import failed: {e}")
    sys.exit(1)

# Test 2: Main app imports
print("\n[2/4] Testing main app import...")
try:
    from app.main import app
    print("  ✓ FastAPI app imported successfully")
except Exception as e:
    print(f"  ✗ Main app import failed: {e}")
    sys.exit(1)

# Test 3: Graph module (with checkpointer)
print("\n[3/4] Testing graph module with checkpointer...")
try:
    # Note: This will create checkpoints.db on import
    from app.core import graph
    print("  ✓ Graph module imported")
    print(f"  ✓ Checkpointer configured with path: {graph.CHECKPOINT_DB_PATH}")
except Exception as e:
    print(f"  ✗ Graph import failed: {e}")
    sys.exit(1)

# Test 4: Check if checkpoints.db exists
print("\n[4/4] Checking checkpoints.db file...")
import os
checkpoint_paths = [
    "checkpoints.db",
    "backend/checkpoints.db",
    "../checkpoints.db"
]
found = False
for path in checkpoint_paths:
    if os.path.exists(path):
        print(f"  ✓ Found checkpoints.db at: {os.path.abspath(path)}")
        found = True
        break

if not found:
    print("  ℹ checkpoints.db not yet created (will be created on first graph invocation)")

print("\n" + "=" * 50)
print("All imports successful! Backend is ready to start.")
print("=" * 50)
