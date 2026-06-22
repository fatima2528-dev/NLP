FROM python:3.11-slim

WORKDIR /app

COPY requirements-deploy.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY frontend/ frontend/
COPY data/ data/
COPY vectorstore/ vectorstore/

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
