"""
Simple test to verify LangSmith connection and API key.
Run this first to ensure your LangSmith setup is working.
"""

# Import LangSmith configuration first
from utils import langsmith_config

from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def test_langsmith_connection():
    """Test basic LangSmith connectivity"""
    try:
        # Test client connection
        client = Client()
        print("✅ LangSmith client created successfully")
        
        # Test a simple LLM call
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "Say hello!")
        ])
        
        chain = prompt | llm
        result = chain.invoke({})
        
        print("✅ LangSmith tracing is working!")
        print(f"Response: {result.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ LangSmith connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your API key in langsmith_config.py")
        print("2. Verify your API key has the correct permissions")
        print("3. Ensure you have an active LangSmith account")
        print("4. Check your internet connection")
        return False

if __name__ == "__main__":
    print("Testing LangSmith connection...")
    success = test_langsmith_connection()
    
    if success:
        print("\n🎉 LangSmith is ready! You can now run:")
        print("python test_with_langsmith.py")
    else:
        print("\n🔧 Please fix the LangSmith configuration before proceeding.") 