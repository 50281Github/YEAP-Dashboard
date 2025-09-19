import subprocess
import sys

def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(f"--- {script_name} output ---")
        print(result.stdout)
        if result.stderr:
            print(f"--- {script_name} errors ---")
            print(result.stderr)
        print(f"{script_name} finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(e.stdout)
        print(e.stderr)

if __name__ == "__main__":
    scripts_to_run = [
        "q345_analyze_data_new.py",
        "q6q7q10q11_analysis.py",
        "q8q9_analysis.py",
    ]

    for script in scripts_to_run:
        run_script(script)

    print("All analysis scripts have been executed.")