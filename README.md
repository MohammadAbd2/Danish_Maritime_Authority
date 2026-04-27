# AI-Assisted Clinical Evaluation System for Maritime Nursing

A bilingual English/Danish React + FastAPI application for digitising the Radio Medical Record and reviewing maritime nursing documentation with local AI-style orchestration, clinical rules, uploaded document context, RAG-ready storage and professional PDF export.

## Students

- Mohammad Abd Al Rahem
- Ahmed Asfour

## Features

- React frontend based on the Radio Medical Record structure.
- Danish Maritime Authority / Søfartsstyrelsen visual style with the provided logo.
- English, Danish or bilingual interface and output.
- FastAPI backend with REST endpoints.
- Clinical review agent that checks ABCDE documentation, observations and inconsistencies.
- Dynamic advice based on the entered case, including fast heartbeat/running scenarios.
- File upload support for PDF, DOCX, TXT and scanned image reports.
- Uploaded file text is extracted, shown in the UI, used as AI context, and included in the exported PDF.
- Button to remove uploaded context.
- Button to generate random realistic test data.
- Professional downloadable PDF report.
- Server status indicator: checking, running or down.
- Promptfoo and unit-test structure included.

## Requirements

Install these first:

- Python 3.10+
- Node.js 18+
- npm
- Ollama
- Tesseract OCR if you want scanned image text extraction

Pull the local model:

```bash
ollama pull mistral
```

For OCR on Ubuntu/Linux:

```bash
sudo apt install tesseract-ocr
```

## Run everything

From the project root:

```bash
chmod +x run_project.sh
./run_project.sh
```

Open:

- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs

## Manual run

Terminal 1:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

## API endpoints

- `GET /health` — backend status
- `GET /api/health` — API status used by the frontend
- `POST /api/review` — review a Radio Medical Record
- `POST /api/files/upload` — upload PDF/DOCX/TXT/image context
- `GET /api/files` — list uploaded context files
- `DELETE /api/files/clear` — clear uploaded context
- `POST /api/export/pdf` — generate a downloadable PDF
- `GET /api/history` — recent review history

## How uploaded files are used

When a file is uploaded, the backend extracts text from it. The frontend shows a preview so the nurse can verify the content. The extracted text is sent with the review request, used by the clinical reviewer as context, and included in the PDF report under uploaded document context.

## Testing

Backend:

```bash
cd backend
source venv/bin/activate
pytest
```

Frontend:

```bash
cd frontend
npm test
```

Promptfoo:

```bash
cd promptfoo
promptfoo eval
```

## Troubleshooting

If `localhost refused to connect`, check logs:

```bash
cat backend/backend.log
cat frontend/frontend.log
cat ollama.log
```

If PDF export or review fails, open http://localhost:8000/docs and test `/api/health`. The frontend status badge should show whether the server is running.
