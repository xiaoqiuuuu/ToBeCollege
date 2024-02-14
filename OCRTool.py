import base64
import json
import urllib
import requests
from PIL import Image
import io

API_KEY = "替换为你自己的 API_KEY"
SECRET_KEY = "替换为你自己的 SECRET_KEY"



def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def image_to_base64(image: Image.Image, urlencoded=False, format="JPEG"):
    """
    获取PIL Image对象的base64编码信息
    :param format:
    :param image: PIL.Image.Image 类型的对象
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    output_buffer = io.BytesIO()
    # 将Image对象保存到内存缓冲区
    image.save(output_buffer, format=format)  # 默认使用JPEG格式，也可以根据需要调整
    byte_content = output_buffer.getvalue()
    base64_content = base64.b64encode(byte_content).decode("utf8")

    if urlencoded:
        import urllib.parse  # 引入urllib.parse模块以支持urlencoding
        base64_content = urllib.parse.quote_plus(base64_content)

    return base64_content


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


class OCRTool:
    def __init__(self):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?access_token=" + get_access_token()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
    }

    def recognize_digits(self, image):
        """
        识别图像中的数字
        Args:
            image: PIL.Image.Image 图像对象

        Returns:
            str: 识别出的数字的文本表示
        """

        payload = "image=" + image_to_base64(image, True,
                                             format="PNG") + "&recognize_granularity=big&detect_direction=false"
        return requests.request("POST", self.url, data=payload, headers=self.headers).text
