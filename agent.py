import joblib
import pandas as pd
import numpy as np
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import yfinance as yf
import json
from . import prompt

# Load the trained model
from google import genai
from google.genai import types
import base64

# Model for prediction of triage disposition
client = genai.Client(
      vertexai=True,
      project="virtual-nurse-450613",
      location="global",
  )

si_text1 = """You are a helpful doctor who will predict triage deposition and notes for clinical plan based on patient's information.
The disposition should be one of the following categories: 
- Home Care (self care)
- See within 6-8 weeks in office
- See this week in office
- Go to the hospital/urgent care if not better within 24 hours
- Go to the ED Now (by car)
- Call Emergency Medical Services now
You should always print out the deposition with confidence score."""

model = "gemini-2.5-pro"

tools = [
    types.Tool(
      retrieval=types.Retrieval(
        vertex_rag_store=types.VertexRagStore(
          rag_resources=[
            types.VertexRagStoreRagResource(
              rag_corpus="projects/virtual-nurse-450613/locations/us-central1/ragCorpora/7991637538768945152"
            )
          ],
        )
      )
    )
  ]

generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    seed = 0,
    max_output_tokens = 65535,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    tools = tools,
    system_instruction=[types.Part.from_text(text=si_text1)],
    thinking_config=types.ThinkingConfig(
      thinking_budget=-1,
    ),
  )


def predict_triage(patient_summary: str):
    """
    Predict triage disposition and notes for clinical plan based on patient summary.
    
    Parameters:
    -----------
    patient_summary : str
        Text containing patient summary
        
    Returns:
    --------
    str
        Text containing triage disposition and notes for clinical plan prediction.
    """

    msg1_text1 = types.Part.from_text(text=patient_summary)

    # Make prediction
    contents = [
    types.Content(
      role="user",
      parts=[
        msg1_text1
      ]
    ),
    ]

    response = client.models.generate_content(
    model = model,
    contents = contents,
    config = generate_content_config,
    )
    return response.text

root_agent = Agent(
    model='gemini-2.5-pro',
    name='triage_agent',
    description='An agent that predicts triage disposition for tonsillectomy patients.',
    instruction=prompt.VIRTUAL_ASSISTANT_PROMPT,
    tools=[predict_triage]
)

""" app = AdkApp(agent=root_agent)

for event in app.stream_query(
    user_id="USER_ID",
    message="Patient is bleeding and has a fever",
):
    print(event) """