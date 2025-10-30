# agent/workflow/executor.py
class ReconExecutor:
    def __init__(self, llm_client, target, interactive=False, target_mode="host"):
        self.llm = llm_client
        self.target = target
        self.interactive = interactive
        self.target_mode = target_mode

    def workflow(self, steps=3):
        print(f"Running recon workflow on {self.target} in {self.target_mode} mode for {steps} steps...")
        for step in range(1, steps + 1):
            prompt = f"Step {step} analysis for {self.target}"
            if self.interactive:
                prompt += " (interactive mode)"
            response = self.llm.query(prompt)
            print(f"Step {step}: {response}")

