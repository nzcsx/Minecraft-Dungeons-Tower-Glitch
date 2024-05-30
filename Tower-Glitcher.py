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


''' Temporary new functions, not sure if they are useful '''
from win32con import GWL_STYLE, WS_CAPTION, SWP_NOMOVE, SWP_NOSIZE, SWP_NOZORDER, SWP_FRAMECHANGED
from win32gui import GetWindowLong, SetWindowLong, SetWindowPos

def remove_border(hwnd): # chatgpt function, remove border of the window, shadow still present
    style = GetWindowLong(hwnd, GWL_STYLE)
    # Remove the title bar and border
    style &= ~WS_CAPTION
    # Apply the new style
    SetWindowLong(hwnd, GWL_STYLE, style)
    # Redraw the window with the new style
    SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)


def find_tower_button(window,scale=1): # return mouse position of the power button
    position_window(window,scale)
    time.sleep(1)

    # flattened reference button
    flat_button = [ 392, 186, 631, 765, 708, 706, 704, 702, 390, 688, 704, 706, 708, 765, 563, 192, 392, \
                    392, 186, 626, 626, 683, 713, 416, 395, 381, 391, 708, 708, 647, 496, 563, 192, 392, \
                    392, 186, 626, 626, 626, 626, 477, 743, 747, 385, 722, 496, 496, 496, 563, 192, 392, \
                    392, 186, 626, 626, 626, 626, 173, 462, 399, 487, 496, 496, 496, 496, 563, 192, 392, \
                    392, 186, 626, 626, 626, 626, 626, 173, 765, 556, 496, 496, 496, 496, 563, 192, 392, \
                    392, 186, 626, 626, 626, 626, 173, 173, 344, 137, 142, 496, 496, 496, 563, 192, 392, \
                    392, 186, 626, 626, 626, 626, 173, 765, 765, 544, 132, 496, 496, 496, 563, 192, 392, \
                    392, 186, 626, 765, 626, 626, 173, 173, 395, 131, 124, 496, 496, 765, 563, 192, 392]


    img = get_window((0,0,100,int(720*scale/2+100)))
    img = img.convert('RGB')

    scr_window = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            row.append(sum(pixel)) # sum RGB values so result is 2D
        scr_window.append(row)
    
    d_,d = 99999999, 99999999
    best = None
    for j in range(0,len(scr_window)-8):
        for i in range(len(scr_window[0])-17):
            w = [row[i:i+17] for row in scr_window[j:j+8]]
            flat_w = [item for sublist in w for item in sublist]
            d_ = sum([((flat_w[_]-flat_button[_])**2) for _ in range(len(flat_w))])
            if d_ < d:
                d = d_
                best = (j,i)
                if j > 0 and i > 0 and (d_ == 0):
                    break
        if j > 0 and i > 0 and (d_ == 0):
            break

    return (best[1]+8)/scaleFactor, (best[0]+4)/scaleFactor


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

def position_window(window,scale=1): # able to change window scale more freely
    ShowWindow(window, SW_SHOWNORMAL)
    SetWindowPos(window, HWND_TOPMOST, 0, 0, int(1280*scale/scaleFactor), int(720*scale/scaleFactor), 0)
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
        remove_border(mcd_window)
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
        time.sleep(1)

        # Find and select tower button in a small window
        x,y = find_tower_button(mcd_window,scale=0.6)
        
        print('Click Now!') # just for debug ... feel free to remove
        time.sleep(0.3)
        print('Click Now!!')
        time.sleep(0.3)
        print('Click Now!!!')
        time.sleep(0.3)
        mouse.position = (x, y) # left_click restores the scale=1 window so not using that here
        mouse.click(pymouse.Button.left)

        # Select start tower run using keyboard, and wait for map loading
        position_window(mcd_window) # restore original window
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