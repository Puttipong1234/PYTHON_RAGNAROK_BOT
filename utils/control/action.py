from ahk import AHK
from utils.control.all_control import *
ahk = AHK()

win = ahk.find_window(title=b'Ragnarok') # Find the opened window

# win.send('{ENTER}')

class bot_action():
    def __init__(self,hotkey=None,skill_on_location=None):
        
        """
        hotkey like {F1} {ENTER} or Simple text like 'a' 'b' 'w'
        skill_on_location [x , y ]coordination
        """
        
        self.hotkey = hotkey
        self.skill_on_location = skill_on_location
    
    
    def use_skill(self):
        
        if self.skill_on_location is None:
            win.send(self.hotkey)
        
        else:
            key_stroke = self.hotkey
            win.send(key_stroke)
            set_pos(self.skill_on_location[0],self.skill_on_location[1])
            time.sleep(0.5)
            hold_left_click()
            time.sleep(0.5)
            release_left_click()
            time.sleep(1)
    
    def use_skill_wing(self):
        
        key_stroke = self.hotkey
        win.send(key_stroke)
        time.sleep(0.5)
        win.send("{ENTER}")
        time.sleep(0.5)
                
    def simple_left_click(self,x,y):
        
        # command = "{" + "CLICK {}, {}".format(str(x),str(y)) + "}"
        # win.send(command)
        
        set_pos(x,y)
        time.sleep(0.2)
        hold_left_click()
        time.sleep(0.1)
        release_left_click()

    

                
            
    