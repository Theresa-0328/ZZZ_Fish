import pyautogui
import cv2
import numpy as np
from PIL import Image
import pygetwindow
import time
import pydirectinput
import threading


def find_window(window_name):
    windows = pygetwindow.getWindowsWithTitle(window_name)
    if windows:
        return windows[0]
    else:
        print(f"窗口'{window_name}'未找到")
        return None


def capture_window_area():
    screenshot = pyautogui.screenshot()
    return np.array(screenshot)


def rapid_click(key, times, interval):
    for _ in range(times):
        pydirectinput.press(key)
        time.sleep(interval)


def match_template(screenshot, template):
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max_val, max_loc


def main():
    print("开始自动钓鱼")

    template1 = cv2.imread('image/1.png')
    template2 = cv2.imread('image/2.png')
    template3 = cv2.imread('image/3.png')
    template4 = cv2.imread('image/4.png')
    template5 = cv2.imread('image/5.png')
    template6 = cv2.imread('image/6.png')
    template7 = cv2.imread('image/7.png')
    template8 = cv2.imread('image/8.png')
    template9 = cv2.imread('image/9.png')

    window = find_window("绝区零")
    if window is None:
        print(f"请先打开游戏")
        return
    window.activate()

    state_fish = 0

    while True:
        screenshot = capture_window_area()

        if state_fish == 0:
            val, loc = match_template(screenshot, template1)
            if val > 0.9:
                print(val, "开始抛竿，等待上鱼")
                pydirectinput.press('f')
                time.sleep(0.5)
                state_fish = 1

        if state_fish == 1:
            val, loc = match_template(screenshot, template2)
            if val > 0.9:
                print(val, "开始收竿")
                pydirectinput.press('f')
                time.sleep(0.5)
                state_fish = 2

        if state_fish == 2:
            val, loc = match_template(screenshot, template9)
            if val > 0.8:
                pydirectinput.press('space')
                continue
            val, loc = match_template(screenshot, template4)
            if val > 0.8:
                val, loc = match_template(screenshot, template5)
                if val > 0.8:
                    print(val, "长按A")
                    pydirectinput.keyDown('a')
                    time.sleep(1.7)
                    pydirectinput.keyUp('a')
                    continue
                val, loc = match_template(screenshot, template6)
                if val > 0.8:
                    print(val, "连点A")
                    rapid_click('a', 10, 0.05)
                    continue

            val, loc = match_template(screenshot, template3)
            if val > 0.8:
                val, loc = match_template(screenshot, template5)
                if val > 0.8:
                    print(val, "长按D")
                    pydirectinput.keyDown('d')
                    time.sleep(1.7)
                    pydirectinput.keyUp('d')
                    continue
                val, loc = match_template(screenshot, template6)
                if val > 0.8:
                    print(val, "连点D")
                    rapid_click('d', 10, 0.05)
                    continue

            val, loc = match_template(screenshot, template8)
            if val > 0.8:
                print(val, "开始下一轮钓鱼")
                time.sleep(1)
                pydirectinput.moveTo(200, 200)
                pydirectinput.click()
                state_fish = 0
                continue

            val, loc = match_template(screenshot, template7)
            if val > 0.8:
                print(val, "开始下一轮钓鱼")
                time.sleep(1)
                pydirectinput.moveTo(200, 200)
                pydirectinput.click()
                state_fish = 0
                continue

        time.sleep(0.05)


if __name__ == "__main__":
    main()
