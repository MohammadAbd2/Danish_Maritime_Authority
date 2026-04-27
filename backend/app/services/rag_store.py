from pathlib import Path

class RAGStore:
    def __init__(self):
        self.docs = Path(__file__).resolve().parents[3] / "knowledge" / "clinical_reference.md"
        self._content = self.docs.read_text(encoding="utf-8") if self.docs.exists() else ""
        self._uploaded = []

    def add_texts(self, texts, metadatas=None):
        for i, text in enumerate(texts):
            meta = (metadatas or [{}])[i] if metadatas else {}
            self._uploaded.append({"text": text or "", "meta": meta})

    def retrieve(self, query: str, limit: int = 4):
        base_chunks = [c.strip() for c in self._content.split("\n## ") if c.strip()]
        upload_chunks = []
        for d in self._uploaded:
            txt = d["text"]
            for i in range(0, min(len(txt), 6000), 900):
                upload_chunks.append(f"Uploaded file {d['meta'].get('filename','document')}: {txt[i:i+900]}")
        chunks = base_chunks + upload_chunks
        scored = []
        q_terms = set((query or "").lower().split())
        for c in chunks:
            score = sum(1 for t in q_terms if t in c.lower())
            scored.append((score, c[:1000]))
        return [c for _, c in sorted(scored, reverse=True)[:limit] if c]
