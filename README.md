# 🏥 AI-First CRM – HCP Log Interaction Module

An **AI-first Customer Relationship Management (CRM) system** focused on the **Log Interaction Screen** for Healthcare Professionals (HCPs).  
This module is designed for **life sciences field representatives** to log, edit, and analyze HCP interactions using **natural language**, powered by **LangGraph and LLMs**.

The solution supports both **structured form-based logging** and a **conversational chat interface**, exactly as required in the assignment.

---

## 🎯 Assignment Context (Task 1)

This project was built as part of **Round 1 – Technical & Development Task** for the  
**AI-First CRM HCP Module – Log Interaction Screen**.

Core requirements addressed:
- React UI with Redux for state management
- FastAPI backend
- LangGraph-based AI agent
- LLM integration using **Groq (gemma2-9b-it)**
- SQL-based persistence
- Conversational + structured interaction logging

---

## 🌟 Key Features

### ✨ AI-Powered Log Interaction Screen
- **Conversational Logging**  
  Field reps can describe an HCP interaction in natural language instead of filling long forms.

- **Automatic Data Extraction**  
  The AI extracts structured fields such as:
  - HCP name
  - Interaction date
  - Sentiment
  - Discussed products
  - Shared materials
  - Follow-up intent

- **Conversational Editing**  
  Logged interactions can be updated by saying things like  
  _“Actually, the HCP name was Dr. Mehta”_ without manually editing fields.

---

## 🤖 LangGraph Multi-Tool AI Agent

A **LangGraph agent** orchestrates decision-making and tool execution.  
Instead of a single LLM call, the agent maintains state and routes user input to the appropriate tool.

### Implemented Tools (5)

1. **Log Interaction**  
   Converts free-text input into structured CRM data using the LLM.

2. **Edit Interaction**  
   Allows partial updates to existing interaction records via conversational input.

3. **Schedule Follow-Up**  
   Suggests next actions, follow-up timelines, and talking points for the sales representative.

4. **Extract Insights**  
   Analyzes interaction history to identify opportunities, risks, or engagement signals.

5. **Validate HCP**  
   Normalizes HCP names, formats specialties, and improves data consistency.

Each tool is implemented as a **LangGraph node**, allowing controlled execution and clear separation of responsibilities.

---

## 🧠 Why LangGraph?

LangGraph is used to build a **stateful, multi-step AI agent** that mirrors how a real sales assistant operates.

The agent:
1. Interprets the user’s intent (log, edit, analyze, validate)
2. Selects the appropriate tool
3. Executes tools in sequence when needed
4. Maintains conversational context across turns

This approach enables the **Log Interaction Screen** to seamlessly support:
- Structured form-based workflows
- Conversational chat-based workflows

Exactly as required in the assignment.

---

## 🎨 Frontend Experience

- **Split-Screen Interface**
  - **Left Panel**: Auto-filled, read-only structured form controlled by AI
  - **Right Panel**: Conversational chat interface with the AI agent

- **Modern UI**
  - Built with **React 18**, **Redux Toolkit**, and **Vite**
  - Uses **Google Inter** font
  - Responsive layout suitable for field representatives

---

## 🧱 Tech Stack

### Frontend
- React 18
- Redux Toolkit
- Vite
- Google Inter Font

### Backend
- Python 3.10+
- FastAPI
- LangGraph
- SQLAlchemy

### AI & LLM
- Groq API
- Model: **gemma2-9b-it**
- Optional context support via llama-3.3-70b-versatile

### Database
- SQLite (development and demo)
- PostgreSQL / MySQL compatible schema

> **Note:** SQLite is used for local development simplicity.  
> The ORM layer and schema are fully compatible with PostgreSQL or MySQL as required by the assignment.

---

⚙️ Running the Application Locally
---
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py


cd frontend
npm install
npm run dev
---