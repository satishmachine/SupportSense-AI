"""
SupportSense-AI — Sentiment Review Reply Workflow
===================================================

A modular LangGraph workflow that analyzes customer reviews,
detects sentiment, diagnoses issues, and generates contextual
support responses.
"""

import os
from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

# ──────────────────────────────────────────────
# 1. Environment
# ──────────────────────────────────────────────
load_dotenv()


# ──────────────────────────────────────────────
# 2. LLM Configuration
# ──────────────────────────────────────────────
def get_groq_llm(
    model: str = "openai/gpt-oss-120b",
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> ChatOpenAI:
    """Return a ChatOpenAI instance configured for the Groq Cloud API."""
    return ChatOpenAI(
        model=model,
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
        max_tokens=max_tokens,
    )


# ──────────────────────────────────────────────
# 3. Pydantic Schemas (Structured LLM Output)
# ──────────────────────────────────────────────
class SentimentSchema(BaseModel):
    """Schema enforcing binary sentiment classification."""

    sentiment: Literal["positive", "negative"] = Field(
        description="Sentiment of the review"
    )


class DiagnosisSchema(BaseModel):
    """Schema for multi-dimensional issue diagnosis on negative reviews."""

    issue_type: Literal["UX/UI", "Performance", "Bug", "Support", "Other"] = Field(
        description="The category of issue mentioned in the review"
    )
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(
        description="The emotional tone expressed by the user in the review"
    )
    urgency: Literal["low", "Medium", "High"] = Field(
        description="How urgent or critical the issue appears to be"
    )


# ──────────────────────────────────────────────
# 4. Shared State
# ──────────────────────────────────────────────
class ReviewState(TypedDict):
    """Shared state schema passed between graph nodes."""

    review: str
    sentiment: str
    diagnosis: dict
    response: str


# ──────────────────────────────────────────────
# 5. Graph Nodes
# ──────────────────────────────────────────────
def find_sentiment(state: ReviewState) -> dict:
    """Classify the review sentiment as positive or negative."""
    llm = get_groq_llm()
    structured_model = llm.with_structured_output(SentimentSchema)
    prompt = f"For the following review, find out the sentiment: {state['review']}"
    result = structured_model.invoke(prompt)
    return {"sentiment": result.sentiment}


def check_sentiment(state: ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    """Route to the appropriate branch based on detected sentiment."""
    if state["sentiment"] == "positive":
        return "positive_response"
    return "run_diagnosis"


def positive_response(state: ReviewState) -> dict:
    """Generate a warm thank-you message for a positive review."""
    llm = get_groq_llm()
    prompt = (
        f"Write a warm thank you message in your response "
        f"based on the review of the user: {state['review']}"
    )
    response = llm.invoke(prompt).content
    return {"response": response}


def run_diagnosis(state: ReviewState) -> dict:
    """Diagnose a negative review across issue_type, tone, and urgency."""
    llm = get_groq_llm()
    structured_model = llm.with_structured_output(DiagnosisSchema)
    prompt = f"Diagnose this negative review:\n{state['review']}"
    result = structured_model.invoke(prompt)
    return {"diagnosis": result.model_dump()}


def negative_response(state: ReviewState) -> dict:
    """Craft an empathetic, actionable support reply using diagnosis context."""
    llm = get_groq_llm()
    diagnosis = state["diagnosis"]
    prompt = (
        f"You are a support assistant. The user had a {diagnosis['issue_type']} issue "
        f"and sounded {diagnosis['tone']} and marked urgency as: {diagnosis['urgency']}. "
        f"Write an empathetic helpful response message."
    )
    response = llm.invoke(prompt).content
    return {"response": response}


# ──────────────────────────────────────────────
# 6. Graph Builder
# ──────────────────────────────────────────────
def build_workflow() -> StateGraph:
    """Construct and compile the SupportSense-AI LangGraph workflow.

    Returns
    -------
    compiled : CompiledStateGraph
        A compiled graph ready to be invoked with ``workflow.invoke(state)``.
    """
    graph = StateGraph(ReviewState)

    # Nodes
    graph.add_node("find_sentiment", find_sentiment)
    graph.add_node("positive_response", positive_response)
    graph.add_node("run_diagnosis", run_diagnosis)
    graph.add_node("negative_response", negative_response)

    # Edges
    graph.add_edge(START, "find_sentiment")
    graph.add_conditional_edges("find_sentiment", check_sentiment)
    graph.add_edge("positive_response", END)
    graph.add_edge("run_diagnosis", "negative_response")
    graph.add_edge("negative_response", END)

    return graph.compile()


# ──────────────────────────────────────────────
# 7. Convenience Runner
# ──────────────────────────────────────────────
def analyze_review(review_text: str) -> dict:
    """End-to-end helper: build the workflow, invoke it, and return the final state.

    Parameters
    ----------
    review_text : str
        The raw customer review to analyze.

    Returns
    -------
    dict
        Final state containing ``review``, ``sentiment``,
        ``diagnosis`` (if negative), and ``response``.
    """
    workflow = build_workflow()
    initial_state: ReviewState = {"review": review_text}
    return workflow.invoke(initial_state)


# ──────────────────────────────────────────────
# 8. CLI Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    sample = (
        "I have been trying to log in for over an hour now, "
        "& app is keep stucking, really frustrating"
    )
    result = analyze_review(sample)
    print("\n── SupportSense-AI Result ──")
    print(f"  Review    : {result['review']}")
    print(f"  Sentiment : {result['sentiment']}")
    if result.get("diagnosis"):
        print(f"  Diagnosis : {result['diagnosis']}")
    print(f"  Response  :\n{result['response']}")
