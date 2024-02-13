'''
    ImageProcessor 是一个图片处理的类，主要负责把传入的图片分割成 10*16 的格式，方便后续的处理。
'''

from Tile import Tile
from PIL import Image, ImageOps
from OCRTool import OCRTool

import os

class ImageProcessor():
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = ImageProcessor.load_image(self)

    def load_image(self):
        return Image.open(self.image_path)

    def show_image(self):
        self.image.show()

    # split_image 将 image 分割成 10 * 16 份,返回一个 Tile 对象列表
    def split_image(self, tile_size=(42, 42), begin_position=(12, 10)):
        width, height = self.image.size
        tiles = []

        id = 0
        for y in range(begin_position[0], height - tile_size[0], tile_size[0]):
            for x in range(begin_position[1], width - tile_size[1], tile_size[1]):
                tile_picture = self.image.crop((x, y, x + tile_size[0], y + tile_size[1]))
                tile_picture = tile_picture.crop((17, 12, 35, 35))
                tile_picture = ImageOps.invert(tile_picture)
                tile = Tile(tile_picture, (x, y, x + tile_size[0], y + tile_size[1]), "tile_picture{:03d}".format(id))
                tile.save_image("Images")
                tiles.append(tile)
                id += 1
        return tiles


if __name__ == "__main__":
    image = ImageProcessor("screenshot.png")

    tiles = image.split_image()

    ocr_tool = OCRTool()

    digits = []
    digit = []
    for i, tile in enumerate(tiles):
        digit.append(ocr_tool.recognize_digit(tile.image))
        if i % 10 == 9:
            digits.append(digit)
            digit = []

    for i in digits:
        print(i)