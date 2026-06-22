# Hugging Face Spaces Deployment Guide

Follow these steps to deploy **Fatima's Assistant** publicly.

## Prerequisites

- Hugging Face account: https://huggingface.co/join
- Groq API key: https://console.groq.com
- Project files ready in this folder

## Option A — Upload via Web UI

1. Go to https://huggingface.co/new-space
2. **Space name:** `fatimas-assistant`
3. **License:** MIT (or any)
4. **SDK:** Docker
5. Click **Create Space**
6. Upload these files/folders:
   - `app.py`
   - `Dockerfile`
   - `requirements-deploy.txt`
   - `README.md`
   - `frontend/` (folder)
   - `data/` (folder with CV.pdf)
   - `vectorstore/` (folder)
7. **Settings → Repository secrets → New secret**
   - Name: `GROQ_API_KEY`
   - Value: paste your Groq key
8. Go to **App** tab and wait for build (5–15 min first time)
9. Copy your live URL and paste it into `README.md` under **Live Demo**

## Option B — Deploy with Git

```powershell
cd d:\Code\Nlp
git init
git add app.py Dockerfile requirements-deploy.txt README.md frontend data vectorstore build_vectorstore.py rag.ipynb .env.example .gitignore
git commit -m "Fatima's Assistant RAG chatbot"
```

Create the Space on Hugging Face (Docker SDK), then:

```powershell
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/fatimas-assistant
git push origin main
```

Add `GROQ_API_KEY` in Space Settings → Repository secrets.

## Verify Deployment

1. Open the Space URL in an incognito browser window
2. Ask: "What is Fatima Jawad's CGPA?"
3. Ask a follow-up: "Which university is that at?" (tests chat history)
4. Ask off-topic: "Who is Einstein?" — should refuse politely

## Update README

After deployment works, edit `README.md` and replace:

```
https://huggingface.co/spaces/YOUR_USERNAME/fatimas-assistant
```

with your actual Space URL before submitting the ZIP.
