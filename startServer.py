from threading import Thread
import os
def run_time(script):
    os.system(f"py {script}")
scriptone = Thread(target=run_time, args=("server.py",))
scriptone.start()
script2 = Thread(target=run_time, args=("main.py",))
script2.start()
script2 = Thread(target=run_time, args=(r"remote_new_download\rar_main.py",))
script2.start()
