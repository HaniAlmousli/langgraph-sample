"""
LangSmith configuration for debugging LangGraph applications.
Set your LangSmith API key and project name here.
"""
import os
from datetime import datetime

# LangSmith Configuration
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Replace with your actual LangSmith API key
# Make sure this key has the correct permissions and is active
api_key = "..."

# Validate API key format
if not api_key.startswith("lsv2_"):
    print("⚠️  Warning: API key doesn't start with 'lsv2_'. Please check your LangSmith API key.")
elif len(api_key) < 50:
    print("⚠️  Warning: API key seems too short. Please check your LangSmith API key.")

os.environ["LANGCHAIN_API_KEY"] = api_key

# Create a unique project name for each run session
def get_session_project_name(base_name="langgraph-sample", include_timestamp=True):
    """Generate a unique project name for the current session"""
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{base_name}-{timestamp}"
    return base_name

# Set the project name - you can customize this
SESSION_PROJECT_NAME = get_session_project_name("langgraph-sample")
os.environ["LANGCHAIN_PROJECT"] = SESSION_PROJECT_NAME

# Optional: Set to true for more detailed logging
os.environ["LANGCHAIN_VERBOSE"] = "true"

print(f"🔧 LangSmith configured with project: {os.environ['LANGCHAIN_PROJECT']}")
print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")

# Export the function for use in other modules
__all__ = ["get_session_project_name", "SESSION_PROJECT_NAME"] 