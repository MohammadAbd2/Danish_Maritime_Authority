from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="Maritime Medical AI Auditor", version="1.1.0")

# Development-friendly CORS for Vite/React and FastAPI docs.
# This prevents the browser from hiding useful API errors behind a CORS failure.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "maritime-medical-ai-auditor", "version": "1.1.0"}

app.include_router(router, prefix="/api")
