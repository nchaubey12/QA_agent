# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

app = FastAPI(title="QA Agent")

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="qa_agent",
    session_service=session_service,
)

class QARequest(BaseModel):
    context: str
    question: str

class QAResponse(BaseModel):
    answer: str

@app.get("/")
async def dashboard():
    return FileResponse("dashboard.html", media_type="text/html")

@app.post("/ask", response_model=QAResponse)
async def ask(request: QARequest):
    if not request.context.strip() or not request.question.strip():
        raise HTTPException(status_code=400, detail="Both context and question are required.")

    session = await session_service.create_session(
        app_name="qa_agent",
        user_id="user",
    )

    user_message = f"Context: {request.context}\n\nQuestion: {request.question}"

    message = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    result_text = ""
    async for event in runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    result_text += part.text

    return QAResponse(answer=result_text)

@app.get("/health")
def health():
    return {"status": "ok"}
