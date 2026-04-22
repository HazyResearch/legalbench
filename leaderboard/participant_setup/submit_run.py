# This script exemplifies how to call an LLM on a single LegalBench task.

import weave
from weave import Model
import asyncio
import argparse

def main():
    parser = argparse.ArgumentParser(description='Submit a run for a single LegalBench task')
    parser.add_argument('--task', type=str, help='Task name')
    parser.add_argument('--team', default='fuels', type=str, help='Weave team name')
    parser.add_argument('--project', default='legalbench-wandb', type=str, help='Weave project name')
    parser.add_argument('--model_name', type=str, help='Name you would like to show up on the leaderboard')
    
    args = parser.parse_args()
    
    TASK = args.task
    WEAVE_TEAM = args.team
    WEAVE_PROJECT = args.project

    client = weave.init(f"{WEAVE_TEAM}/{WEAVE_PROJECT}")

    dataset = weave.ref(f"{TASK}_test").get()

    class MyModel(Model):
        prompt_template: str

        @weave.op()
        def predict(self, text: str):
            prompt_template = self.prompt_template

            prompt = prompt_template.replace("{{text}}", text)
            
            return {'generation': prompt}

    # Load base prompt
    with open(f"tasks/{TASK}/base_prompt.txt") as in_file:
        prompt_template = in_file.read()

    model = MyModel(prompt_template=prompt_template, name=args.model_name)

    eval = weave.ref(f"{TASK}_evaluation").get()

    asyncio.run(eval.evaluate(model))

if __name__ == "__main__":
    main()

# invoke via python -m leaderboard.participant_setup.submit_run --task <task name> --team <name of weave team> --project <name of weave project>
