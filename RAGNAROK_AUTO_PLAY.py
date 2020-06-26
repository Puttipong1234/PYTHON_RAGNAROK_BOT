import sys
import threading

import cv2 as cv
import numpy as np
from PIL import Image

from utils.cap import WindowCapture
# from utils.bot import BOT
from utils.control.action import bot_action
from utils.control.all_control import *
from utils.thread_event import (atk_detector, get_buff_detector,
                                health_sp_detector, items_detector,
                                monsters_detector, walk_detector,
                                wing_away_detector)

"""
detecting window and character
"""
wincap = WindowCapture('Ragnarok')
pause_running_bot = False
stop = False
char_x = wincap.center[0] - 2
char_y = wincap.center[1] - 15
character_location_center = [char_x,char_y]

left = wincap.window_rect[0]
top = wincap.window_rect[1]


    # print(wincap.h)
    # print(wincap.w)
    # print(wincap.top_left)
"""
all skill action
"""
Bot_atk_action = bot_action()
Bot_walk_action = bot_action()
Bot_pickup_item_action = bot_action()
Bot_teleport_skill_action = bot_action(hotkey="{F9}")
Bot_heal_skill_action = bot_action(hotkey="{F2}",skill_on_location=character_location_center)
Bot_agi_buff_action = bot_action(hotkey="{F4}",skill_on_location=character_location_center)
Bot_bless_buff_action = bot_action(hotkey="{F5}",skill_on_location=character_location_center)
    

"""
detector for fetching data
"""
Walk_detector = walk_detector(color_signal=(24,49,49),portal_color_signal=(29,41,41)) # pink to atk
w_t1 = threading.Thread(target=Walk_detector.run,daemon=True)
w_t1.start()

Monsters_detector = monsters_detector(color_signal=(231, 99, 132)) # pink to atk
# mons_t1 = threading.Thread(target=Monsters_detector.run)
# mons_t1.start()

Atk_detector = atk_detector(color_signal=(254,249,5))
atk_t1 = threading.Thread(target=Atk_detector.run,daemon=True)
atk_t1.start()


Items_detector = items_detector(color_signal=(33,198,66))
itm_t1 = threading.Thread(target=Items_detector.run,daemon=True)
itm_t1.start()

"""
health detector
"""
crop_stat=(173 , 77 , 206, 105 )
Health_sp_detector = health_sp_detector(regen_at_percentage=50,crop_stat=crop_stat)
hp_t1 = threading.Thread(target=Health_sp_detector.run,daemon=True)
hp_t1.start()



"""
buff detector
"""
Agi_buff_detector = get_buff_detector(timer=240,self_pointing=True,delay_after_skill=2,bot_buff_action=Bot_agi_buff_action)
Bless_buff_detector = get_buff_detector(timer=240,self_pointing=True,delay_after_skill=2,bot_buff_action=Bot_bless_buff_action)
agi_t1 = threading.Thread(target=Agi_buff_detector.run,daemon=True)
bless_t1 = threading.Thread(target=Bless_buff_detector.run,daemon=True)
agi_t1.start()
bless_t1.start()

buff_detectors = [Agi_buff_detector,Bless_buff_detector]

def escape_and_regen_or_buff(buff_detector=[]):
    
    while Monsters_detector.detect_monsters():
        Bot_teleport_skill_action.use_skill_wing()

    while Health_sp_detector.is_low_health:
        Bot_heal_skill_action.use_skill()
    
    if buff_detector:
        for i in buff_detector:
            if i.wait_for_buff:
                i.use_buff()
                time.sleep(i.delay_after_skill)
                i.wait_for_buff = False

    # Then back to main loop


def main_bot():
    
    #input for bot action
    need_wing_setup = 1
    need_wing = need_wing_setup #walk 3 time then wing
    
    while not pause_running_bot:
        
        # get buff before find monster

        while not stop:
            
            
            if Walk_detector.detect_portal():
                escape_and_regen_or_buff()
            #buff check
                # wing until no monster and buff
                # if true stop = true
            needs_buffs = []
            for i in buff_detectors:
                if i.wait_for_buff:
                    needs_buffs.append(i)
                
            if needs_buffs:
                escape_and_regen_or_buff(needs_buffs)

            #health check 
                # wing until no monster and buff
                # if true stop = true
            if Health_sp_detector.is_low_health:
                escape_and_regen_or_buff()
            

            mons = Monsters_detector.detect_monsters()
            if mons:
                # bot.attack!!
                Bot_atk_action.simple_left_click(mons[0],mons[1])
                ## attack loop
                time.sleep(0.5)
                while True: # attack until no more yellow in screen
                    
                    if Health_sp_detector.is_low_health: # check during attacking monster
                        escape_and_regen_or_buff()
                        break
                    if not Atk_detector.is_attacking:
                        time.sleep(0.3)
                        if Items_detector.is_found_items_at is not None:
                            Bot_pickup_item_action.simple_left_click(Items_detector.is_found_items_at[0],Items_detector.is_found_items_at[1])
                            
                        break
                        #bot.stop attack
                
                need_wing = need_wing - 0.3
                # add wing index then next loop
                if need_wing <= 0:
                    Bot_teleport_skill_action.use_skill_wing()
                    need_wing = need_wing_setup
            
            elif not Monsters_detector.detect_monsters():
                # print(Walk_detector.next_walk)
                if need_wing <= 0:
                    Bot_teleport_skill_action.use_skill_wing()
                    need_wing = need_wing_setup
                
                elif Walk_detector.next_walk is not None :
                    Bot_walk_action.simple_left_click(Walk_detector.next_walk[0],Walk_detector.next_walk[1])
                    need_wing = need_wing - 0.5
                    time.sleep(0.5)
                #walk or wing check wing index
                #bot.walk passing Walk_detector.next_walk 
                    # if walk add wing index
                

# loop_time = time()


main_bot_t1 = threading.Thread(target=main_bot,daemon=True)


if __name__ == "__main__":
    

    while True:
        
        a = input("Enter To Start")
        main_bot_t1.start()
        
        
        if input("Enter To Stop") == "" :
        
        # Monsters_detector.stop()
        # mons_t1.join()
            pause_running_bot=True
            stop = True
            main_bot_t1.join()
            
            
            Atk_detector.stop()
            atk_t1.join()
            
            Items_detector.stop()
            itm_t1.join()
            
            Walk_detector.stop()
            w_t1.join()
            
            Agi_buff_detector.end()
            agi_t1.join()
            
            Bless_buff_detector.end()
            bless_t1.join()
            
            Health_sp_detector.end()
            hp_t1.join()
        
        if input("press 'q' to end") == "q":
            print("Thank For Playing ")
            break
        
        
        

        # get an updated image of the game
        # screenshot = wincap.get_screenshot()
        # img = Image.fromarray(screenshot, 'RGB')
        # rgb_im = screenshot.convert('RGB')
        
        
        # cv.imshow('PYBOTT VISION', screenshot)  
        
        

        # # press 'q' with the output window focused to exit.

    
# print('Done.')
