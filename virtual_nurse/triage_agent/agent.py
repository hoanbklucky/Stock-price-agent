"""triage_agent for predicting deposition and notes for clinical plan"""

from google.adk import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

from . import prompt

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        "Use this tool to predict deposition and notes for clinical plan based on patient's information."
    ),
    rag_resources=[
        rag.RagResource(
            # please fill in your own rag corpus
            # here is a sample rag corpus for testing purpose
            # e.g. projects/123/locations/us-central1/ragCorpora/456
            rag_corpus="projects/virtual-nurse-450613/locations/us-central1/ragCorpora/7991637538768945152"
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

MODEL = "gemini-2.5-pro"

triage_agent = Agent(
    model=MODEL,
    name="triage_agent",
    instruction=prompt.TRIAGE_PROMPT,
    tools=[ask_vertex_retrieval]
)