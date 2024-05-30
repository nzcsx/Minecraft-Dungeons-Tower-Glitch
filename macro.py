from win32gui import GetWindowText, GetForegroundWindow
from PIL import ImageGrab
import pynput.keyboard as pykeybd
import pynput.mouse as pymouse
import time
import datetime
import random

mouse = pymouse.Controller()
keyboard = pykeybd.Controller()

def get_cursor_pos():
    (x,y) = mouse.position
    return x,y

def get_pixel_clr(x,y):
    pic = ImageGrab.grab().load()
    return pic[x,y]

def get_active_win():
    return GetWindowText(GetForegroundWindow())

def left_click_at(x,y):
    time.sleep(1)
    mouse.position = (x, y)
    mouse.click(pymouse.Button.left)
    
def left_hold_at(x,y):
    time.sleep(1)
    mouse.position = (x, y)
    mouse.press(pymouse.Button.left)
    time.sleep(0.5)
    mouse.release(pymouse.Button.left)

def type_string(string):
    time.sleep(1)
    keyboard.type(string)


if __name__ == '__main__':
    
    time.sleep(3)
    
    level = 263
    counter = 0
    
    while (level <= 1000):
        time.sleep(5)
        
        # click at Minecraft Launcher, wait
        left_click_at(520,1060)
        time.sleep(3)
        
        # if doesn't show up, click again
        if (get_active_win() != "Minecraft Launcher"):
            left_click_at(520,1060)
            time.sleep(3)
            
        # wait for laucher loading
        while (get_pixel_clr(977,739) != (255, 164, 31)):
            time.sleep(1)

        # click on Play
        left_click_at(977,739)
        
        # wait for game booting until title appears
        while (get_pixel_clr(152, 124) != (255, 121, 31)):
            time.sleep(1)
        
        # type any button, wait for main menu
        type_string("\n")
        time.sleep(3)
        
        # Play Online, wait for session menu
        type_string("\n")
        time.sleep(1)
        
        # Start Online Game, wait for entering
        type_string("\n")
        time.sleep(9)
        
        # open map
        type_string("m")
        
        # click tower
        left_click_at(35, 487)
        
        # click continue
        left_click_at(181,915)
        
        # wait for loading map
        time.sleep(6)
        
        # move character and conclude mission
        left_hold_at(5, 593)      
        time.sleep(2)
        left_hold_at(43,290)
        time.sleep(6)
        
        # close the game
        left_click_at(1901,1)
        
        # buffer sleep
        time.sleep(5)
        
        # update counters
        print(counter)
        level += 3
        counter += 1
        '''
        x, y = get_cursor_pos()
        print(x, " ", y, " ", get_pixel_clr(152, 124), " ")
        '''