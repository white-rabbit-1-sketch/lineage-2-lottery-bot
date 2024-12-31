import pyautogui
import cv2
import numpy as np
import time
import pygetwindow as gw
import pydirectinput
import ctypes

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000

ACTIVATE_WINDOW_SLEEP_TIME = 2
REGULAR_SLEEP_TIME = 0.6
KEY_EVENT_SLEEP_TIME = 0.05

IMAGES_COORDS_CACHE = {}

class NavigatorService:
    def __init__(self, assets_path: str):
        self.assets_path = assets_path

    def activate_window(self, window_title: str) -> None:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            windows[0].activate()
            time.sleep(ACTIVATE_WINDOW_SLEEP_TIME)
        else:
            raise Exception(f"Window '{window_title}' not found.")

    def find_image(self, target_image: str, confidence: float = 0.8) -> [int, int, int, int]:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(self.assets_path + target_image, cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            x, y = max_loc
            h, w = template.shape[:2]
            return x, y, h, w
        else:
            return None

    def click(self, x: int, y: int) -> None:
        ctypes.windll.user32.SetCursorPos(x, y)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(KEY_EVENT_SLEEP_TIME)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(REGULAR_SLEEP_TIME)

    def click_image(
        self,
        image: str,
        offset_x: int,
        offset_y: int,
        throw_on_error: bool = True,
        use_cache: bool = True
    ) -> None:
        result = None

        #if use_cache: result = IMAGES_COORDS_CACHE.get(image)

        if not result:
            result = self.find_image(image)
            IMAGES_COORDS_CACHE[image] = result

        if result:
            x, y, h, w = result
            self.click(x + offset_x, y + offset_y)
        elif throw_on_error: raise Exception("Image not found")

    def input(self, text: str) -> None:
        for char in text:
            pydirectinput.write(char, 0.005)

        time.sleep(REGULAR_SLEEP_TIME)