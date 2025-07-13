from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langsmith import traceable

# Import LangSmith configuration
from utils import langsmith_config

class BinaryAnswer(BaseModel):
    is_true: bool = Field(
        description="""Whether the answer to the question is yes or no.
        True if yes otherwise False."""
    )

binary_question_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Answer this question as True for "yes" and False for "no".
            No other answers are allowed:

            {question}
            """,
        )
    ]
)

binary_question_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@traceable(name="binary_question_chain")
def create_binary_question_chain():
    """Create the binary question chain with tracing"""
    return (
        binary_question_prompt
        | binary_question_model.with_structured_output(BinaryAnswer)
    )

BINARY_QUESTION_CHAIN = create_binary_question_chain()