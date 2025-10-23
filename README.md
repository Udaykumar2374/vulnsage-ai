# 🧠 VulnSage – AI-Powered Vulnerability Triage Assistant

VulnSage is an autonomous AI assistant that helps security teams efficiently **triage, classify, and remediate vulnerability reports**. Inspired by HackerOne's **Hai Agent**, this tool uses LLMs, embeddings, and smart retrieval to deliver actionable security insights instantly.

---

## 🚀 Features

- 🧠 **LLM-Powered Intelligence** – Answers questions & analyzes vulnerability text.
- 📄 **File Upload Support** – Upload `.txt`, `.md`, or `.pdf` files for analysis.
- 🕵️‍♂️ **Duplicate Detection** – Finds similar past reports using embeddings.
- 🎯 **Severity Classification** – Estimates severity via CVSS/OWASP/CWE.
- 🧾 **Structured Output** – Outputs summaries, remediation, and source references.
- 🧠 **Retrieval-Augmented Generation (RAG)** – Enriches results with OWASP/CWE docs.
- 🧪 **Fullstack App** – React (frontend) + FastAPI (backend) + LangChain (LLM tools).

---

## 💻 Tech Stack

| Layer      | Tools Used |
|------------|------------|
| Frontend   | React, Tailwind CSS, Vite |
| Backend    | FastAPI, LangChain, python-dotenv |
| LLMs       | OpenRouter API (GPT-3.5-turbo) |
| Embeddings | HuggingFace MiniLM + FAISS |
| RAG        | LangChain RetrievalQA |
| File Upload| FastAPI + FormData |

---

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/vulnsage.git
cd vulnsage
