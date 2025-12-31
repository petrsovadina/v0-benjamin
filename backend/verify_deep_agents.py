#!/usr/bin/env python
"""Verify Deep Agents (create_react_agent) import path works with LangGraph 1.x"""

try:
    from langgraph.prebuilt import create_react_agent
    print("Deep Agents available")
    print(f"create_react_agent function: {create_react_agent}")
except ImportError as e:
    print(f"Import error: {e}")
    exit(1)
