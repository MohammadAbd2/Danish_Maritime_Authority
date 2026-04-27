from datetime import datetime

class MemoryStore:
    _items = []

    def save_review(self, record, result):
        self._items.append({
            "created_at": datetime.utcnow().isoformat() + "Z",
            "patient_name": getattr(record.patient, "name_title", ""),
            "score": result.score,
            "finding_count": len(result.findings),
        })

    def list_recent(self, limit=10):
        return list(reversed(self._items))[:limit]
