from PIL import Image, ImageDraw, ImageFont
import requests
import re
from datetime import datetime
from io import BytesIO
import os


class Weather:
    is_true_city = True

    def __init__(self, city):
        self.city = city
        self._weather()

    def _weather_img(self, a: str):
        """
        根据天气情况返回对应的天气图片
        param: a string 天气
        return: path[str]
        """
        if "雨" in a:
            if "小" in a:
                file_name = "小雨.png"
            elif "中" in a:
                file_name = "中雨.png"
            elif "大" in a:
                file_name = "大雨.png"
            else:
                file_name = "雷阵雨.png"

        elif "阴" in a:
            file_name = "阴.png"
        elif "多云" in a:
            file_name = "多云.png"
        elif "雪" in a:
            if "小" in a:
                file_name = "小雪.png"
            elif "中" in a:
                file_name = "中雪.png"
            else:
                file_name = "雪.png"
        elif "风" in a:
            file_name = "风.png"
        else:
            file_name = "晴朗.png"
        return os.path.join(os.path.dirname(__file__), file_name)

    def _format_str(self, string) -> str:
        """
        格式化字符串
        """
        return re.sub(r"\s+", " ", string).strip()
        # return string.replace("\n", "").replace("℃", "").replace("  ", "")

    def _weather(self) -> None:
        """
        获取天气信息
        """
        data = requests.get(
            f"https://weather.cma.cn/api/autocomplete?q={self.city}&limit=10"
        )
        data = data.json()["data"][0].split("|")
        # 判断是否为正确的城市名
        if data[3] != "中国":
            self.is_true_city = False

        else:
            self.city = data[1]
            web_page = requests.get(
                f"https://weather.cma.cn/web/weather/{data[0]}.html"
            )

            data = web_page.content.decode("utf-8")
            # 通过正则表达式获取未来7天的天气
            weather_7days = re.findall(
                r'<div class="day-item">(([\s\S])*?)</div>', data
            )
            temperature_7days = re.findall(
                r'<div class="high">(([\s\S])*?)</div>[\s\S]*?<div class="low">(([\s\S])*?)</div>',
                data,
            )
            # 保存未来3天的天气
            self.today_temperature = self._format_str(temperature_7days[0][0])
            self.today_weather = self._format_str(weather_7days[1][0])
            self.tomorow_temperature = self._format_str(temperature_7days[1][0])
            self.tomorow_weather = self._format_str(weather_7days[8][0])
            self.after_tomorrow_temperature = self._format_str(temperature_7days[2][0])
            self.after_tomorrow_weather = self._format_str(weather_7days[15][0])

    def image(self):
        """
        生成天气图片
        return: bytes|str
        """
        if self.is_true_city:
            city = self.city

            today_temperature = self.today_temperature

            today_weather = self.today_weather

            tomorow_temperature = self.tomorow_temperature

            tomorrow_weather = self.tomorow_weather

            after_tomorrow_temperature = self.after_tomorrow_temperature

            after_tomorrow_weather = self.after_tomorrow_weather

            # 字体和字号
            # 绝对路径
            font_path = os.path.join(os.path.dirname(__file__), "1.ttf")

            font = ImageFont.truetype(font_path, size=25)
            # 字体二的大小自动根据城市名长度计算
            font2_size = 73 - len(city) * 7
            font2 = ImageFont.truetype(font_path, size=font2_size)
            font1 = ImageFont.truetype(font_path, size=20)
            # 读取背景图片
            background = Image.open(os.path.join(os.path.dirname(__file__), "天气.png"))
            drawer = ImageDraw.Draw(background)

            # 添加日期
            formatted_date = datetime.now().strftime(r"%Y年%m月%d日 %A")

            # 定义英文到中文的映射
            replacement_dict = {
                "Monday": "星期一",
                "Tuesday": "星期二",
                "Wednesday": "星期三",
                "Thursday": "星期四",
                "Friday": "星期五",
                "Saturday": "星期六",
                "Sunday": "星期天",
            }

            # 使用字典映射进行替换
            translated_date = " ".join(
                [replacement_dict.get(day, day) for day in formatted_date.split(" ")]
            )

            drawer.text((440, 180), translated_date, fill=(255, 255, 255), font=font1)

            # 今日天气

            drawer.text(
                (320, 30),
                f"{city}·{today_temperature}·{today_weather}",
                fill=(0, 0, 0),
                font=font2,
            )

            # 明日天气
            drawer.text(
                (320, 227),
                f"明天   {tomorow_temperature}",
                fill=(255, 255, 255),
                font=font,
            )
            weather_img = Image.open(self._weather_img(tomorrow_weather))
            weather_img = weather_img.resize((40, 40))
            background.paste(weather_img, (370, 220), mask=weather_img)

            # 后天天气
            drawer.text(
                (600, 227),
                f"后天   {after_tomorrow_temperature}",
                fill=(255, 255, 255),
                font=font,
            )
            weather_img = Image.open(self._weather_img(after_tomorrow_weather))
            weather_img = weather_img.resize((40, 40))
            background.paste(weather_img, (650, 220), mask=weather_img)
            # 将合成的图片储存到内存中
            result = BytesIO()
            background.save(result, format="PNG")
            return result.getvalue()

        else:
            return "请输入正确的城市名"
