# from graphs.notice_extraction import NOTICE_EXTRACTION_GRAPH
# from example_emails import EMAILS

# initial_state = {
#      "notice_message": EMAILS[0],
#      "notice_email_extract": None,
#     "escalation_text_criteria": """There's a risk of fire or
#      water damage at the site""",
#      "escalation_dollar_criteria": 100_000,
#      "requires_escalation": False,
#     "escalation_emails": ["brog@abc.com", "bigceo@company.com"],
# }

# final_state = NOTICE_EXTRACTION_GRAPH.invoke(initial_state)

# final_state["notice_email_extract"]


# final_state["requires_escalation"]
# #-----------------
#************************************************************

# from graphs.notice_extraction import NOTICE_EXTRACTION_GRAPH
# from example_emails import EMAILS

# initial_state_no_escalation = {
#     "notice_message": EMAILS[0],
#      "notice_email_extract": None,
#      "escalation_text_criteria": """There's a risk of water
#       damage at the site""",
#      "escalation_dollar_criteria": 100_000,
#      "requires_escalation": False,
#      "escalation_emails": ["brog@abc.com", "bigceo@company.com"],
#  }


# initial_state_escalation = {
#      "notice_message": EMAILS[0],
#      "notice_email_extract": None,
#      "escalation_text_criteria": """Workers explicitly violating safety protocols""",
#      "escalation_dollar_criteria": 100_000,
#      "requires_escalation": False,
#      "escalation_emails": ["brog@abc.com", "bigceo@company.com"],
#  }

# no_esc_result = NOTICE_EXTRACTION_GRAPH.invoke(initial_state_no_escalation)

# no_esc_result["requires_escalation"]

# esc_result = NOTICE_EXTRACTION_GRAPH.invoke(initial_state_escalation)

# esc_result["requires_escalation"]
#************************************************************

from graphs.email_agent import email_agent_graph
from example_emails import EMAILS
message_1 = {"messages": [("human", EMAILS[0])]}
for chunk in email_agent_graph.stream(message_1, stream_mode="values"):
      chunk["messages"][-1].pretty_print()