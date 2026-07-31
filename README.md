# AKM45 Vector AI — Production AI Resume Screening Platform

[![CI/CD Pipeline](https://github.com/hiresmart-ai/hiresmart-ai/actions/workflows/ci.yml/badge.svg)](https.github.com/hiresmart-ai/hiresmart-ai/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15.1-black.svg)](https://nextjs.org)

**AKM45 Vector AI** is an enterprise-grade, production-ready AI-powered Applicant Tracking System (ATS). It automates candidate resume parsing, skill extraction, vector-based semantic search, weighted ATS match calculation, and LLM candidate evaluation reports.

---

## 🌟 Key Features

- **⚡ Multi-Format Document Parsing**: PyMuPDF (fitz), `python-docx`, and pytesseract OCR fallback for scanned PDF and DOCX resumes.
- **🧠 500+ Skill Taxonomy & NER**: spaCy NLP entity extraction + regex boundary matcher categorizing programming languages, frameworks, databases, cloud, DevOps, AI/ML, and soft skills.
- **🔍 FAISS Vector Semantic Search**: Encodes documents with `BAAI/bge-small-en-v1.5` into 384-dimensional embeddings for natural language candidate queries.
- **📊 Weighted ATS Matching Engine**:
  - **Skill Match (40%)**: Jaccard overlap of required vs. candidate skills.
  - **Semantic Match (30%)**: Cosine similarity between job and candidate embeddings.
  - **Experience Match (20%)**: Proportional years of experience rating.
  - **Education Match (10%)**: Degree level evaluation.
- **💡 Llama 3 LLM Candidate Reports**: Ollama powered candidate executive summaries, strengths, missing critical skills, and technical interview questions.
- **🔒 Enterprise Security & Auth**: JWT access/refresh token rotation, bcrypt password hashing, RBAC (Admin, Recruiter, Candidate), and Resend email verification.

---

## 🏗️ Clean Architecture

```
hiresmart-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (auth, companies, jobs, applications, resumes, matching)
│   │   ├── services/     # Business & domain logic layer
│   │   ├── repositories/ # Async SQLAlchemy 2.0 Repository pattern
│   │   ├── models/       # Relational ORM models with UUID PKs
│   │   ├── schemas/      # Pydantic request & response validation
│   │   ├── ai/           # Parser, Embeddings (FAISS), Matching Engine, LLM (Ollama)
│   │   └── workers/      # Celery task queue & Redis broker
│   ├── tests/            # Unit & Integration Pytest suites
│   └── Dockerfile        # Multi-stage Docker build
├── frontend/
│   ├── app/              # Next.js 15 App Router (Auth & Dashboard routes)
│   ├── components/       # shadcn/ui + Framer Motion components
│   ├── hooks/            # TanStack Query & Zustand hooks
│   └── services/         # Axios API wrappers
└── docker-compose.yml    # Complete containerized local dev environment
```

---

## 🚀 Quick Start (Local Development with Docker)

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone repository & initialize environment
```bash
cd hiresmart-ai
cp .env.example .env
```

### 2. Start services with Docker Compose
```bash
docker compose up -d
```

Services will boot up at:
- **Frontend App**: `http://localhost:3000`
- **FastAPI OpenAPI Docs**: `http://localhost:8000/docs`
- **MailHog Local Email**: `http://localhost:8025`
- **Celery Flower Dashboard**: `http://localhost:5555`

---

## 🧪 Running Automated Tests

```bash
# Run backend Pytest suite inside Docker container
docker compose exec backend pytest tests/unit -v
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
