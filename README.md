<p align="center">
  <img src="assets/workflow_graph.png" alt="SupportSense-AI Workflow" width="480"/>
</p>

<h1 align="center">🧠 SupportSense-AI</h1>

<p align="center">
  <em>Intelligent, AI-Powered Customer Review Analysis &amp; Response System</em>
</p>

<p align="center">
  <a href="#-features"><img src="https://img.shields.io/badge/LangGraph-Workflow-blueviolet?style=for-the-badge" alt="LangGraph"/></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/LLM-Groq%20Cloud-orange?style=for-the-badge" alt="Groq"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"/></a>
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+"/></a>
</p>

---

## 📖 Overview

**SupportSense-AI** is an agentic AI system that **automatically analyzes customer reviews**, detects sentiment, diagnoses issues in negative feedback, and generates context-aware support responses — all orchestrated through a **LangGraph state-machine workflow**.

Instead of writing rigid if-else logic, SupportSense-AI leverages **LLM-powered structured outputs** and **conditional graph routing** to dynamically decide how to handle each review, producing professional, empathetic replies in real time.

---

## ✨ Features

| Capability | Description |
|:---|:---|
| 🔍 **Sentiment Detection** | Classifies reviews as `positive` or `negative` using LLM structured output |
| 🩺 **Issue Diagnosis** | For negative reviews — identifies `issue_type`, `tone`, and `urgency` automatically |
| 💬 **Dynamic Response Generation** | Generates warm thank-you messages for positive reviews, and empathetic troubleshooting replies for negative ones |
| 🔀 **Conditional Routing** | LangGraph's conditional edges intelligently route the workflow based on detected sentiment |
| 🏗️ **Structured Output Schemas** | Pydantic models enforce reliable, typed outputs from the LLM at every node |

---

## 🏛️ Architecture

The system is built as a **LangGraph StateGraph** with the following nodes and edges:

```
┌─────────┐
│  START   │
└────┬─────┘
     │
     ▼
┌────────────────┐
│ find_sentiment │  ← Classifies review as positive/negative
└────┬───────────┘
     │
     ├── positive ──►  ┌───────────────────┐
     │                 │ positive_response  │ ──► END
     │                 └───────────────────┘
     │
     └── negative ──►  ┌───────────────┐     ┌───────────────────┐
                        │ run_diagnosis │ ──► │ negative_response │ ──► END
                        └───────────────┘     └───────────────────┘
```

### Workflow Nodes

| Node | Purpose | Output |
|:---|:---|:---|
| `find_sentiment` | Analyzes the review text and classifies sentiment | `{ sentiment: "positive" \| "negative" }` |
| `positive_response` | Generates a warm, appreciative thank-you message | `{ response: "..." }` |
| `run_diagnosis` | Diagnoses the negative review across 3 dimensions | `{ diagnosis: { issue_type, tone, urgency } }` |
| `negative_response` | Crafts an empathetic, actionable support reply using diagnosis context | `{ response: "..." }` |

### Shared State Schema

```python
class ReviewState(TypedDict):
    review: str        # The raw customer review text
    sentiment: str     # Detected sentiment (positive/negative)
    diagnosis: dict    # Structured diagnosis for negative reviews
    response: str      # The generated reply message
```

### Structured Output Schemas

**SentimentSchema** — enforces binary classification:
```python
class SentimentSchema(BaseModel):
    sentiment: Literal['positive', 'negative']
```

**DiagnosisSchema** — multi-dimensional issue analysis:
```python
class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX/UI", "Performance", "Bug", "Support", "Other"]
    tone: Literal["angry", "frustrated", "disappointed", "calm"]
    urgency: Literal["low", "Medium", "High"]
```

---

## 🛠️ Tech Stack

| Technology | Role |
|:---|:---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful workflow orchestration with conditional routing |
| [LangChain](https://github.com/langchain-ai/langchain) | LLM abstraction layer & structured output binding |
| [Groq Cloud](https://groq.com/) | Ultra-fast LLM inference (via OpenAI-compatible API) |
| [Pydantic](https://docs.pydantic.dev/) | Schema validation for structured LLM outputs |
| [Python 3.12+](https://www.python.org/) | Runtime |
| [uv](https://github.com/astral-sh/uv) | Fast Python package manager |

---

## 🚀 Quick Start

### Prerequisites

- Python **3.12** or higher
- A [Groq API key](https://console.groq.com/)

### 1 · Clone the repository

```bash
git clone https://github.com/satishmachine/SupportSense-AI.git
cd SupportSense-AI
```

### 2 · Set up the environment

```bash
# Using uv (recommended)
uv venv
uv pip install -r requirements.txt

# Or using pip
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 3 · Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4 · Run the Streamlit app

```bash
streamlit run SupportSense_app.py
```

### 5 · Or run from the command line

```bash
python workflow.py
```

### 6 · Or use the Jupyter notebook

```bash
jupyter notebook 002_Sentiment_review_reply_workflow.ipynb
```

---

## 📋 Example

### Input — Negative Review
```
"I have been trying to log in for over an hour now, & app is keep stucking, really frustrating"
```

### Output — Structured Analysis & Response

```json
{
  "review": "I have been trying to log in for over an hour now, & app is keep stucking, really frustrating",
  "sentiment": "negative",
  "diagnosis": {
    "issue_type": "Bug",
    "tone": "frustrated",
    "urgency": "High"
  },
  "response": "Hi [Name], I'm really sorry you're running into this issue — especially when you need things to work smoothly. I completely understand how frustrating that can be, and I'm here to help get this resolved as quickly as possible..."
}
```

> The system automatically detected this as a **high-urgency bug report** from a **frustrated** user, and generated a professional, empathetic support response with actionable troubleshooting steps.

---

## 📂 Project Structure

```
SupportSense-AI/
├── assets/
│   └── workflow_graph.png              # Auto-generated LangGraph visualization
├── workflow.py                         # Modular workflow engine (importable)
├── SupportSense_app.py                 # Streamlit UI application
├── 002_Sentiment_review_reply_workflow.ipynb  # Original exploration notebook
├── main.py                             # Entry point (placeholder)
├── requirements.txt                    # Python dependencies
├── pyproject.toml                      # Project metadata (uv/pip)
├── .env                                # API keys (not committed)
├── .gitignore                          # Git ignore rules
├── LICENSE                             # MIT License
└── README.md                           # This file
```

---

## 🔮 Roadmap

- [ ] Add **FastAPI** endpoint to expose the workflow as a REST API
- [ ] Support **multi-language** review analysis
- [x] ~~Add a **Streamlit / Gradio** interactive demo UI~~ ✅
- [ ] Integrate **persistent memory** for follow-up conversations
- [ ] Add **batch processing** for analyzing review datasets at scale
- [ ] Deploy to **cloud** (AWS Lambda / GCP Cloud Run)

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/satishmachine">Satish Kumar</a>
</p>
