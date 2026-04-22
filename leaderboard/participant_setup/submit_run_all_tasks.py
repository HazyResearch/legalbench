"""This script exemplifies how to call an LLM across 
all LegalBench tasks present in weave. Each task has its own
leaderboard and the for-loop at the bottom iterates over all of them."""

import weave
from weave import Model
import asyncio
import openai
import os
import argparse

TASKS = [
    "abercrombie",
    "sara_numeric",
    "successor_liability",
    "citation_prediction_open",
    "definition_extraction",
    "ssla_company_defendants",
]

def main():
    parser = argparse.ArgumentParser(description='Submit runs for all LegalBench tasks')
    parser.add_argument('--team', default='fuels', type=str, help='Weave team name')
    parser.add_argument('--project', default='legalbench-wandb', type=str, help='Weave project name')
    
    args = parser.parse_args()
    
    WEAVE_TEAM = args.team
    WEAVE_PROJECT = args.project

    client = weave.init(f"{WEAVE_TEAM}/{WEAVE_PROJECT}")

    """In the following, two sample models are set up to evaluate a few
    well-known closed and open-source LLMs on all of the tasks
    in the TASKS list (note: 'model' in the context of weave does not mean
    the raw LLM, but a class that configures a run on a given evaluation;
    LLM calls are made from within the predict() method of the class to generate
    predictions. The user should replace the following section with
    their own custom model (=class)."""

    # Set up OpenAI client (GPT‑4o‑mini)
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # set up Together
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

    together_client = openai.OpenAI(
        api_key=TOGETHER_API_KEY,
        base_url="https://api.together.xyz",
    )

    TOGETHER_MODELS = [
        "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "meta-llama/Llama-4-Scout-17B-16E-Instruct",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "Qwen/Qwen2.5-7B-Instruct-Turbo",
        "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    ]
    # ───────────────────────────────────────────────────────────────────────────────

    class MyModel5(Model):
        """GPT‑4o‑mini wrapper (unchanged)."""

        prompt: str

        def generate_prompt(self, template: str, data: dict) -> str:
            prompt = template
            for key, value in data.items():
                placeholder = f"{{{{{key}}}}}"
                prompt = prompt.replace(placeholder, str(value))
            return prompt

        @weave.op()
        def predict(self, data: dict | None):
            prompt_for_model = self.generate_prompt(self.prompt, data)

            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_for_model}],
                max_tokens=1000,
                temperature=0.0,
            )
            generated_text = response.choices[0].message.content
            return {"generation": generated_text}


    class MyTogetherModel(Model):
        """Minimal Together AI wrapper – shares the same prompt logic."""

        prompt: str
        model_name: str  # full Together model id

        def generate_prompt(self, template: str, data: dict) -> str:
            prompt = template
            for key, value in (data or {}).items():
                placeholder = f"{{{{{key}}}}}"
                prompt = prompt.replace(placeholder, str(value))
            return prompt

        @weave.op()
        def predict(self, data: dict | None):
            prompt_for_model = self.generate_prompt(self.prompt, data)

            response = together_client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt_for_model}],
                max_tokens=1000,
                temperature=0.0,
            )
            generated_text = response.choices[0].message.content
            return {"generation": generated_text}


    for task in TASKS:
        with open(f"tasks/{task}/base_prompt.txt") as in_file:
            prompt_template = in_file.read()

        eval = weave.ref(f"{task}_evaluation").get()

        # Evaluate GPT‑4o‑mini
        model = MyModel5(name="gpt-4o-mini_base-prompt", prompt=prompt_template)
        asyncio.run(eval.evaluate(model))

        # Evaluate the five Together models
        for together_id in TOGETHER_MODELS:
            together_model = MyTogetherModel(
                name=f"{together_id.split('/')[-1]}_base-prompt",
                prompt=prompt_template,
                model_name=together_id,
            )
            asyncio.run(eval.evaluate(together_model))

if __name__ == "__main__":
    main()

# invoke via python -m leaderboard.participant_setup.submit_run_all_tasks --team <name of weave team> --project <name of weave project>
