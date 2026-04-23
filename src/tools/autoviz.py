from pathlib import Path

from autoviz.AutoViz_Class import AutoViz_Class

# will create visualizations for all csv files in the coresponding folders
def run_autoviz(data_dir: str = "src/data"):
	csv_root = Path(data_dir)
	csv_files = sorted(csv_root.glob("*.csv"))

	visualizer = AutoViz_Class()

	for csv_path in csv_files:
		print(f"Running AutoViz for {csv_path}...\n")
        
		output_dir = Path("outputs/autoviz") / csv_path.stem
		output_dir.mkdir(parents=True, exist_ok=True)

		visualizer.AutoViz(
			filename=str(csv_path),
			sep=",",
			depVar="",
			verbose=2,
			chart_format="png",
			save_plot_dir=str(output_dir),
		)
		
