import yaml
import os

def load_config(path="configs/config.yaml"):
    config = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.safe_load(f) or {}

    # Merge environment overrides
    env_overrides = {
        "llm": {
            "provider": os.environ.get("LLM_BACKEND", config.get("llm", {}).get("provider", "ollama")),
            "api_key": os.environ.get("LLM_API_KEY", config.get("llm", {}).get("api_key")),
            "model": os.environ.get("LLM_MODEL", config.get("llm", {}).get("model", "llama2")),
            "base_url": os.environ.get("LLM_BASE_URL", config.get("llm", {}).get("base_url")),
            "context_length": int(os.environ.get("LLM_CONTEXT_LEN", config.get("llm", {}).get("context_length", 8192))),
        },
        "ollama": {
            "host": os.environ.get("OLLAMA_URL", config.get("ollama", {}).get("host", "http://localhost:11434"))
        }
    }

    return env_overrides
