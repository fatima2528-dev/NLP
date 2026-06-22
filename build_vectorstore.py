"""Build FAISS vectorstore from data/ without starting the web server."""

from app import VECTORSTORE_DIR, build_rag

if __name__ == "__main__":
    if VECTORSTORE_DIR.exists():
        print(f"Vectorstore already exists at {VECTORSTORE_DIR}/")
    else:
        build_rag()
        print(f"Built vectorstore at {VECTORSTORE_DIR}/")
