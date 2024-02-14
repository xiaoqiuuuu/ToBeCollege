"""
    ImageProcessor 是一个图片处理的类，主要负责把传入的图片分割成 10*16 的格式，方便后续的处理。
"""

from Tile import Tile
from PIL import Image, ImageOps


class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = ImageProcessor.load_image(self)

    def load_image(self):
        return Image.open(self.image_path)

    def show_image(self):
        self.image.show()

    # split_image 将 image 分割成 10 * 16 份,返回一个 Tile 对象列表
    def split_image(self, tile_size=(42, 42), begin_position=(12, 10) , delta = (17,12,35,35)):
        width, height = self.image.size
        tiles = []

        id = 0
        for y in range(begin_position[0], height - tile_size[0], tile_size[0]):
            for x in range(begin_position[1], width - tile_size[1], tile_size[1]):
                tile_picture = self.image.crop((x, y, x + tile_size[0], y + tile_size[1]))
                tile_picture = tile_picture.crop(delta)
                tile_picture = ImageOps.invert(tile_picture)
                tile = Tile(tile_picture, (x + delta[0], y + delta[1], x + delta[2], y + delta[3]), "tile_picture{:03d}".format(id))
                # tile.save_image("Images")
                tiles.append(tile)
                id += 1
        return tiles
