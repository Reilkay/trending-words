import io
from PIL import Image
import requests
import jieba
import collections
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud
from logging import CRITICAL
from bs4 import BeautifulSoup
from typing import Tuple


class Trend:
    def __init__(self, URLs: Tuple) -> None:
        self.__headers = {
            'User Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.__URLs = URLs
        self.__content_all = ''
        self.__cloud_img = None
        self.__top_img = None

    def __get_content(self) -> None:
        self.__content_all = ''
        for URL in self.__URLs:
            try:
                resp = requests.get(url=URL, headers=self.__headers)
                html = resp.text
                # Speculate coding
                if resp.encoding == 'ISO-8859-1':
                    encodings = requests.utils.get_encodings_from_content(html)
                    if encodings:
                        encoding = encodings[0]
                        if encoding == 'GB2312':
                            encoding = 'GB18030'
                        html = resp.content.decode(encoding=encoding)
                soup = BeautifulSoup(html, 'html.parser')
                for hyperlink in soup.find_all('a'):
                    try:
                        self.__content_all += hyperlink.string
                    except:
                        continue
            except Exception as e:
                print('{}请求失败，错误为：{}'.format(URL, e))

    def __processing_text(self) -> None:
        content = self.__content_all.replace('\r',
                                             '').replace('\n', '').replace(
                                                 '\u3000', '')
        jieba.setLogLevel(CRITICAL)
        word_list = [item for item in jieba.lcut(content) if len(item) > 1]
        return word_list

    def __generate_image(self, word_list: list) -> None:
        if len(word_list) == 0:
            print('分词失败')
        word_count = collections.Counter(word_list)
        word_cloud = WordCloud(font_path='./res/font/Microsoft_Yahei_Bold.ttf',
                               background_color='white',
                               width=600,
                               height=400)
        word_cloud.generate_from_frequencies(word_count)
        self.__cloud_img = word_cloud.to_image()

        top10 = word_count.most_common(10)
        # 标签
        labels = [item[0] for item in top10]
        # 每个标签所占的比例
        count_sum = sum([item[1] for item in top10])
        x = [item[1] / count_sum * 100 for item in top10]
        # 绘制饼图
        actual_figure = plt.figure(figsize=(6, 4), dpi=100)
        pie_figure = actual_figure.add_subplot(111)
        figure_tmp = pie_figure.pie(x, labels=labels, autopct='%3.2f%%')
        # 正常显示中文标签
        myfont = fm.FontProperties(
            fname='./res/font/Microsoft_Yahei_Bold.ttf')  # 设置字体
        for text in figure_tmp[1]:
            text.set_fontproperties(myfont)
        buffer = io.BytesIO()  # 获取输入输出流对象
        actual_figure.canvas.print_png(buffer)  # 将画布上的内容打印到输入输出流对象
        data = buffer.getvalue()  # 获取流的值
        buffer.write(data)  # 将数据写入buffer
        top_img = Image.open(buffer)
        self.__top_img = top_img

    def get_img(self) -> Tuple:
        self.__get_content()
        self.__generate_image(self.__processing_text())
        return (self.__cloud_img, self.__top_img)


Trend(('http://neu.edu.cn', )).get_img()
