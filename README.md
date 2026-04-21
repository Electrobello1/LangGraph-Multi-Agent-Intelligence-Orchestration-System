# 🔍 LangGraph Multi-Agent Intelligence Orchestration System

A **multi-agent AI system built with LangGraph** that analyzes GitHub repositories, extracts insights from README files, evaluates documentation quality, and generates structured feedback using multiple tools and agents.
## 🚀 Overview

This project implements an **agentic workflow system** that automatically:
- Fetches GitHub repository data
- Parses and analyzes README files
- Extracts meaningful metadata
- Evaluates documentation quality
- Generates improvement feedback

The system is built using a **multi-agent architecture** orchestrated with LangGraph.
---

## 🧠 Key Features

- 🧩 Multi-agent system (content, metadata, structure, quality, reviewer)
- 🔗 GitHub API integration
- 📄 README content extraction and parsing
- 📊 Repository metadata analysis (stars, forks, language)
- 🧪 Rule-based + heuristic quality scoring
- 🔁 Conditional retry loop (improve until pass)
- ⚙️ Fully deterministic + extensible pipeline

---
## 🏗️ Architecture

```text
GitHub Repo URL
        ↓
┌─────────────────────┐
│   Analyzer Agent     │  → Fetch README + Repo metadata (API tool)
└─────────────────────┘
        ↓
────────────────────────────────────────
↓                ↓                ↓
Content        Metadata       Structure
Agent          Agent           Agent
↓                ↓                ↓
────────────────────────────────────────
        ↓
   Quality Agent
        ↓
   Reviewer Agent
        ↓
     Final Output
```

## 🤖 Agents Description

### 🧠 1. Analyzer Agent
Responsible for:
- Fetching README content from GitHub API
- Retrieving repository metadata (stars, forks, language)

---

### ✍️ 2. Content Agent
Responsible for:
- Extracting the project title
- Generating a short summary of the README

---

### 🏷️ 3. Metadata Agent
Responsible for:
- Extracting keywords from README
- Generating meaningful tags for the repository

---

### 🧱 4. Structure Agent
Responsible for:
- Checking presence of required sections:
  - Installation
  - Usage
  - License
- Identifying missing documentation parts

---

### 📊 5. Quality Agent
Responsible for:
- Computing README quality score based on:
  - Length
  - Formatting
  - Presence of code blocks

---

### 🧑‍⚖️ 6. Reviewer Agent
Responsible for:
- Aggregating outputs from all agents
- Generating final feedback
- Deciding final status:
  - PASS or RETRY
  
## 🔧 Tools Used

| 🛠️ Tool Name            | 📌 Purpose                         | ⚙️ Type              |
|------------------------|-----------------------------------|---------------------|
| GitHub README API      | Fetch repository README content    | API Integration     |
| GitHub Repository API  | Retrieve stars, forks, language    | API Integration     |
| README Parser          | Extract title, summary, tags       | Text Processing     |
| Quality Scoring Tool   | Evaluate documentation quality     | Analysis / Scoring  |

## 📦 Features

- Multi-agent orchestration using LangGraph
- GitHub API integration
- Rule-based analysis engine
- Structured output generation
- Conditional retry logic
- Extensible tool-based architecture

## ⚙️ Installation
1. Clone the repository
git clone https://github.com/your-username/repo-intelligence-agent.git
cd repo-intelligence-agent

2. Install dependencies
pip install requests langgraph

3. Run the system
python main.py

## 📊 Example Output
▶️ Usage

Run the system with a GitHub repository URL:

result = app.invoke({
    "repo_url": "https://github.com/example/repo"
})

{
  "repo_url": "https://github.com/example/repo",
  "stars": 9,
  "forks": 6,
  "language": "Python",
  "title": "Flask Chatbot System",
  "summary": "A chatbot built using Flask and DialoGPT",
  "tags": ["flask", "chatbot", "api"],
  "missing_sections": [],
  "quality_score": 3,
  "review_feedback": {},
  "status": "pass"
}


##  🧪 Example Workflow
Input: GitHub URL
↓
Fetch README + metadata
↓
Run parallel agents:
   - content extraction
   - metadata extraction
   - structure validation
↓
Quality scoring
↓
Final review decision
↓
Output structured result

🛠️ Tech Stack
Python 🐍
LangGraph 🧠
GitHub REST API 🌐
Regex & Text Processing
Functional Multi-Agent Design

 ##  📈 Key Features Demonstrated

  - Multi-agent orchestration
  - Tool integration beyond LLMs

- API-based data extraction

- Rule-based reasoning system

- Structured AI evaluation pipeline

## 🚀 Future Improvements

Add LLM-based semantic reviewer
Improve tagging using embeddings
Add web search tool (Tavily / SerpAPI)
Export results as PDF report
Build FastAPI web dashboard
Add repository ranking system (0–100 score)

## 📁 Project Structure

## 📁 Project Structure

```text
repo-intelligence-agent/
│
├── main.py            # Entry point: runs the LangGraph workflow and prints results
├── graph.py           # Defines and compiles the LangGraph pipeline
├── state.py           # Shared state schema (A3State)
├── agents.py          # All agent nodes (analyzer, content, metadata, reviewer, etc.)
├── tools.py           # External tools (GitHub API, parsing, scoring functions)
│
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation

```
## 👨‍💻 Author
Princewill Bello

## 📜 License
MIT