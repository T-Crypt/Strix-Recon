#!/usr/bin/env python3
"""
Strix Recon Agent main.py
Loads config, initializes LLM client (Ollama-aware), and starts ReconExecutor.
"""

import os
import sys
from agent.utils.config import load_config
from agent.workflow.executor import ReconExecutor
from agent.llm.llm_client import LLMClient

def print_banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(r"""
 STRIX | LLM-based Autonomous Recon Agent ⚡
""")

def get_env_provider_and_host(config):
    provider = os.environ.get("LLM_BACKEND", config.get("llm", {}).get("provider", "ollama")).lower()
    host = os.environ.get("OLLAMA_URL", config.get("ollama", {}).get("host", "http://localhost:11434"))
    return provider, host

def parse_args():
    if len(sys.argv) < 2:
        print("Usage: main.py <target> [steps] [interactive] [target_mode]")
        sys.exit(1)
    target = sys.argv[1]
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    interactive = bool(int(sys.argv[3])) if len(sys.argv) > 3 else False
    target_mode = sys.argv[4] if len(sys.argv) > 4 else "host"
    return target, steps, interactive, target_mode

def main():
    print_banner()
    config = load_config()
    provider, ollama_host = get_env_provider_and_host(config)

    api_key = None if provider == "ollama" else (
        config.get("llm", {}).get("api_key") or os.environ.get("LLM_API_KEY")
    )

    print(f"[*] Using provider: {provider}")
    print(f"[*] Ollama Host: {ollama_host}")
    if api_key:
        print("[*] API Key detected (hidden)")

    llm_client = LLMClient(
        api_key=api_key,
        provider=provider,
        model=config.get("llm", {}).get("model", "llama2"),
        ollama_host=ollama_host,
        context_length=config.get("llm", {}).get("context_length", 8192),
    )

    target, steps, interactive, target_mode = parse_args()
    executor = ReconExecutor(llm_client, target, interactive, target_mode)
    executor.workflow(steps)

if __name__ == "__main__":
    main()
