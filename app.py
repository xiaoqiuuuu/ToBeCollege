import json
import math
import random
import threading
import time

from CaptureWindow import CaptureWindow
from ImageProcessor import ImageProcessor
from Matrix import Matrix
from Tile import Tile
import pyautogui
from pygetwindow import getWindowsWithTitle
from OCRTool import OCRTool
import concurrent.futures


def monitor_window_position(window_title):
    # 获取指定标题的窗口
    windows = getWindowsWithTitle(window_title)
    if windows:
        # 获取第一个匹配窗口的位置
        window = windows[0]
        position = (window.left, window.top + 130)

        # 这里您可以处理窗口位置信息（例如，记录或触发事件）
        # print(f"窗口 '{window_title}' 的当前位置: {position}")
        return position
    return None


def recognize_and_append(tile):
    data = json.loads(ocr_tool.recognize_digits(tile.image))
    digit = data['words_result'][0]['words']
    digits[tile.id] = int(digit)  # 注意：假设tile.id是从1开始计数的，需要减1来匹配digits的索引
    print(f"线程ID: {threading.get_ident()} 正在识别第{tile.id}个数字：{digit}")
    time.sleep(0.1)


if __name__ == "__main__":
    target_title = '开局托儿所'  # 替换为您的目标窗口标题

    # 获取截图路径 ， 和窗口位置
    image_path = CaptureWindow.get_screenshot()

    # 对截图进行分割操作
    image_processor = ImageProcessor(image_path)
    tiles = image_processor.split_image()

    # 线程数量
    thread_num = 3
    # 文字识别
    # 创建 OCRTool，将数字图片识别到 10 * 16 的矩阵中
    digits = [0 for i in range(len(tiles))]
    tiles_parts = [tiles[i:i + len(tiles) // thread_num] for i in range(0, len(tiles), len(tiles) // thread_num)]

    ocr_tool = OCRTool()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
        futures = {executor.submit(recognize_and_append, tile): tile for part in tiles_parts for tile in part}
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"处理Tile时发生错误: {exc}")
                exit(0)

    matrix = Matrix(digits)

    n = matrix.n
    m = matrix.m

    matrix.show()


    def clear(a: Tile, b: Tile):
        # 获取窗口位置
        position = monitor_window_position(target_title)

        a_x = (a.position[0] + a.position[2]) // 2
        a_y = (a.position[1] + a.position[3]) // 2

        b_x = (b.position[0] + b.position[2]) // 2
        b_y = (b.position[1] + b.position[3]) // 2

        # 开始拖拽的位置
        start_x = position[0] + a_x
        start_y = position[1] + a_y

        # 拖拽结束的位置
        end_x = position[0] + b_x
        end_y = position[1] + b_y

        # print(position[0], position[1])
        print("start_x:", start_x, "start_y", start_y, "end_x:", end_x, "end_y:", end_y)

        # 首先单击开始位置（相当于按下鼠标左键）
        pyautogui.click(start_x, start_y, button='left')

        # 然后移动鼠标到结束位置（期间保持按钮按下状态）
        pyautogui.dragTo(end_x, end_y, duration=0.25, button='left')  # 可以根据需要调整duration参数来控制拖拽的速度


    def check_clear(x, y, xs):

        for i in range(1, n + 1):
            if x + i - 1 > n:
                break
            for j in range(1, m + 1):
                if j + y - 1 > m:
                    break

                res, score = matrix.query((x, y, x + i - 1, y + j - 1))

                if res == 10:
                    x2 = x + i - 1
                    y2 = y + j - 1

                    if xs < score:
                        return True
                    print(f"本次得分{score}")
                    clear(tiles[(x - 1) * m + y - 1], tiles[(x2 - 1) * m + y2 - 1])
                    matrix.modify((x, y, x2, y2))

                    return True

                if res > 10:
                    break
        return False


    xs = 2.00
    while True:
        flg = 0
        for i in range(1, 17):
            for j in range(1, 11):
                flg |= check_clear(i, j, xs)
        if flg == 0:
            break
        xs += 0.05

    print(f"游戏结束，本次得分为{160 - matrix.query((1,1,16,10))[1]}")

