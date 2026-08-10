import json
from pathlib import Path
import re

import altair as alt
import draco
from draco.renderer import AltairRenderer
import pandas as pd
import vl_convert as vlc

def _sanitize_field_name(name: str) -> str:
	"""Convert a column name into a Draco-safe identifier."""
	safe = re.sub(r"[^0-9a-zA-Z_]", "_", str(name))
	if not safe:
		safe = "field"
	if safe[0].isdigit():
		safe = f"f_{safe}"
	return safe

def _rename_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
	"""Rename dataframe columns in place to Draco-safe identifiers."""
	raw_columns = [str(col) for col in df.columns]
	sanitized = []
	counts = {}

	for col in raw_columns:
		base = _sanitize_field_name(col)
		idx = counts.get(base, 0)
		counts[base] = idx + 1
		sanitized.append(base if idx == 0 else f"{base}_{idx}")

	df.columns = sanitized
	return df

def run_draco(data_dir: str = "src/data", top_k: int = 3):
	# Keep full datasets inlined in Vega-Lite output for PDF export.
	alt.data_transformers.disable_max_rows()

	csv_root = Path(data_dir)
	csv_files = sorted(csv_root.glob("*.csv"))
	renderer = AltairRenderer()
	draco_solver = draco.Draco()

	for csv_path in csv_files:
		print(f"Running Draco for {csv_path}...\n")

		output_dir = Path("outputs/draco") / csv_path.stem
		output_dir.mkdir(parents=True, exist_ok=True)

		try:
			df = pd.read_csv(csv_path)
			df = _rename_dataframe_columns(df)
			schema = draco.schema_from_dataframe(df)

			partial_spec = {
				**schema,
				"view": [
					{
						"mark": [
							{
								"encoding": [
									{"channel": "x"},
									{"channel": "y"},
								]
							}
						]
					}
				],
			}
			
			facts = draco.dict_to_facts(partial_spec)
			models = list(draco_solver.complete_spec(facts, models=top_k))
		except Exception as e:
			print(f"Draco could not parse {csv_path.name} - {e}\n")
			continue

		if not models:
			print(f"No Draco recommendations generated for {csv_path.name}\n")
			continue

		rank_summary = []
		for rank, model in enumerate(models, start=1):
			try:
				spec_dict = draco.answer_set_to_dict(model.answer_set)
				vl_spec = renderer.render(spec_dict, df).to_dict()

				spec_path = output_dir / f"rank-{rank:02d}-spec.json"
				spec_path.write_text(json.dumps(vl_spec, indent=2))

				pdf_path = output_dir / f"rank-{rank:02d}-viz.pdf"
				pdf_data = vlc.vegalite_to_pdf(vl_spec=vl_spec)
				pdf_path.write_bytes(pdf_data)

				rank_summary.append(f"#{rank}(cost={model.cost})")
			except Exception as e:
				print(f"Draco export failed for {csv_path.name} rank {rank} - {e}\n")

		if rank_summary:
			print(
				f"Saved {len(rank_summary)} ranked visualizations for {csv_path.name}: "
				+ ", ".join(rank_summary)
				+ "\n"
			)
		else:
			print(f"No exportable Draco visualizations for {csv_path.name}\n")
