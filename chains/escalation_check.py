from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langsmith import traceable

# Import LangSmith configuration
# from utils import langsmith_config

class EscalationCheck(BaseModel):
    needs_escalation: bool = Field(
        description="""Whether the notice requires escalation
        according to specified criteria"""
    )

escalation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Determine whether the following notice received
            from a regulatory body requires immediate escalation.
            Immediate escalation is required when {escalation_criteria}.

            Here's the notice message:

            {message}
            """,
        )
    ]
)

escalation_check_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@traceable(name="escalation_check_chain")
def create_escalation_check_chain():
    """Create the escalation check chain with tracing"""
    return (
        escalation_prompt
        | escalation_check_model.with_structured_output(EscalationCheck)
    )

ESCALATION_CHECK_CHAIN = create_escalation_check_chain()