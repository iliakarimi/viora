import pyautogui as pg



class ComputerControl():
    
    """
    Control Computer
    """

    @classmethod
    def keyboard_control(
                cls, key= '', key_times=1, write= '',
                firsthkey= '', sechkey= '', hotkey= '',
            ):

        if write:
            pg.write(write)
            return

        if key:
            pg.press(key, presses=int(key_times) if key_times else 0)
            return

        if hotkey:
            keys = hotkey.split('+')
            pg.hotkey(*keys)
            return

        if firsthkey and sechkey:
            with pg.hold(firsthkey):
                pg.press(sechkey)
            return


    @classmethod
    def mouse_control(
                cls, movex=None, movey=None, 
                click_button=None, click_times=0, scroll=0
            ):
        
        if movex or movey is not None or 0:
            try:
                pg.moveTo(x=movex, y=movey)
                
            except Exception as e:
                return f"Error: {e}"
            return
        
        elif click_button:
            try:
                pg.click(button=click_button, clicks=click_times)
            except Exception as e:
                return f"Error: {e}"
            return
        
        elif scroll:
           try:
            pg.vscroll(clicks=scroll)
           except Exception as e:
               return f"Error: {e}"
