import os
from google import genai
from google.genai import types

def get_client():
    api_key = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY", "dummy")
    base_url = os.environ.get("AI_INTEGRATIONS_GEMINI_BASE_URL")

    if base_url:
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(base_url=base_url, api_version="")
        )
    else:
        client = genai.Client(api_key=api_key)

    return client

def call_llm(prompt: str, temperature: float = 0.4) -> str:
    client = get_client()
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=8192,
        )
    )
    return response.text or ""

def classify_task(user_input: str) -> str:
    from utils.prompts import CLASSIFIER_PROMPT
    prompt = CLASSIFIER_PROMPT.format(user_input=user_input)
    result = call_llm(prompt, temperature=0.1).strip().lower()
    valid_tasks = {"summarize", "explain", "compare", "evaluate"}
    if result not in valid_tasks:
        return "summarize"
    return result
