import requests

class LLMClient:
    def __init__(self, api_key=None, provider="ollama", model="llama2",
                 ollama_host="http://localhost:11434", context_length=8192):
        self.api_key = api_key
        self.provider = provider.lower()
        self.model = model
        self.ollama_host = ollama_host
        self.context_length = context_length

    def query(self, prompt):
        print(f"[LLM] Querying {self.provider} ({self.model}) with prompt: {prompt[:50]}...")

        if self.provider == "ollama":
            try:
                response = requests.post(
                    f"{self.ollama_host}/api/generate",
                    json={"model": self.model, "prompt": prompt},
                    timeout=60
                )
                return response.json().get("response", "No response")
            except Exception as e:
                return f"[Error: Ollama connection failed: {e}]"

        elif self.provider == "openai":
            # Placeholder for remote API mode
            return "Remote LLM response (OpenAI mock)"

        return "mock response"
