from win32gui import GetWindowText, FindWindow, SetWindowPos, ShowWindow, SetForegroundWindow
from win32con import SW_SHOWNORMAL, HWND_TOPMOST
from PIL import ImageGrab, Image
import pynput.keyboard as pykeybd
import pynput.mouse as pymouse

import os, time, json, subprocess

mouse = pymouse.Controller()
keyboard = pykeybd.Controller()

''' Helper functions '''
def get_cursor_pos():
    (x,y) = mouse.position
    return x,y

def get_pixel_clr(x,y):
    pic = ImageGrab.grab().load()
    return pic[x,y]

def position_window(window):
    ShowWindow(window, SW_SHOWNORMAL)
    SetWindowPos(window, HWND_TOPMOST, 0, 0, 1280, 720, 0)
    SetForegroundWindow(window)


''' Input functions '''
def left_click_at(window, x,y):
    time.sleep(1)
    position_window(window)
    mouse.position = (x, y)
    mouse.click(pymouse.Button.left)
    
def left_hold_at(window, x,y):
    time.sleep(1)
    position_window(window)
    mouse.position = (x, y)
    mouse.press(pymouse.Button.left)
    time.sleep(0.5)
    mouse.release(pymouse.Button.left)

def type_string(window, string):
    time.sleep(1)
    position_window(window)
    keyboard.type(string)


''' Main function '''
if __name__ == '__main__':
    config = None
    with open("./.config") as f:
        config = json.load(f)

    time.sleep(3)
    
    level = 263
    counter = 0

    while (level <= 1000):
        # Open Dungeons game
        mcd_path = os.path.expanduser(config["install_path"])
        subprocess.Popen(mcd_path)
        time.sleep(10)

        # Get window, wait for loading
        mcd_window = FindWindow("UnrealWindow", None)
        assert(''.join(GetWindowText(mcd_window).split()) == "MinecraftDungeons")

        # Keep spamming "x" until main menu 
        while True:
            time.sleep(1)
            type_string(mcd_window, "x")
            if get_pixel_clr(60,610) == (65,140,80):
                break

        # Start Online Game, wait for entering camp
        type_string(mcd_window, "\n")
        time.sleep(1)
        type_string(mcd_window, "\n")
        time.sleep(float(config["camp_loading_time"]))

        # Open map
        type_string(mcd_window, "m")

        # Select mainland
        left_click_at(mcd_window, 500, 80)

        # Select tower
        left_click_at(mcd_window, 30, 350)

        # Select start tower run, and wait for map loading
        left_click_at(mcd_window, 150,650)
        time.sleep(float(config["mission_loading_time"]))

        # Move character and conclude mission
        left_hold_at(mcd_window, 20, 400)
        time.sleep(2)
        left_hold_at(mcd_window, 30,225)
        time.sleep(6)

        # Close the game
        left_click_at(mcd_window, 1249,12)
        
        # Buffer sleep
        time.sleep(float(config["buffer_time"]))

        # update counters
        print(counter)
        level += 3
        counter += 1