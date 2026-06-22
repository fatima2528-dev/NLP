"""Fatima's Assistant — RAG chat API + static frontend."""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field

load_dotenv()

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
VECTORSTORE_DIR = ROOT / "vectorstore"
FRONTEND_DIR = ROOT / "frontend"

SYSTEM_TEMPLATE = (
    "You are Fatima's Assistant, a chatbot that answers questions about Fatima Jawad "
    "using ONLY the context below.\n"
    "- Use only facts found in the context; never use outside knowledge.\n"
    "- You MAY combine facts from several context chunks to give a complete answer.\n"
    "- Use the conversation history to resolve follow-up questions (e.g. \"her\", \"that project\").\n"
    "- If the answer is genuinely not in the context, say: "
    "\"I don't have that information in the provided CV.\"\n"
    "- Be concise and quote details (dates, CGPA, titles) exactly as written.\n\n"
    "Context:\n{context}"
)


def load_documents():
    documents = []
    for path in sorted(DATA_DIR.glob("*")):
        if path.suffix.lower() in (".txt", ".md"):
            documents.extend(TextLoader(str(path), encoding="utf-8").load())
        elif path.suffix.lower() == ".pdf":
            documents.extend(PyPDFLoader(str(path)).load())
    if not documents:
        raise FileNotFoundError(f"No documents found in {DATA_DIR}/")
    return documents


def build_rag():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if VECTORSTORE_DIR.exists():
        vectorstore = FAISS.load_local(
            str(VECTORSTORE_DIR), embeddings, allow_dangerous_deserialization=True
        )
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(load_documents())
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(str(VECTORSTORE_DIR))

    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    return retriever, llm


retriever, llm = build_rag()


def ask(question: str, history: list[dict]) -> str:
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    messages: list[tuple[str, str]] = [
        ("system", SYSTEM_TEMPLATE.format(context=context)),
    ]
    for msg in history[-6:]:
        role = msg.get("role", "")
        content = msg.get("content", "").strip()
        if not content:
            continue
        if role == "user":
            messages.append(("human", content))
        elif role == "assistant":
            messages.append(("ai", content))

    messages.append(("human", question))
    prompt = ChatPromptTemplate.from_messages(messages)
    response = (prompt | llm).invoke({})
    return response.content


app = FastAPI(title="Fatima's Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = [msg.model_dump() for msg in req.history]
    answer = ask(req.message.strip(), history)
    return ChatResponse(answer=answer)


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
