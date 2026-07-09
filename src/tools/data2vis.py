import ast
import json
import os
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List
import pandas as pd
import vl_convert as vlc

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA2VIS_ROOT = REPO_ROOT / "vendor" / "data2vis"
DATA2VIS_MODEL_DIR = DATA2VIS_ROOT / "vizmodel"
DATA2VIS_VENV_DIR = REPO_ROOT / ".venv"
DATA2VIS_PYTHON = Path(
    os.environ.get("DATA2VIS_PYTHON", str(DATA2VIS_VENV_DIR / "bin" / "python"))
)
DATA2VIS_UTILS_FILE = DATA2VIS_ROOT / "utils" / "data_utils.py"
_DATA_UTILS_MODULE: ModuleType = None

def _load_data_utils() -> ModuleType:
    global _DATA_UTILS_MODULE
    if _DATA_UTILS_MODULE is not None:
        return _DATA_UTILS_MODULE

    if not DATA2VIS_UTILS_FILE.exists():
        raise RuntimeError(f"Data2Vis utilities not found at {DATA2VIS_UTILS_FILE}")

    spec = spec_from_file_location("data2vis_data_utils", DATA2VIS_UTILS_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Data2Vis utility module spec")

    previous_cwd = Path.cwd()
    previous_sys_path = list(sys.path)
    try:
        os.chdir(DATA2VIS_ROOT)
        sys.path.insert(0, str(DATA2VIS_ROOT))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        os.chdir(previous_cwd)
        sys.path = previous_sys_path

    _DATA_UTILS_MODULE = module
    return module

def _generate_field_types(records: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    data_utils = _load_data_utils()
    return data_utils.generate_field_types(records)

def _forward_norm(records: List[Dict[str, Any]], out_file: Path, field_types: List[Dict[str, str]]) -> bool:
    data_utils = _load_data_utils()
    try:
        normalized_source = data_utils.replace_fieldnames(
            json.dumps(records), field_types, True
        )
        normalized_json = json.loads(normalized_source)
        data_utils.write_data_to_file(str(out_file), normalized_json)
        return True
    except Exception:
        return False

def _backward_norm(text: str, field_types: List[Dict[str, str]]) -> str:
    data_utils = _load_data_utils()
    return data_utils.backward_norm(text, field_types)

def _extract_first_json(value: str):
    text = (value or "").strip()
    if not text:
        return None

    try:
        return json.loads(text)
    except Exception:
        pass

    try:
        return ast.literal_eval(text)
    except Exception:
        pass

    json_start = text.find("[")
    json_end = text.rfind("]")
    if json_start != -1 and json_end != -1 and json_end > json_start:
        candidate = text[json_start:json_end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            try:
                return ast.literal_eval(candidate)
            except Exception:
                return None

    return None

def _valid_vegalite_spec(spec: Any) -> bool:
    return isinstance(spec, dict) and "mark" in spec and "encoding" in spec

def _inject_data(spec: Dict[str, Any], records: List[Dict[str, Any]]) -> Dict[str, Any]:
    out = json.loads(json.dumps(spec))
    out["$schema"] = out.get("$schema", "https://vega.github.io/schema/vega-lite/v5.json")
    out["data"] = {"values": records}
    return out

def _ensure_data2vis_runtime() -> None:
    if not DATA2VIS_PYTHON.exists():
        raise RuntimeError(
            "Data2Vis runtime is missing. Set DATA2VIS_PYTHON or run setup_data2vis_model_env.sh"
        )

    check_cmd = [str(DATA2VIS_PYTHON), "-c", "import tensorflow"]
    check_proc = subprocess.run(check_cmd, capture_output=True, text=True, check=False)
    if check_proc.returncode != 0:
        stderr = (check_proc.stderr or "").strip()
        raise RuntimeError(
            "TensorFlow is not available. "
            f"Details: {stderr or 'import tensorflow failed'}"
        )

def _run_data2vis_model(records: List[Dict[str, Any]], output_dir: Path) -> List[Dict[str, Any]]:
    if not DATA2VIS_ROOT.exists() or not DATA2VIS_MODEL_DIR.exists():
        raise RuntimeError("Data2Vis vendor repo or model directory is missing.")

    _ensure_data2vis_runtime()

    input_path = output_dir / "model_input.sources"
    predictions_path = output_dir / "model_predictions_raw.txt"

    field_types = _generate_field_types(records)
    if not _forward_norm(records, input_path, field_types):
        raise RuntimeError("Data2Vis forward normalization failed")

    infer_cmd = [
        str(DATA2VIS_PYTHON),
        "-m",
        "bin.infer",
        "--tasks",
        "- class: DecodeText\n  params:\n    delimiter: ''",
        "--model_dir",
        str(DATA2VIS_MODEL_DIR),
        "--model_params",
        "inference.beam_search.beam_width: 3",
        "--input_pipeline",
        "class: ParallelTextInputPipeline\nparams:\n  source_delimiter: ''\n  target_delimiter: ''\n  source_files:\n    - " + str(input_path),
    ]

    proc = subprocess.run(
        infer_cmd,
        cwd=DATA2VIS_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    combined_output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    predictions_path.write_text(combined_output)

    if proc.returncode != 0:
        raise RuntimeError(
            "Data2Vis inference failed. See model_predictions_raw.txt for details."
        )

    parsed = _extract_first_json(proc.stdout)
    if parsed is None:
        parsed = _extract_first_json(combined_output)

    if not isinstance(parsed, list):
        raise RuntimeError("Could not parse Data2Vis inference output")

    specs: List[Dict[str, Any]] = []
    for row in parsed:
        if not isinstance(row, str):
            continue

        denorm_text = _backward_norm(row, field_types)
        try:
            candidate = json.loads(denorm_text)
        except Exception:
            continue

        if _valid_vegalite_spec(candidate):
            specs.append(candidate)

    if not specs:
        raise RuntimeError("No valid Vega-Lite specs were produced by Data2Vis")

    return specs[:3]


def run_data2vis(data_dir: str = "src/data"):
    csv_root = Path(data_dir)
    csv_files = sorted(csv_root.glob("*.csv"))

    for csv_path in csv_files:
        print(f"Running Data2Vis for {csv_path}...\n")

        output_dir = REPO_ROOT / "src" / "outputs" / "data2vis" / csv_path.stem
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            df = pd.read_csv(csv_path)
            df.drop(columns=['index', 'test_index', 'run_index', 'build'], inplace=True) # drop unnecessary columns!!!
            records = df.where(pd.notnull(df), None).to_dict(orient="records")

            specs = _run_data2vis_model(records, output_dir)

            if not specs:
                print(f"No Data2Vis specs generated for {csv_path.name}\n")
                continue

            for idx, spec in enumerate(specs):
                final_spec = _inject_data(spec, records)

                spec_path = output_dir / f"spec_{idx}.json"
                spec_path.write_text(json.dumps(final_spec, indent=2))

                png_path = output_dir / f"viz_{idx}.png"
                png_data = vlc.vegalite_to_png(vl_spec=final_spec, scale=2)
                png_path.write_bytes(png_data)
        except Exception as e:
            print(f"Data2Vis error processing {csv_path.name} - {e}\n")
