import os
import sys
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

def run_llm4vis(data_dir: str = "src/data"):
    vendor_path = str(REPO_ROOT / "vendor" / "LLM4Vis")
    if vendor_path not in sys.path:
        sys.path.insert(0, vendor_path)

    import prompts
    import utils

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY")

    utils.openai.api_key = api_key
    utils.openai.api_base = (
        os.getenv("OPENAI_BASE_URL")
        or "https://api.openai.com/v1"
    )

    model = "gpt-4o-mini"

    for csv_path in sorted(Path(data_dir).glob("*.csv")):
        print(f"Running LLM4Vis for {csv_path}...\n")

        output_dir = Path("outputs/llm4vis") / csv_path.stem
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            df = pd.read_csv(csv_path)
            feature_dict = df.describe(include="all").fillna("").to_dict()

            # generate dataset description (feature_summary.py flow)
            description = utils.openai.ChatCompletion.create(
                model=model,
                temperature=0,
                messages=[
                    {"role": "system", "content": prompts.role_str_sum},
                    {"role": "user", "content": prompts.template_icl_sum.format(feature_dict)},
                ],
            )["choices"][0]["message"]["content"]

            # recommend visualization type (final_run.py flow)
            response = utils.openai.ChatCompletion.create(
                model=model,
                temperature=0,
                messages=[
                    {"role": "system", "content": prompts.role_str_demo_prepare},
                    {"role": "user", "content": prompts.demos_descri_x.format(description)},
                ],
            )["choices"][0]["message"]["content"]

            # save the final stage output text
            (output_dir / f"{csv_path.stem}.txt").write_text(response)

        except Exception as e:
            print(f"LLM4Vis error processing {csv_path.name} - {e}\n")
