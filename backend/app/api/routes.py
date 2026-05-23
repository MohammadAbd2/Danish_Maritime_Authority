from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from app.models.schemas import RMRSubmission, ReviewResponse, UploadedDocument
from app.services.clinical_reviewer import ClinicalReviewer
from app.services.memory_store import MemoryStore
from app.services.document_parser import extract_text, extract_structured_data
from app.services.pdf_exporter import build_pdf

router = APIRouter()
reviewer = ClinicalReviewer()
memory = MemoryStore()
uploaded_documents = []

@router.get("/health")
def api_health():
    return {"status": "ok", "message": "Backend API is running"}

@router.post("/review", response_model=ReviewResponse)
def review_record(payload: RMRSubmission):
    try:
        if uploaded_documents and not payload.uploaded_context:
            payload.uploaded_context = "\n\n".join(d["text"] for d in uploaded_documents[-3:])[:12000]
        result = reviewer.review(payload)
        memory.save_review(payload, result)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Review failed: {exc}")

@router.post("/files/upload", response_model=UploadedDocument)
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text, kind = extract_text(file.filename, content)
        doc = {"filename": file.filename, "kind": kind, "text": text}
        uploaded_documents.append(doc)
        try:
            reviewer.rag.add_texts([text], metadatas=[{"filename": file.filename, "kind": kind}])
        except Exception:
            pass
        
        # Extract structured data for auto-fill
        structured_data = extract_structured_data(text)
        
        return UploadedDocument(
            filename=file.filename, 
            characters=len(text), 
            preview=text[:5000],
            extracted_data=structured_data
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}")

@router.get("/files")
def list_files():
    return [{"index": i, "filename": d["filename"], "kind": d["kind"], "characters": len(d["text"]), "preview": d["text"][:300]} for i, d in enumerate(uploaded_documents)]

@router.delete("/files/clear")
def clear_files():
    uploaded_documents.clear()
    return {"status": "cleared"}

@router.post("/export/pdf")
def export_pdf(payload: RMRSubmission):
    try:
        result = reviewer.review(payload)
        pdf = build_pdf(payload, result)
        return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=radio-medical-record-review.pdf"})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {exc}")

@router.get("/history")
def history(limit: int = 10):
    return memory.list_recent(limit=limit)
