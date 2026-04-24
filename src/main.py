from tools.autoviz import run_autoviz
from tools.deepeye import run_deepeye
from tools.lux import run_lux

def main():
    print("Running AutoViz...\n")
    try:
        run_autoviz()
        print(f"AutoViz completed!\n")
    except Exception as e:
        print(f"AutoViz failed - {e}\n")
    
    print("Running DeepEye...\n")
    try:
        run_deepeye()
        print(f"DeepEye completed!\n")
    except Exception as e:
        print(f"DeepEye failed - {e}\n")

    print("Running Lux...\n")
    try:
        run_lux()
        print(f"Lux completed!\n")
    except Exception as e:
        print(f"Lux failed - {e}\n")

if __name__ == "__main__":
    main()
