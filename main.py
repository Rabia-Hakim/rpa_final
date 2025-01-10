import subprocess
import sys

# set the mode and the browser:
mode = "normal"  # choose 'normal' or 'headless'
browser = "chrome"  # choose 'chrome' or 'firefox'

# Install requirements
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
except subprocess.CalledProcessError as error:
    print("Error during installation:", error)
    sys.exit(1)

# Run the script based on the chosen mode and browser
if mode == 'normal':
    print(f"Running in normal mode with {browser}")
    result = subprocess.run(["python", "rpa_challenge.py", browser, mode], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Error:")
        print(result.stderr)
        
elif mode == 'headless':
    print(f"Running in headless mode with {browser}")
    result = subprocess.run(["python", "rpa_challenge.py", browser, mode], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Error:")
        print(result.stderr)
