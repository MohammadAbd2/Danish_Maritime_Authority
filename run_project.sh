#!/bin/bash
set -e

echo "========================================="
echo "🚀 Starting Maritime AI Maritime Medical System"
echo "========================================="

command -v node >/dev/null 2>&1 || { echo "❌ Node.js is not installed"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is not installed"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 is not installed"; exit 1; }
command -v ollama >/dev/null 2>&1 || { echo "❌ Ollama is not installed"; exit 1; }

echo "🧠 Starting Ollama..."
(ollama serve > ollama.log 2>&1 & echo $! > .ollama.pid) || true
sleep 3

echo "📥 Checking model: mistral..."
if ! ollama list | grep -q mistral; then
  echo "⬇️ Pulling mistral model..."
  ollama pull mistral
fi

echo "⚙️ Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
  echo "📦 Creating Python virtual environment..."
  python3 -m venv venv
fi
source venv/bin/activate

echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

echo "🚀 Starting FastAPI backend..."
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > backend.log 2>&1 &
echo $! > ../.backend.pid
cd ..

echo "💻 Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
  echo "📦 Installing frontend dependencies..."
  npm install
fi

echo "🚀 Starting React frontend with Vite..."
npm run dev -- --host 127.0.0.1 > frontend.log 2>&1 &
echo $! > ../.frontend.pid
cd ..

echo ""
echo "========================================="
echo "✅ Project is running"
echo "========================================="
echo "🌐 Frontend:    http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000/docs"
echo "📄 Logs: ollama.log, backend/backend.log, frontend/frontend.log"
echo "🛑 Press CTRL+C to stop"
echo "========================================="

trap 'echo "Stopping..."; kill $(cat .frontend.pid 2>/dev/null) $(cat .backend.pid 2>/dev/null) 2>/dev/null || true; exit 0' INT TERM
wait
