import importlib.util
from pathlib import Path
import pkgutil
import lux
import pandas as pd
import vl_convert as vlc

if not hasattr(pkgutil, "find_loader"):
	def _find_loader(name: str):
		spec = importlib.util.find_spec(name)
		if spec is None:
			return None
		return spec.loader

	pkgutil.find_loader = _find_loader

# you can indicate that you are interested in some attributes - df.intent = ['AverageCost']

def run_lux(data_dir: str = "src/data"):
	csv_root = Path(data_dir)
	csv_files = sorted(csv_root.glob("*.csv"))

	for csv_path in csv_files:
		print(f"Running Lux for {csv_path}...\n")

		output_dir = Path("outputs/lux") / csv_path.stem
		output_dir.mkdir(parents=True, exist_ok=True)

		try:
			df = pd.read_csv(csv_path)
			ldf = lux.LuxDataFrame(df)

			# set intent
			excluded_cols = {"index", "build", "test_index", "run_index"}
			candidate_cols = [col for col in ldf.columns if col.lower() not in excluded_cols]

			if (ldf.columns.str.startswith("y")).any():
				y_cols = [col for col in candidate_cols if col.lower().startswith("y")]
				other_cols = [col.title() for col in candidate_cols if col not in y_cols]

				ldf.intent = [other_cols] + [col.title() for col in y_cols]	
			else:
				ldf.intent = [col.title() for col in candidate_cols]

			print("intent - ", ldf.intent, "\n")

			# force recommendation generation outside notebook display context
			if hasattr(ldf, "maintain_recs"):
				ldf.maintain_recs()

			recommendations = getattr(ldf, "recommendation", None)

			if recommendations is None:
				print(f"No recommendations generated for {csv_path.name}!!!\n")
				continue

			for action_name, vis_list in recommendations.items():
				action_dir = output_dir / action_name
				action_dir.mkdir(parents=True, exist_ok=True)

				for idx, vis in enumerate(list(vis_list)[:5]): # limit to top 5 recommendations per action
					try:
						spec = vis.to_vegalite(prettyOutput=False)
						chart_path = action_dir / f"rec_{idx}.png"

						png_data = vlc.vegalite_to_png(vl_spec=spec, scale=2)
						chart_path.write_bytes(png_data)
					except Exception as vis_error:
						print(vis_error)
		except Exception as e:
			print(f"Lux error processing {csv_path.name} - {e}\n")
			

