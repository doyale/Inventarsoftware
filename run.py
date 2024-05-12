import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

def run():
    script1_thread = threading.Thread(target=run_script, args=("UI_main.py",))
    script2_thread = threading.Thread(target=run_script, args=("eln_window.py",))

    script1_thread.start()
    script2_thread.start()

    script1_thread.join()
    script2_thread.join()

if __name__ == "__main__":
    run()