import pyautogui as pyagui

# print()


def correct_resolution():
    
    swidth = pyagui.resolution().width
    sheight = pyagui.resolution().height

    return f"{swidth-1}" + "*" + f"{sheight-1}"
