import threading
import time
import random

import cv2 as cv
from PIL import Image

from .cap import WindowCapture
from .utils import spiral, tranform_spiral, translate_hp_sp_from_Image


wincap = WindowCapture('Ragnarok')

class wing_away_detector(threading.Thread):
    
    def __init__(self,color_signal):
        self.color_signal = color_signal # color to detect
        self.is_found_avoids_at = None
        self.need_to_break = False
    
    def detect_avoids(self,screenshot):
        pass
        # function find monster pixel >> 
        # self.is_found_monster_at = [x,y]
        # self.is_found_monster_at = None
    
    def run(self):
        
        print("Start Attacking Detector !")
        
        while not self.need_to_break:
            screenshot = wincap.grab_screenshot()

            self.detect_avoids(screenshot) # check ไปเรื่อยๆ
    
    def stop(self):
        
        print("Stop Detector")
        self.need_to_break = True
        
class items_detector(threading.Thread):
    
    
    def __init__(self,color_signal):
        self.color_signal = color_signal # color to detect
        self.need_to_break = False
        self.is_found_items_at = None
    
    def detect_items(self,screenshot):
        # loop_list = tranform_spiral(spiral=spiral(wincap.w,wincap.h,dx=20),top_left_location=wincap.top_left)
        # for x,y in loop_list:
        loop_list = spiral(wincap.w,wincap.h,dx=50)
        for x,y in loop_list:
            try:
                r, g, b = screenshot.getpixel((x, y))
                if (r,g,b) == self.color_signal:
                    x = x+wincap.top_left[0]
                    y = y+wincap.top_left[1]
                    # print("found items at" ,x ,y)
                    self.is_found_items_at = [x,y]
                    return
                
            except:
                pass

        self.is_found_items_at = None
        
    
    def run(self):
        
        print("Start Monster Detector !")
                
        while True:
            screenshot = wincap.grab_screenshot()
            self.detect_items(screenshot) # check ไปเรื่อยๆ
            
            if self.need_to_break:
                break
    
    def stop(self):
        
        print("Stop Detector items")
        self.need_to_break = True

class walk_detector(threading.Thread):
     
    
    def __init__(self,color_signal=(24, 49, 49),portal_color_signal=()):
        self.color_signal = color_signal # color to detect
        self.portal_color_signal = portal_color_signal # color to detect
        self.is_found_portal = False # color to detect
        self.need_to_break = False
        self.next_walk = None
        
    def detect_portal(self):
        screenshot = wincap.grab_screenshot()
        h, w = screenshot.size
        for x in range(0,h,20):
            for y in range(0,w,20):
                try:
                    r, g, b = screenshot.getpixel((x, y)) 
                    r2, g2, b2 = screenshot.getpixel((x+20, y)) 
                    r3, g3, b3 = screenshot.getpixel((x+10, y+20)) 
                    
                    if (r,g,b) == self.portal_color_signal and (r2,g2,b2) == self.portal_color_signal and (r3,g3,b3) == self.portal_color_signal:
                        return True
                
                except:
                    pass
        
        return False
        # loop_list = spiral(wincap.w,wincap.h,dx=100)
        # detect = False
        # for x,y in loop_list:
        #     try:
        #         r, g, b = screenshot.getpixel((x, y))
        #         if (r,g,b) == self.portal_color_signal:
        #             x = x+wincap.top_left[0]
        #             y = y+wincap.top_left[1]
        #             # print("found items at" ,x ,y)
        #             self.is_found_portal = True
        #             detect = True
        #             return True
        #             # break
                
        #     except:
        #         pass
        # if detect:
        #     self.is_found_portal = False
        #     return False
    
    def detect_walk(self,screenshot):
        
        # loop_list = tranform_spiral(spiral=spiral(wincap.w,wincap.h,dx=10),top_left_location=wincap.top_left)
        while True:
            # loc=[0,0]
            # loc[0] = random.randint(100,wincap.w-100) 
            # loc[1] = random.randint(100,wincap.h-100) 
            if self.need_to_break:
                return
            
            loop_list = spiral(wincap.w,wincap.h,dx=25)
            loop_list = loop_list[:int(len(loop_list)/1.5)]

            loc = random.choice(loop_list)
            
            r, g, b = screenshot.getpixel((loc[0],loc[1]))
            if (r,g,b) == self.color_signal:
                loc[0] = loc[0]+wincap.top_left[0]
                loc[1] = loc[1]+wincap.top_left[1]
                # print("next walk to " , loc[0] , "   ", loc[1])
                self.next_walk = [loc[0],loc[1]]
                return
            
        return
                          
                

    
    def run(self):
        
        print("Start walk Detector !")
        
        while True:
            if self.need_to_break:
                break
            screenshot = wincap.grab_screenshot()
            self.detect_walk(screenshot)
        print("end walk Detector !")
        return

    
    def stop(self):
        
        print("Stop Detector walk")
        self.need_to_break = True        

