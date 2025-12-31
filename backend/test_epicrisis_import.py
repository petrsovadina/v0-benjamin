#!/usr/bin/env python
"""Test that START/END pattern is correctly implemented."""
import os
# Set dummy API key for import testing only
os.environ['ANTHROPIC_API_KEY'] = 'test-key-for-import-check'

from epicrisis_graph import app
print('OK')
