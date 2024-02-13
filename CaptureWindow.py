'''
    该类实现了捕捉窗口并截屏返回的功能，调用此方法可以直接在项目文件夹中生成 screenshot 的截图
'''

import pygetwindow as gw
import pyautogui
from PIL import Image


class CaptureWindow:
    @staticmethod
    def crop_bottom(image_path, percent_to_keep):
        # 打开图片
        image = Image.open(image_path)

        # 计算需要保留的高度
        width, height = image.size
        kept_height = int(height * percent_to_keep)

        # 裁剪图片
        cropped_image = image.crop((0, height - kept_height, width, height))

        # 保存裁剪后的图片
        cropped_image.save(image_path)

    @staticmethod
    def get_screenshot():
        percent_to_keep = 0.85  # 保留下方的90%

        # 获取窗口对象
        window = gw.getWindowsWithTitle('开局托儿所')[0]  # 替换为你要捕捉的窗口标题

        # 获取窗口的位置和大小
        x, y, width, height = window.left, window.top, window.width, window.height

        # 捕获窗口的屏幕截图
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        image_path = "screenshot.png"
        # 保存截图
        screenshot.save(image_path, "PNG")

        # 裁剪截图
        CaptureWindow.crop_bottom(image_path, percent_to_keep)
