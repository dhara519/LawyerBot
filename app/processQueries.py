# Function looks for specific words in the question and returns the relevant information.
# If it can't find an answer, it asks the user to rephrase the question.


# Function to process user queries
def get_legal_info(query):
    query = query.lower()

    # Search in legal framework
    if "state law" in query or "MGL" in query:
        return legal_framework["state_laws"]["MGL_Ch90_S20A"]["description"]

    if "boston parking rules" in query:
        return legal_framework["city_ordinances"]["boston_traffic_rules"]["sections"]["article_IV"]["title"]

    # Search in appeal process
    if "appeal deadline" in query:
        return appeal_process["administrative_appeal"]["deadline"]

    if "online appeal" in query:
        return appeal_process["administrative_appeal"]["methods"]["online"]["platform"]

    if "court appeal" in query:
        return appeal_process["court_process"]["judge_appeal"]["required_forms"]

    return "I'm sorry, I couldn't find information on that topic. Please rephrase your question."

# Example Queries
print(get_legal_info("What is the deadline for appeal?"))
print(get_legal_info("Tell me about state laws on parking violations."))
print(get_legal_info("Where can I file an online appeal?"))