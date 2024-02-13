'''
该文件实现了一个Tile类，用于保存经过ImageProcessor处理后的图像块，和每个图像块位置信息
'''
import os.path

from PIL import Image


class Tile:
    def __init__(self, image, position, name="tile_picture"):
        self.image = image
        self.position = position
        self.name = name

    def get_position(self):
        return self.position

    def show_image(self):
        self.image.show()

    def save_image(self, folder_path=None):
        if folder_path is not None:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            self.image.save(folder_path + "\\" + self.name + ".png", format="PNG")
        else:
            self.image.save(self.name, format="PNG")