class monsters_detector(threading.Thread):
    
    is_found_monster_at = None
    
    def __init__(self,color_signal=(231, 99, 132)):
        self.color_signal = color_signal # color to detect
        # self.is_found_monster_at = None
        self.need_to_break = False
    
    # def detect_monsters(self,screenshot):
    def detect_monsters(self):
        # loop_list = tranform_spiral(spiral=spiral(wincap.w,wincap.h,dx=10),top_left_location=wincap.top_left)
        screenshot = wincap.grab_screenshot()
        loop_list = spiral(wincap.w,wincap.h,dx=50)
        loop_list = loop_list[:int(len(loop_list)/1.4)] 
        h, w = screenshot.size
        for x,y in loop_list:
            try:
                r, g, b = screenshot.getpixel((x, y))
                if (r,g,b) == self.color_signal:
                    x = x+wincap.top_left[0]
                    y = y+wincap.top_left[1]
                    # print("Found Monster AT" , x , "   ", y)
                    self.is_found_monster_at = [x,y]
                    return self.is_found_monster_at

            except:
                pass
        
        # self.is_found_monster_at = None
        return None
            
        
       

        # function find monster pixel >> 
        # self.is_found_monster_at = [x,y]
        # self.is_found_monster_at = None
    
    def run(self):
        
        print("Start Monster Detector !")
                
        while True:
            # screenshot = wincap.grab_screenshot()
            # self.detect_monsters(screenshot) # check ไปเรื่อยๆ
            
            if self.need_to_break:
                break
    
    def stop(self):
        
        print("Stop Detector Mons")
        self.need_to_break = True

class atk_detector(threading.Thread):
    
    is_attacking = False
    
    def __init__(self,color_signal):
        self.color_signal = color_signal # color to detect
        # self.is_attacking = False
        self.next_walk = []
        self.need_to_break = False                 
        
    
    def detect_attack(self,screenshot):
        
        # loop_list = tranform_spiral(spiral=spiral(wincap.w,wincap.h,dx=10),top_left_location=wincap.top_left)
        # for x,y in loop_list:
        loop_list = spiral(wincap.w,wincap.h,dx=10)
        for x,y in loop_list:
            try:
                r, g, b = screenshot.getpixel((x, y))
                if (r,g,b) == self.color_signal:
                    # print("Player is attacking" )
                    self.is_attacking = True
                    return
            except:
                pass
        self.is_attacking = False
            

            


        # function find yellow triangle
        # self.is_attacking = True if found
        # self.is_attacking = False if not found
    
    def run(self):
        
        print("Start Attacking Detector !")
        
        while True:
            screenshot = wincap.grab_screenshot()
            self.detect_attack(screenshot) # check ไปเรื่อยๆ
            # print(self.is_attacking)
        
            if self.need_to_break:
                break
    

    def stop(self):
        
        print("Stop Detector atk")
        self.need_to_break = True

class health_sp_detector(threading.Thread):
    
    need_to_break = False
    
    def __init__(self,regen_at_percentage,crop_stat):
        
        self.regen_at_percentage_hp = regen_at_percentage # percent of hp to regen
        self.regen_at_percentage_sp = regen_at_percentage # percent of sp to regen
        self.crop_stat = crop_stat
        # self.need_to_break = False
        self.is_low_health = False
        self.is_low_sp = False
        
        """
        key to heal
        """
        
    def detect_health_sp(self,screenshot):
        
        res = translate_hp_sp_from_Image(screenshot)
        reshp = res["hp"]
        
        if int(reshp) < self.regen_at_percentage_hp:
            print("need healing")
            self.is_low_health = True
        
        else :
            self.is_low_health = False
        
        ressp = res["sp"]
        
        if int(ressp) < self.regen_at_percentage_sp:
            self.is_low_sp = True
        
        else :
            self.is_low_sp = False
        
        return
        
        # func by crop location >> to number >> 
        # if number of health percent lower than self.regen_at_percentage 
    
    def run(self):
        
        print("Start hp Detector !")
        
        while True:
            screenshot = wincap.grab_screenshot()
            screenshot = screenshot.crop(self.crop_stat)
            self.detect_health_sp(screenshot) # check ไปเรื่อยๆ

            if health_sp_detector.need_to_break:
                break
        
        return
            
    def end(self):
        
        print("Stop Detector hp sp")
        # self.need_to_break = True
        health_sp_detector.need_to_break = True
        return
        
        
class get_buff_detector(threading.Thread):
    
    """
    hotkey as {ENTER} {F1} 'a' 'b'
    """
    
    def __init__(self,timer,self_pointing = True ,delay_after_skill = 0 , bot_buff_action = None):
        self.need_to_break = False
        self.timer = timer # use every ... sec
        self.self_pointing = self_pointing # true if skill need to use on self
        self.wait_for_buff = True
        self.delay_after_skill = delay_after_skill
        self.bot_buff_action = bot_buff_action
    
    def use_buff(self):
        res = self.bot_buff_action.use_skill()
        return True
        
    def run(self):
        
        print("start buff detector") ## use potion of skill every .. sec
        timer = 0
        while True:
            if self.need_to_break:
                break
            
            if timer >= self.timer :
                self.wait_for_buff = True
                print("need buff now")
                while True:
                    if not self.wait_for_buff:
                        timer = 0
                        break

            else:
                time.sleep(1)
                timer += 1
                continue
            
        return
            
        
                
            
            # need to change state in main bot thread
            
    def end(self):
        
        print("Stop Detector buff")
        self.need_to_break = True
        return
            
                
            

# while(True):
    
#     # get an updated image of the game
#     screenshot , IMG_to_match = wincap.grab_screenshot()

#     cv.imshow('PYBOTT VISION', screenshot)
    
#     # cv.imshow('PYBOTT VISION', screenshot)  

#     # debug the loop rate
#     # loop_time = time()
#     # press 'q' with the output window focused to exit.
#     # waits 1 ms every loop to process key presses
#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break
    
# print('Done.')
