import threading
from utils.control.all_control import *
from utils.control.action import bot_action
from utils.thread_event import wincap

# def simple_left_click(x,y):
#     set_pos(x+75,y+100)
#     time.sleep(0.5)
#     hold_left_click()
#     time.sleep(0.5)
#     release_left_click()
    



class BOT(threading.Thread):
    
    
    def __init__(self,attacking_detector,health_sp_detector,get_buff_detector,monsters_detector,items_detector,wing_index=5):
        
        
        """
        use wing every {wing_index} move
        """
        
        self.wing_index = wing_index
        self.need_wing = 0
        
        """
        inject all treading detector to bot
        get_buff_detector must be list of buff class (eg . A B Awake)
        """
        
        self.detector = {
            "attacking_detector" : attacking_detector,
            "health_sp_detector" : health_sp_detector,
            "get_buff_detector" : get_buff_detector,
            "monsters_detector" : monsters_detector,
            "items_detector" : items_detector
        }
                
        self.running_detector = []
        
        self.pause = False # True  bot will be pause
        
        """
        miscellanous
        """
        self.monster_count = 0
        
        """
        player status
        """
        self.is_atk = attacking_detector.is_attacking
        self.next_walk = attacking_detector.next_walk
        self.is_low_health = health_sp_detector.is_low_health
        self.is_low_sp = health_sp_detector.is_low_sp
        self.is_monster_found = monsters_detector.is_found_monster_at  ## finish monster detector
        self.is_items_found = items_detector.is_found_items_at
        self.is_buff_expire = [] # loop to check
        
        """
        save current state of bot
        """
        self.bot_state = None # start from nothing
    
    def run(self):
        
        """
        setup bot action before run
        """
        
        for key,value in self.detector.items(): # สั่งรัน thread ทุกตัว
            # value is class of detector so we call func from this class
            t = threading.Thread(target=value.run)
            t.start()
            self.running_detector.append(t)
        
        while not self.pause :
            
            if not self.is_atk:
                
                if self.is_low_health and self.is_low_sp :
                    
                    while self.is_monster_found is not None:
                        wing_away = bot_action()
                        wing_away.use_skill_wing()
                    
                    if self.detector["get_buff_detector"].heal_is_skill :
                        simple_heal = bot_action(hotkey=self.detector["get_buff_detector"].heal_hot_key,skill_on_location=self.detector["get_buff_detector"].window_size_at_character)
                        while self.detector["get_buff_detector"].is_low_health:
                            simple_heal.use()
                    else:
                        simple_heal = bot_action(hotkey=self.detector["get_buff_detector"].heal_hot_key)
                        while self.detector["get_buff_detector"].is_low_health:
                            simple_heal.use()
                            time.sleep(0.25)
                            
                self.bot_state == "LOOKING FOR MON"
            
            if self.bot_state == "LOOKING FOR MON":
                
                if self.is_monster_found:
                    
                    simple_attack = bot_action()
                    simple_attack.simple_left_click(self.is_monster_found)
                    
                    self.bot_state = "ATTACKING"
                    self.wing_index = self.wing_index - 0.5
                    
                else:

                    walking_action = bot_action()
                    walking_action.simple_left_click(x=self.next_walk[0],y=self.next_walk[1])
                    time.sleep(0.5)
                    self.wing_index = self.wing_index - 1
                    self.bot_state == "LOOKING FOR MON"
                

        for key,value in self.detector.items(): # สั่งรัน thread ทุกตัว
            # value is class of detector so we call func from this class
            value.stop() # call function stop on each detector class
        
        for i in self.running_detector:
            i.join()
    
    def run_buff(self):
        
        while not self.pause:
            if self.detector["get_buff_detector"]:
                for each_buff in self.detector["get_buff_detector"]:
                    if each_buff.wait_for_buff:
                        self.is_buff_expire.append(each_buff)
                        self.bot_state = None
                        
                        each_buff.wait_for_buff = False # update thread after use buff
            
                for each_expire_buff in self.is_buff_expire:
                    if not each_expire_buff.self_pointing:
                        simple_buff = bot_action(hotkey=each_expire_buff.hotkey,skill_on_location=None)
                        time.sleep(each_expire_buff.delay_after_skill)
                    
                    else :
                        loc = each_expire_buff.window_size_at_character
                        simple_buff = bot_action(hotkey=each_expire_buff.hotkey,skill_on_location=loc)
                        time.sleep(each_expire_buff.delay_after_skill)
                
                self.is_buff_expire = []
                    
            
        
                        

                
            
            # update char status by access detector class attribute
            

    
    def stop(self):
        
        self.pause = True
        

