#!/usr/bin/env python3
"""Test script to verify translator_graph.py compiles correctly.

This test verifies that all imports work and the graph can be compiled
with the upgraded LangChain/LangGraph dependencies. It uses dummy
environment variables since we only need to verify compilation, not
actual API functionality.
"""
import os

# Set dummy environment variables for compilation testing
# These are only used for validation - no actual API calls are made
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-for-compilation-check")
os.environ.setdefault("OPENAI_API_KEY", "test-key-for-compilation-check")
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "test-key-for-compilation-check")

try:
    from translator_graph import app
    print('Translator graph compiled:', app is not None)
except Exception as e:
    print(f'Compilation failed: {e}')
    exit(1)
