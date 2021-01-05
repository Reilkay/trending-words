from typing import Tuple
from PIL import Image, ImageFont, ImageDraw


class NoneImage:
    def __init__(self) -> None:
        self.__text = "暂无图片"

    def get_none_img(self,
                     size: Tuple = (600, 400),
                     color: Tuple = (255, 255, 255)):
        image = Image.new('RGB', size, color)
        font_type = './res/font/Microsoft_Yahei_Bold.ttf'
        font = ImageFont.truetype(font_type, 24)
        font_color = "#000000"
        draw = ImageDraw.Draw(image)
        draw.text((size[0] / 2 - len(self.__text) * 9.5, size[1] / 2 - 20),
                  u'%s' % self.__text, font_color, font)
        return image
