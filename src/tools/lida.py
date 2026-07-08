import base64
import json
import os
from pathlib import Path

import pandas as pd
from lida import Manager, TextGenerationConfig, llm

def _build_custom_lida_manager():
	base_url = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
	api_key = os.getenv("VLLM_API_KEY", "EMPTY")
	model_name = os.getenv("LIDA_MODEL", "granite-3.2-8b-instruct-Q4_K_M")
	
	os.environ["OPENAI_BASE_URL"] = base_url

	manager = Manager(text_gen=llm("openai", api_key=api_key, model=model_name))
	textgen_config = TextGenerationConfig(model=model_name, temperature=0, top_p=1)

	return manager, textgen_config

def _build_chatgpt_lida_manager():
	api_key = os.getenv("OPENAI_API_KEY")

	if not api_key:
		raise ValueError("OPENAI_API_KEY is required for using ChatGPT!")

	manager = Manager(text_gen=llm("openai", api_key=api_key))
	textgen_config = TextGenerationConfig(temperature=0, top_p=1)

	return manager, textgen_config

def _write_chart_outputs(chart, output_dir: Path, prefix: str):
	if getattr(chart, "spec", None) is not None:
		spec_path = output_dir / f"{prefix}_spec.json"
		spec_path.write_text(json.dumps(chart.spec, indent=2) if not isinstance(chart.spec, str) else chart.spec)

	if getattr(chart, "code", None):
		code_path = output_dir / f"{prefix}_code.py"
		code_path.write_text(chart.code)

	raster = getattr(chart, "raster", None)
	if raster:
		png_path = output_dir / f"{prefix}.png"
		payload = raster.split(",", 1)[1] if isinstance(raster, str) and "," in raster else raster
		try:
			png_path.write_bytes(base64.b64decode(payload))
		except Exception:
			png_path.write_text(str(raster))

def run_lida(data_dir: str = "src/data", n_goals: int = 3, backend: str = "custom"):
	csv_root = Path(data_dir)
	csv_files = sorted(csv_root.glob("*.csv"))
	if not csv_files:
		print(f"No CSV files found in {csv_root}\n")
		return

	selected_backend = backend.lower()
	if selected_backend == "custom":
		manager, textgen_config = _build_custom_lida_manager()
	elif selected_backend == "chatgpt":
		manager, textgen_config = _build_chatgpt_lida_manager()
	else:
		raise ValueError("backend must be either 'custom' or 'chatgpt'")

	for csv_path in csv_files:
		print(f"Running LIDA for {csv_path}...\n")

		output_dir = Path("outputs/lida") / csv_path.stem
		output_dir.mkdir(parents=True, exist_ok=True)

		try:
			df = pd.read_csv(csv_path)
			# df.drop(columns=['index', 'test_index', 'run_index', 'build'], inplace=True)
			summary = manager.summarize(
				df,
				file_name=csv_path.name,
				summary_method="default",
				textgen_config=textgen_config,
			)
			goals = manager.goals(
				summary,
				n=n_goals,
				persona="You are a data analyst focused on generating visualizations",
				textgen_config=textgen_config,
			)

			for idx, goal in enumerate(goals):
				charts = manager.visualize(
					summary=summary,
					goal=goal,
					library="seaborn",
					textgen_config=textgen_config,
				)

				for chart_idx, chart in enumerate(charts):
					prefix = f"goal_{idx}_chart_{chart_idx}"
					_write_chart_outputs(chart, output_dir, prefix)
		except Exception as e:
			print(f"LIDA error processing {csv_path.name} - {e}\n")
