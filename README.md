# Fatima's Assistant

A **Retrieval-Augmented Generation (RAG)** chatbot that answers questions about **Fatima Jawad** using only her personal CV. Built for an NLP course assignment demonstrating document indexing, vector search, prompt engineering, and deployment.

## Live Demo

**Deployment URL:** `https://huggingface.co/spaces/YOUR_USERNAME/fatimas-assistant`

> Replace with your Hugging Face Space URL after deployment (see [Deployment](#deployment) below).

## Features

- Personal dataset: CV (`data/CV.pdf`)
- Named chatbot identity: **Fatima's Assistant**
- Full RAG pipeline: load → split → embed → FAISS → retrieve → generate
- Grounded answers with anti-hallucination prompt (`temperature=0`)
- **Chat history** for follow-up questions
- Minimal web chat UI (HTML + FastAPI)

## RAG Pipeline

```
data/CV.pdf
     |
[ Load ] --> [ Split ] --> [ Embed ] --> [ FAISS store ]
                                              |
User question ----------------------> [ Retrieve k chunks ]
                                              |
                                              v
                                    [ Groq LLM + prompt ]
                                              |
                                              v
                                         Answer
```

| Step | Tool |
|------|------|
| Load | PyPDFLoader |
| Split | RecursiveCharacterTextSplitter (500 chars, 100 overlap) |
| Embed | HuggingFace `all-MiniLM-L6-v2` |
| Store | FAISS (local, saved in `vectorstore/`) |
| Retrieve | Top-6 similar chunks |
| Generate | Groq `llama-3.3-70b-versatile` |

## Tech Stack

- **LangChain** 0.3.x — RAG orchestration
- **FAISS** — vector database
- **sentence-transformers** — embeddings
- **Groq API** — LLM inference
- **FastAPI + Uvicorn** — backend API
- **Docker** — Hugging Face Spaces deployment

## Project Structure

```
Nlp/
├── app.py                  # FastAPI server + RAG logic
├── build_vectorstore.py    # Build FAISS index locally
├── rag.ipynb               # Step-by-step RAG tutorial notebook
├── Dockerfile              # HF Spaces Docker config
├── requirements.txt        # Full deps (local + notebook)
├── requirements-deploy.txt # Lean deps for Docker deploy
├── data/
│   └── CV.pdf              # Personal dataset
├── vectorstore/            # Pre-built FAISS index
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── .env.example            # API key template
```

## Local Setup

### 1. Clone / unzip and enter the project

```powershell
cd d:\Code\Nlp
```

### 2. Create virtual environment (recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Set API key

Copy `.env.example` to `.env` and add your Groq key:

```
GROQ_API_KEY=gsk-your-key-here
```

Get a free key at [console.groq.com](https://console.groq.com).

### 5. Build vector index (first time only)

```powershell
python build_vectorstore.py
```

### 6. Run the app

```powershell
python app.py
```

Open **http://127.0.0.1:8000** in your browser.

## Example Questions

- What is Fatima Jawad's current CGPA?
- Which university is she studying at?
- What programming languages does she know?
- Tell me about her projects.
- What freelance experience does she have?

## Deployment

Deploy on **Hugging Face Spaces** (Docker). Vercel is not suitable for this Python ML backend.

### Step-by-step

1. Create an account at [huggingface.co](https://huggingface.co).
2. Click **New Space** → Name: `fatimas-assistant` → SDK: **Docker** → Create.
3. Upload or git-push these files:
   - `app.py`, `Dockerfile`, `requirements-deploy.txt`
   - `frontend/`, `data/`, `vectorstore/`
   - `README.md`
4. Go to Space **Settings → Repository secrets** and add:
   - Name: `GROQ_API_KEY`
   - Value: your Groq API key
5. Wait for the Docker build to finish (check **Logs** tab).
6. Your live URL will be:
   `https://huggingface.co/spaces/YOUR_USERNAME/fatimas-assistant`

### Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails (memory) | Ensure `vectorstore/` is included so embeddings are not rebuilt |
| App crashes on start | Check Logs; verify `GROQ_API_KEY` secret is set |
| Slow first request | Normal — embedding model downloads once on cold start |

## Anti-Hallucination Design

- Strict system prompt: answer **only** from retrieved CV chunks
- `temperature=0` for deterministic output
- Fixed refusal phrase when answer is not in documents
- Retrieval uses only the latest question (not polluted by chat history)

## Author

Fatima Jawad — NLP / Software Engineering assignment

## License

Educational use only.
