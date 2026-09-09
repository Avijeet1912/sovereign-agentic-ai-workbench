# Sovereign Agentic AI Workbench

**SIH26117** — Smart India Hackathon MVP

An AI assistant that answers questions using confidential industrial documents and structured industrial data, while keeping everything local and enforcing role-based access.

> This is a **prototype for an internal hackathon**, NOT a production enterprise system.
> All data is **synthetic/fake** and used only for demonstration purposes.

---

## Features

- Local AI answering with Ollama (no cloud APIs)
- SQLite database with synthetic industrial data
- Simple document retrieval (RAG)
- Role-based access control (Admin / Engineer / Operator)
- Audit logging
- Clean modern dashboard

---

## Architecture

```
Internet
   X

React (Vite)
    ↓
FastAPI (Python)
    ↓
SQLite
    ↓
Local Documents (.md)
    ↓
Ollama
    ↓
Local AI
```

No request is sent to an external AI service.

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| Frontend | React + Vite |
| Backend | FastAPI (Python) |
| Database | SQLite |
| AI | Ollama (local model) |
| Auth | JWT + bcrypt |

---

## Installation

### 1. Install Python

```bash
python --version  # Should be 3.10+
```

### 2. Install Node.js

```bash
node --version  # Should be 18+
npm --version
```

### 3. Install Ollama

```bash
# Download from https://ollama.com
# Then pull a small model suitable for 8GB RAM:
ollama pull phi3:mini
```

### 4. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

### 6. Configure Environment

```bash
cp .env.example .env
# Edit .env as needed
```

---

## How to Run

### Backend

```bash
cd backend
python app.py
```

Backend will run at `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm run dev
```

Frontend will run at `http://localhost:5173`

### Health Check

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

---

## Demo Credentials

These are for the local synthetic prototype only:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Engineer | engineer | engineer123 |
| Operator | operator | operator123 |

---

## Example Questions

- "Why did Pump 4 experience repeated shutdowns last month, and what was the production impact?"
- "How many hours was Pump 4 down in March?"
- "Which equipment had the highest downtime?"
- "What was the production loss during Pump 4 shutdowns?"

---

## Offline Usage

After all dependencies and models are installed, the application works without internet.
No request is sent to an external AI service.

---

## Known Limitations

- This is a prototype, not production-ready
- Uses synthetic/fake data only
- AI answers may be inaccurate or hallucinated
- Single-user only
- No enterprise security guarantees