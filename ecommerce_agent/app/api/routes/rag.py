from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import tempfile
import os
from pydantic import BaseModel

from langchain_chroma import Chroma

from app.rag.ingestion import ingest_document, embeddings
from app.rag.retrieval import query_rag


router = APIRouter(prefix="/rag")

# --------- Ingestion endpoint ---------
@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    collection: str = Form(default="default"),
    tags: str = Form(default="")
):
    # Write uploaded bytes to a temp file so loaders (PyPDFLoader etc.) can open it

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{file.filename.split('.')[-1]}"
    ) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        print(f"Ingesting {tmp_path}")
        print(f"Collecting {collection} with tags: {tags}")
        result = ingest_document(tmp_path, file.filename, collection, tags)
        return result
    finally:
        os.unlink(tmp_path)   # Always clean up the temp file


class QueryRequest(BaseModel):
    question: str
    collection: str = "default"
    topK: int = 4
    citeSources: bool = True

# --------- Retrieval endpoint ---------
@router.post("/query")
async def query(req: QueryRequest):
    try:
        result = query_rag(req.question, req.collection, req.topK, req.citeSources)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- List of Documents endpoint ---------
@router.get("/documents")
async def list_docs(collection: str = "default"):

    store = Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory="././chroma_db"
    )
    # Get all stored metadata
    data = store.get()
    seen = set()
    files = []
    for meta in data["metadatas"]:
        src = meta.get("source_file", "unknown")
        if src not in seen:
            seen.add(src)
            files.append({"file": src, "collection": collection})
    return {"documents": files, "total_chunks": len(data["ids"])}