import subprocess


def cleart():
    try:
        #Try clear Terminal with "cls"
        subprocess.run(["cls"])
    except Exception:
        #if not windows using "clear"
        subprocess.run(["clear"])
