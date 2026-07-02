import json
from pathlib import Path

import draco
import pandas as pd
import vl_convert as vlc

def _to_records(csv_path: Path):
	df = pd.read_csv(csv_path)

	records = []
	for row in df.to_dict(orient="records"):
		cleaned = {}
		for key, value in row.items():
			if pd.isna(value):
				cleaned[key] = None
			else:
				cleaned[key] = value
		records.append(cleaned)

	return records

def run_draco(data_dir: str = "src/data"):
	csv_root = Path(data_dir)
	csv_files = sorted(csv_root.glob("*.csv"))

	for csv_path in csv_files:
		print(f"Running Draco for {csv_path}...\n")

		output_dir = Path("outputs/draco") / csv_path.stem
		output_dir.mkdir(parents=True, exist_ok=True)

		try:
			records = _to_records(csv_path)
			base_query = draco.data_to_asp(records)
			result = draco.run(base_query, silence_warnings=True)
		except Exception as e:
			print(f"Draco could not parse {csv_path.name} - {e}\n")
			continue

		if result is None:
			print(f"No Draco recommendations generated for {csv_path.name}\n")
		else:
			spec = result.as_vl()
			spec["data"] = {"values": records}

			spec_path = output_dir / "spec.json"
			spec_path.write_text(json.dumps(spec, indent=2))

			png_path = output_dir / "viz.png"
			png_data = vlc.vegalite_to_png(vl_spec=spec, scale=2)
			png_path.write_bytes(png_data)
