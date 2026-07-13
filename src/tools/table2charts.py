import json
import os
import sys
from hashlib import md5
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]

def _load_vendor():
    vendor_pkg = REPO_ROOT / "vendor" / "Table2Charts" / "Table2Charts"
    vendor_root = REPO_ROOT / "vendor" / "Table2Charts"

    original_sys_path = list(sys.path)

    try:
        src_root = str(REPO_ROOT / "src")
        filtered = [
            p for p in original_sys_path
            if p != str(REPO_ROOT)
            and not p.startswith(src_root)
        ]
        sys.path = [str(vendor_pkg), str(vendor_root)] + filtered
        from single_inference import pretend_args, single_inference
    finally:
        sys.path = original_sys_path

    return vendor_pkg, pretend_args, single_inference

def _vendor_example_pairs():
    data_root = REPO_ROOT / "vendor" / "Table2Charts" / "Data" / "Example" / "data"
    emb_root = REPO_ROOT / "vendor" / "Table2Charts" / "Data" / "Example" / "embeddings" / "fasttext"

    if not data_root.exists():
        raise RuntimeError(f"Missing Table2Charts example data directory: {data_root}")
    if not emb_root.exists():
        raise RuntimeError(f"Missing Table2Charts example embedding directory: {emb_root}")

    pairs = []
    for df_path in sorted(data_root.glob("*.DF.json")):
        example_id = df_path.name.split(".")[0]
        emb_path = emb_root / f"{example_id}.EMB.json"
        if emb_path.exists():
            pairs.append((df_path, emb_path))

    return pairs

#! since the tool does not provide any function to parse the input data, we will use the vendor example data for testing
def run_table2charts(data_dir: str = "src/data"):
    vendor_pkg, pretend_args, single_inference = _load_vendor()
    setattr(pretend_args, "web_table", True)

    model_path = REPO_ROOT / "vendor" / "Table2Charts" / "Results" / "Models" / "best-excel.pt"

    if not model_path.exists():
        raise RuntimeError(f"Missing Table2Charts model checkpoint: {model_path}")

    args = pretend_args()
    args.model_path = str(model_path)
    args.web_table = True

    original_cwd = Path.cwd()

    try:
        os.chdir(vendor_pkg)
        runner = single_inference(args)

        _ = data_dir  # Kept for API compatibility
        example_pairs = _vendor_example_pairs()

        if not example_pairs:
            raise RuntimeError("No Table2Charts vendor example JSON files were found.")

        for df_path, emb_path in example_pairs:
            example_name = df_path.name.replace(".DF.json", "")

            print(f"Running Table2Charts for vendor example {example_name}...\n")

            output_dir = REPO_ROOT / "outputs" / "table2charts" / (example_name + "_example")
            output_dir.mkdir(parents=True, exist_ok=True)

            try:
                with open(df_path, "r", encoding="utf-8-sig") as f:
                    table_dict = json.load(f)
                with open(emb_path, "r", encoding="utf-8-sig") as f:
                    embedding = json.load(f)

                info = {"table": table_dict, "embeddings": embedding}
                result = runner.inference(info)

                error_log = output_dir / "error.log"
                if error_log.exists():
                    error_log.unlink()

                (output_dir / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str))
            except Exception as e:
                print(f"Table2Charts error processing {example_name} - {e}\n")
    finally:
        os.chdir(original_cwd)

