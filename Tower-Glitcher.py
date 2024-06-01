from win32gui import GetWindowText, FindWindow, SetWindowPos, ShowWindow, SetForegroundWindow
from win32con import SW_SHOWNORMAL, HWND_TOPMOST
from PIL import ImageGrab, Image
import pynput.keyboard as pykeybd
import pynput.mouse as pymouse

import os, time, json, subprocess

mouse = pymouse.Controller()
keyboard = pykeybd.Controller()

# determine scale factor of user
import ctypes
scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

#### temporary function, not sure if it is useful
import win32con
import win32gui

def remove_border(window):
    style = win32gui.GetWindowLong(window, win32con.GWL_STYLE)
    # Remove the title bar and border
    style &= ~win32con.WS_CAPTION
    # Apply the new style
    win32gui.SetWindowLong(window, win32con.GWL_STYLE, style)
    # Redraw the window with the new style
    win32gui.SetWindowPos(window, 0, 0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER |
                            win32con.SWP_FRAMECHANGED)


''' Helper functions '''
def get_cursor_pos():
    (x,y) = mouse.position
    return x,y

def get_pixel_clr(x,y):
    pic = ImageGrab.grab().load()
    return pic[x,y]

def get_window(box):
    pic = ImageGrab.grab(bbox=box)
    return pic

def position_window(window):
    ShowWindow(window, SW_SHOWNORMAL)
    SetWindowPos(window, HWND_TOPMOST, 0, 0, int(1280/3*2/scaleFactor), int(720/3*2/scaleFactor), 0) # I changed this a bit
    SetForegroundWindow(window)

''' Input functions '''
def left_click_at(window, x,y):
    time.sleep(1)
    position_window(window)
    time.sleep(0.5)
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
        loadwindow = get_window((100,100,200,200)) # stores previous window
        while True:
            time.sleep(0.5)
            type_string(mcd_window, "x")

            window0 = get_window((100,100,200,200)) # window before F1

            keyboard.press(pykeybd.Key.f1)
            keyboard.release(pykeybd.Key.f1)

            time.sleep(0.5)

            window1 = get_window((100,100,200,200)) # window after F1

            if window1 != window0: # detect if window changes
                print('Something changed.')
                if loadwindow == window1: # if new window is identical to the last new window, F1 works
                    print('I think this is the settings again. Now the game is loaded.')
                    # exit setting page and exit loop
                    keyboard.press(pykeybd.Key.esc)
                    keyboard.release(pykeybd.Key.esc)
                    break
                else:
                    # might be the first time that F1 works, or game still loading
                    loadwindow = window1
            
            # try to exit setting page anyway, make sure game goes back to main page
            keyboard.press(pykeybd.Key.esc)
            keyboard.release(pykeybd.Key.esc)


        # Start Online Game, wait for entering camp
        type_string(mcd_window, "\n")
        time.sleep(1)
        type_string(mcd_window, "\n")
        time.sleep(float(config["camp_loading_time"]))

        # Open map
        # remove_border(mcd_window)
        type_string(mcd_window, "m")
        
        # Select mainland
        keyboard.press(pykeybd.Key.ctrl_l)  # Left Control
        keyboard.release(pykeybd.Key.ctrl_l)
        time.sleep(0.5)
        keyboard.press(pykeybd.Key.shift_l)  # Left Shift
        keyboard.release(pykeybd.Key.shift_l)
        time.sleep(0.5)
        keyboard.press(pykeybd.Key.ctrl_l)  # Left Control
        keyboard.release(pykeybd.Key.ctrl_l)
        # ensure it is mainland by pressing one more time
        keyboard.press(pykeybd.Key.ctrl_l)  # Left Control
        keyboard.release(pykeybd.Key.ctrl_l)

        # Select tower
        left_click_at(mcd_window, int(30/scaleFactor), int(360/scaleFactor))

        # Select start tower run using keyboard, and wait for map loading
        type_string(mcd_window, "\n")
        time.sleep(float(config["mission_loading_time"]))

        # Move character and conclude mission
        left_hold_at(mcd_window, 20/scaleFactor, 400/scaleFactor)
        time.sleep(2)
        left_hold_at(mcd_window, 30/scaleFactor, 225/scaleFactor)
        time.sleep(6)

        # Close the game alt+f4
        with keyboard.pressed(pykeybd.Key.alt):
            keyboard.press(pykeybd.Key.f4)
            keyboard.release(pykeybd.Key.f4)
        
        # Buffer sleep
        time.sleep(float(config["buffer_time"]))

        # update counters
        print(counter)
        level += 3
        counter += 1