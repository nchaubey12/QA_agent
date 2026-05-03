def answer_question(context: str, question: str) -> str:
    """
    Formats a context + question pair for the agent to answer.
    Args:
        context: The background text or passage to reason over.
        question: The question to answer based on the context.
    Returns:
        A formatted prompt string.
    """
    return (
        f"Using only the information provided below, answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )
