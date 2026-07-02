import sys

def _load_autoviz():
    from tools.autoviz import run_autoviz
    return run_autoviz

def _load_draco():
    from tools.draco import run_draco
    return run_draco

def _load_deepeye():
    from tools.deepeye import run_deepeye
    return run_deepeye

def _load_lux():
    from tools.lux import run_lux
    return run_lux

def _load_lida():
    from tools.lida import run_lida
    return run_lida

TOOL_LOADERS = {
    "autoviz": _load_autoviz,
    "draco": _load_draco,
    "deepeye": _load_deepeye,
    "lux": _load_lux,
    "lida": _load_lida,
}

TOOL_ORDER = ["autoviz", "draco", "deepeye", "lux", "lida"]

def _run_tool(tool_name: str) -> bool:
    print(f"Running {tool_name.capitalize()}...\n")

    try:
        run_tool = TOOL_LOADERS[tool_name]()
        run_tool()

        return True
    except Exception as e:
        print(f"{tool_name.capitalize()} failed - {e}\n")
        return False


def main() -> int:
    args = [arg.lower() for arg in sys.argv[1:]]

    print("Starting!!!\n")

    if not args or args[0] == "all":
        selected_tools = TOOL_ORDER
    else:
        requested_tool = args[0]

        if requested_tool not in TOOL_LOADERS:
            available = ", ".join(TOOL_ORDER)
            print(f"Unknown tool '{requested_tool}'. Use one of: {available}, or 'all'.")
            return 1
        selected_tools = [requested_tool]

    failed = False
    for tool_name in selected_tools:
        ok = _run_tool(tool_name)
        if not ok:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
