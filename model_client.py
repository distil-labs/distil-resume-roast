import json
from openai import OpenAI

# --- CONFIGURATION ---
SYSTEM_PROMPT = """
## Task
Generate a brutally honest 'roast' critique of the provided resume.

## Output Format (Strict JSON)
You must output a valid JSON object matching this exact structure:
{
    "roast_critique": "A mean, sarcastic paragraph here.",
    "professional_suggestions": [
        "Actionable tip 1",
        "Actionable tip 2",
        "Actionable tip 3"
    ],
    "rating": 5
}

## Rules
1. The "rating" field must be an INTEGER (e.g., 7), not a string.
2. Do NOT put the rating inside the suggestions list.
3. Return ONLY valid JSON.
"""

class DistilLabsLLM:
    def __init__(self, model_name: str, port: int = 11434):
        self.model_name = model_name
        # Standard Pattern: Use OpenAI Client to talk to Ollama
        self.client = OpenAI(
            base_url=f"http://127.0.0.1:{port}/v1",
            api_key="EMPTY"
        )

    def get_prompt(self, resume_text: str) -> list[dict[str, str]]:
        """Constructs the standard chat messages list."""
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{resume_text}"}
        ]

    def invoke(self, resume_text: str) -> str:
        """Sends the request and returns the raw string content."""
        messages = self.get_prompt(resume_text)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.8, 
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Model invocation failed: {e}")