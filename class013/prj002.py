from dotenv import load_dotenv
import requests
import os

load_dotenv()  # 從 .env 文件中讀取環境變數(在這裡是讀取 DISCORD_TOKEN等東西)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
UNITS = "metric"  # 使用公制單位，這樣溫度就會以攝氏度顯示
LANGUAGE = "zh_tw"  # 使用中文語言，這樣天氣描述就會以中文顯示

city_name = "Taipei"  # 你想要查詢天氣的城市名稱
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANGUAGE}"  # 組合成完整的 API 請求 URL，這裡我們把 BASE_URL、城市名稱、API 金鑰、單位和語言參數組合成一個完整的 URL，這樣我們就可以使用這個 URL 來向 OpenWeatherMap API 發送請求了

print(f"發送URL:{send_url}")
# 印出組合好的 URL，這樣我們就可以確認我們的 URL 是正確的了，這裡我們使用了 f-string 來格式化字串，這樣就可以直接在字串中插入變數了

responce = requests.get(
    send_url
)  # 向 OpenWeatherMap API 發送 GET 請求，這裡我們使用了 requests 庫來發送 HTTP 請求，當我們呼叫 requests.get() 方法時，我們把組合好的 URL 傳遞給它，這樣它就會向 OpenWeatherMap API 發送一個 GET 請求，然後把 API 的回應存儲在 response 變數中
print(f"回應狀態碼:{responce.status_code}")
responce.raise_for_status()
# 檢查 API 回應的狀態碼，如果狀態碼不是 200，這個方法就會拋出一個 HTTPError 異常，這樣我們就可以知道我們的 API 請求是否成功了，如果成功了，我們就可以繼續處理回應的資料了
info = responce.json()
# 把 API 回應的資料解析成 JSON 格式，這裡我們使用了 response.json() 方法來把 API 回應的資料解析成一個 Python 字典，這樣我們就可以方便地從這個字典中獲取我們需要的天氣資訊了

if "city" in info:
    print(f"城市名稱:{info['city']['name']}")
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]  # 預報的日期和時間
        temp = forecast["main"]["temp"]  # 預報的溫度
        weather_description = forecast["weather"][0]["description"]
        # 預報的天氣描述，這裡我們取了 weather 陣列中的第一個元素，然後從這個元素中取出了 description 欄位，這樣就可以獲取到天氣的描述了
        print(dt_txt, temp, weather_description)
