import Xlib
import pyautogui
import subprocess
from time import sleep
from utils.encode import encode_image



class ComputerControl():
    """
    Control Computer
    """

    def __init__(self, key= '', times=1, write= '', firsthkey= '', sechkey= '', hotkey= '', left_click=None, right_click=None, wait_time=None, scroll=None): #The 'None' for mouse Parameter's temperary.
        self.key = key
        self.times = times
        self.write = write
        self.firsthkey = firsthkey
        self.sechkey = sechkey
        self.hotkey = hotkey
        self.left_click = left_click
        self.right_click = right_click
        self.wait_time = wait_time
        self.scroll = scroll

    def keyboard_control(self, key=None, times=None, write=None, firsthkey=None, sechkey=None, hotkey=None):

        if write:
            pyautogui.write(write)
            return

        if key:
            pyautogui.press(key, presses=int(times) if times else 1)
            return

        if hotkey:
            keys = hotkey.split('+')
            pyautogui.hotkey(*keys)
            return

        if firsthkey and sechkey:
            with pyautogui.hold(firsthkey):
                pyautogui.press(sechkey)
            return

    def mouse_control(self, left_click, right_click, wait_time, scroll):
        pyautogui.leftClick()
        
        right_click = pyautogui.click(right_click)
        for rc in right_click:
            sleep(wait_time)
            return rc 
        
        m_scrool = pyautogui.scroll(scroll)
        pass
