import os
from fastapi import FastAPI
from pydantic import BaseModel

from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import calculator


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

model = OllamaModel(
    host=OLLAMA_HOST,
    model_id=OLLAMA_MODEL,
    temperature=0.2,
    keep_alive="30m",
)

agent = Agent(
    model=model,
    tools=[calculator],
    system_prompt=(
        "You are a kitchen assistant agent called Homer. You can answer "
        "questions about cooking and recipes." ),
)

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    response = agent(req.message)
    return {"response": str(response)}