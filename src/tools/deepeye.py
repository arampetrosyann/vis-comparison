import sys
import os
from pathlib import Path

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
deepeye_local = os.path.join(repo_root, 'vendor', 'DeepEye')

if os.path.isdir(deepeye_local):
    if deepeye_local not in sys.path:
        sys.path.insert(0, deepeye_local)

def run_deepeye(data_dir: str = "src/data", method: str = "diversified_ranking"):
    try:
        import deepeye_pack
    except ImportError as e:
        print(f"Could not import DeepEye!!! - {e}\n")
        return
    
    csv_root = Path(data_dir)
    csv_files = sorted(csv_root.glob("*.csv"))

    for csv_path in csv_files:
        print(f"Running DeepEye for {csv_path}...\n")

        try:
            dp = deepeye_pack.deepeye(csv_path.stem)

            dp.from_csv(str(csv_path))
            
            # Apply ranking method
            if method == "partial_order":
                dp.partial_order()
            elif method == "learning_to_rank":
                dp.learning_to_rank()
            elif method == "diversified_ranking":
                dp.diversified_ranking()
            else:
                raise ValueError(f"Unknown method - {method}")
            
            output_dir = Path("outputs/deepeye") / csv_path.stem
            output_dir.mkdir(parents=True, exist_ok=True)

            original_cwd = Path.cwd()
            try:
                os.chdir(output_dir)
                dp.to_single_html()
            finally:
                os.chdir(original_cwd)
        except Exception as e:
            print(f"DeepEye error processing {csv_path.name} - {e}\n")
            continue
