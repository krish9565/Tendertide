import os
import subprocess
import platform

def run_scripts_in_separate_windows(scripts):
    """
    Run specific Python scripts in separate windows.
    
    :param scripts: List of script names to run.
    """
    for script_name in scripts:
        # Ensure the script exists in the current directory
        script_path = os.path.join(os.getcwd(), script_name)
        if not os.path.isfile(script_path):
            print(f"Script {script_name} not found in the current directory!")
            continue

        try:
            print(f"Launching script: {script_name}")
            if platform.system() == "Windows":
                # Correctly quote the script path
                subprocess.Popen(
                    f'start cmd /k "python \"{script_path}\""',
                    shell=True
                )
            else:
                # Open a new terminal on macOS or Linux
                subprocess.Popen(["gnome-terminal", "--", "python3", script_path])
        except Exception as e:
            print(f"Error occurred while launching {script_name}: {e}")

if __name__ == "__main__":
    # Provide the names of the Python scripts to run
    scripts_to_run = [
        "WS01-ted.py",      # Replace with the actual script names
        "WS02-philgeps.py", # Example script
        "WS03-worldbank.py" # Another example
    ]
    run_scripts_in_separate_windows(scripts_to_run)
