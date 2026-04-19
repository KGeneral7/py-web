#######################匯入模組#######################
import requests  # 匯入requests模組，用於發送HTTP請求(先安裝requests模組：pip install requests)
import sys
import os

#######################定義常數########################
API_KEY = "5bcad7fe1640dbdb54f65ae164eda027"  # KEY
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"  # URL
ICON_URL = "http://openweathermap.org/img/wn/"  # 圖示URL
UNITS = "metric"  # 定義一個常數UNITS，表示使用公制單位（攝氏度）
LANG = "zh_tw"  # 定義一個常數LANG，表示使用中文語言
#######################建立視窗########################

#######################運行應用程式########################
os.chdir(
    sys.path[0]
)  # 將當前工作目錄更改為腳本所在的目錄，這樣可以確保在運行腳本時能夠正確找到相關文件
city_name = input(
    "請輸入城市名稱: "
)  # 提示用戶輸入城市名稱，並將輸入的值存儲在city_name變量中
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"  # 根據API的要求構建完整的URL，將城市名稱、API密鑰、單位和語言參數添加到URL中

print(f"發送的URL: {send_url}")  # 打印發送的URL，這樣可以幫助我們檢查URL是否正確構建
response = requests.get(
    send_url
)  # 使用requests模組的get方法發送HTTP請求，並將響應存儲在response變量中
info = response.json()  # 將響應的JSON數據解析為Python字典，並存儲在info變量中
# 處理顯示資料
if not (
    info.get("cod") == "404"
):  # 檢查info字典中的"cod"鍵是否等於"404"，如果不等於"404"，表示城市存在，繼續處理資料
    current_temperature = info["main"]["temp"]  # 從info字典中提取當前溫度
    weather_description = info["weather"][0]["description"]  # 從info字典中提取天氣描述
    icon_code = info["weather"][0]["icon"]  # 從info字典中提取天氣圖示代碼
    print(f"城市名稱: {city_name}")  # 打印城市名稱
    print(f"{city_name}的當前溫度: {current_temperature}°C")  # 打印當前溫度
    print(f"{city_name}的天氣描述: {weather_description}")  # 打印天氣描述
    # 根據圖標代碼構建圖標URL
    icon_url = f"{ICON_URL}{icon_code}@4x.png"  # 根據圖標代碼構建圖標URL，使用@4x表示使用高解析度的圖標
    # 從圖標URL下載圖標並保存到本地
    print(f"圖標URL: {icon_url}")  # 打印圖標URL，這樣可以幫助我們檢查URL是否正確構建
    icon_response = requests.get(icon_url)  # 使用requests模組的get方法下載
    # 若成功下載圖標，則將其保存到本地
    if icon_response.status_code == 200:  # 檢查圖標下載是否成功，HTTP狀態碼200表示成功
        with open(
            f"{city_name}_weather_icon.png", "wb"
        ) as icon_file:  # 打開一個新的文件(用open())，以[二進制寫入模式]保存圖標(二進位模式為wb)
            # with是一個上下文管理器，確保在完成文件操作後自動關閉文件
            icon_file.write(icon_response.content)  # 將下載的圖標內容寫入文件中
            # content裡面是圖標的二進制數據，write()將其寫入文件中
        print(f"圖標已保存為 {city_name}_weather_icon.png")  # 打印成功保存圖標的消息
    else:
        print(
            f"無法下載圖標，HTTP狀態碼: {icon_response.status_code}"
        )  # 如果圖標下載失敗，打印錯誤信息和HTTP狀態碼
else:
    print(
        f"城市 {city_name} 不存在，請檢查輸入是否正確。"
    )  # 如果城市不存在，打印錯誤信息
