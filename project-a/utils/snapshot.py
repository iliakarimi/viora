import Xlib
import pyautogui
import subprocess


def __screen_picture():
    """
    This function just Take an ScreenShot from the Screen
    """

    try:
        pyautogui.screenshot('logs/snapshot.png')
    except Xlib.error.DisplayConnectionError:
        subprocess.call(["xhost", "+"])
        pyautogui.screenshot('logs/snapshot.png')
    except Exception as e:
        raise RuntimeError(f"An Error Happend: {e}")
