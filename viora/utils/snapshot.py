import pyautogui
import subprocess
import Xlib

def __screen_picture():
    """
    Take an ScreenShot from the Screen
    """

    try:
        pyautogui.screenshot('logs/snapshot.png')
    
    except Xlib.error.DisplayConnectionError:
        subprocess.call(["xhost", "+"])
        pyautogui.screenshot('logs/snapshot.png')
    
    except Exception as e:
        raise f"An Error Happend: {e}"


__screen_picture()