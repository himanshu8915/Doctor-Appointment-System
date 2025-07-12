# 🏥 Agentic Medical Assistant System

An end-to-end AI-powered healthcare assistant platform that allows users to:
- 📅 Schedule, cancel, or reschedule doctor appointments
- 🩺 Chat with **Dr. Samvedna**, your empathetic virtual medical companion
- 💾 Store and retrieve conversation data using MongoDB and Redis

> Built with FastAPI + LangGraph + Redis + MongoDB + Streamlit

---

## 🌟 Features

### 🤖 Agentic AI System
Uses **LangGraph** to power a multi-node conversation agent that routes queries intelligently to:
- `booking_node`: handles appointment management
- `information_node`: provides doctor availability & FAQ answers
- `personal_assistant`: answers user-specific questions about past interactions and medical help

### 🧠 Memory + Persistence
- 🧾 **Redis Checkpointing** to preserve conversational state
- 🗃️ **MongoDB Integration** to store long-term user data and conversation history

### 💬 Streamlit UI
- Easy-to-use dashboard for interacting with the assistant
- Sidebar login using `user_name` and `user_id`
- Separate tabs for appointment scheduling and personal medical assistant

---

## 🚀 Tech Stack

| Layer         | Tool                      |
|---------------|---------------------------|
| Backend       | FastAPI                   |
| Agent Engine  | LangGraph + LangChain     |
| Memory        | Redis (LangGraph Checkpoint) |
| Database      | MongoDB (Cloud or local)  |
| Model         | Groq API (LLaMA / Mixtral)|
| Frontend      | Streamlit                 |
| Container     | Docker & Docker Compose   |

---

## 📁 Folder Structure

