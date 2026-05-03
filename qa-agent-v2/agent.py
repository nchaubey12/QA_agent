from google.adk.agents import Agent
from tools import answer_question

root_agent = Agent(
    name="qa_agent",
    model="gemini-2.5-flash",
    description="Answers questions based on a provided context passage.",
    instruction=(
        "You are a precise question-answering assistant. "
        "When given a context and a question, use the answer_question tool "
        "to format the input, then provide a clear, concise answer "
        "based strictly on the context. "
        "If the answer cannot be found in the context, say so honestly."
    ),
    tools=[answer_question],
)
