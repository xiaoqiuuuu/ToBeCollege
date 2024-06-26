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
    def split_image(self, begin_position=(15, 15), delta=(10, 10, 40, 40)):
        width, height = self.image.size
        height = height // 17 * 16
        tile_size = (width // 10 - 3 , height // 16 - 1 )
        tiles = []

        id = 0
        for y in range(begin_position[0], height - 20, tile_size[1]):
            for x in range(begin_position[1], width - 20, tile_size[0]):
                tile_picture = self.image.crop((x, y, x + tile_size[0], y + tile_size[1]))
                tile_picture = tile_picture.crop(delta)
                tile_picture = ImageOps.invert(tile_picture)
                tile = Tile(tile_picture, (x + delta[0], y + delta[1], x + delta[2], y + delta[3]), id,
                            "tile_picture{:03d}".format(id))
                tile.save_image("Images")
                tiles.append(tile)
                id += 1
        return tiles
