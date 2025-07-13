"""
Test script with LangSmith integration for debugging LangGraph applications.
This script will run your graphs and send all traces to LangSmith for analysis.
"""

# Import LangSmith configuration first
from utils import langsmith_config

from graphs.notice_extraction import NOTICE_EXTRACTION_GRAPH
from graphs.email_agent import email_agent_graph
from example_emails import EMAILS
from langsmith import traceable

@traceable(name="test_notice_extraction")
def test_notice_extraction():
    """Test the notice extraction graph with LangSmith tracing"""
    print("Testing Notice Extraction Graph...")
    
    initial_state = {
        "notice_message": EMAILS[0],
        "notice_email_extract": None,
        "escalation_text_criteria": """There's a risk of fire or water damage at the site""",
        "escalation_dollar_criteria": 100_000,
        "requires_escalation": False,
        "escalation_emails": ["brog@abc.com", "bigceo@company.com"],
    }

    final_state = NOTICE_EXTRACTION_GRAPH.invoke(initial_state)
    
    print(f"Extracted data: {final_state['notice_email_extract']}")
    print(f"Requires escalation: {final_state['requires_escalation']}")
    
    return final_state

@traceable(name="test_email_agent")
def test_email_agent():
    """Test the email agent graph with LangSmith tracing"""
    print("Testing Email Agent Graph...")
    
    message_1 = {"messages": [("human", EMAILS[0])]}
    
    print("Streaming email agent response...")
    for chunk in email_agent_graph.stream(message_1, stream_mode="values"):
        chunk["messages"][-1].pretty_print()
    
    return "Email agent test completed"

@traceable(name="main_test_runner")
def main():
    """Main test runner with LangSmith tracing"""
    print("Starting LangSmith-enabled tests...")
    
    # # Test notice extraction
    # notice_result = test_notice_extraction()
    
    # Test email agent
    email_result = test_email_agent()
    
    print("All tests completed! Check LangSmith for detailed traces.")
    return  email_result

if __name__ == "__main__":
    main() 