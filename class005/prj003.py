#######################匯入模組#######################
import requests  # 匯入requests模組，用於發送HTTP請求(先安裝requests模組：pip install requests)

#######################定義常數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"  # KEY
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"  # URL
UNITS = "metric"  # 定義一個常數UNITS，表示使用公制單位（攝氏度）
LANG = "zh_tw"  # 定義一個常數LANG，表示使用中文語言
#######################建立視窗########################

#######################運行應用程式########################
city_name = input(
    "請輸入城市名稱: "
)  # 提示用戶輸入城市名稱，並將輸入的值存儲在city_name變量中
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"  # 根據API的要求構建完整的URL，將城市名稱、API密鑰、單位和語言參數添加到URL中

print(f"發送的URL: {send_url}")  # 打印發送的URL，這樣可以幫助我們檢查URL是否正確構建
response = requests.get(
    send_url
)  # 使用requests模組的get方法發送HTTP請求，並將響應存儲在response變量中
info = response.json()  # 將響應的JSON數據解析為Python字典，並存儲在info變量中
