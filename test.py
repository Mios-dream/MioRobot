import requests
import re
import json


city = "重庆"
data = requests.get(f"https://weather.cma.cn/api/autocomplete?q={city}&limit=10")
data = data.json()["data"][0].split("|")
if data[3] != "中国":
    pass

else:
    web_page = requests.get(f"https://weather.cma.cn/web/weather/{data[0]}.html")

    data = web_page.content.decode("utf-8")
    weather_7days = re.findall(r'<div class="day-item">(([\s\S])*?)</div>', data)
    print(weather_7days)
    with open("weather.json", "w+", encoding="utf-8") as f:
        json.dump(weather_7days, f, ensure_ascii=False)
