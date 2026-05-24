#######################匯入模組#######################
import requests


#######################定義類別########################
# 這份類別可以看成是把第一次實作天氣功能的主程式流程拆開整理。
# 原本查看天氣的功能是寫在主程式裡的，現在我們把它拆成一個類別，這樣可以讓程式碼更有結構，也更容易維護。
# 現在改成一個方法處理一個事件，這樣可以讓程式碼更清晰，也更容易測試。
class WearherAPI:
    """把 OpenWeatherMap API 的功能包裝成一個工具類別(可重複使用)"""

    def __init__(self, api_key, lang="zh_tw"):
        # __init__() 是一個特殊的方法，當我們建立一個類別的實例時，這個方法會被自動呼叫，用來初始化這個實例的屬性(負責初始化類別共用設定)
        # 這樣就不用在主程式裡面定義這些常數了，這些常數現在都變成了類別的屬性，可以在類別的其他方法裡面使用
        # 現在查詢時都只要重新處理 API_KEY、BASE_URL、ICON_URL、UNITS、LANG 這些參數就好，其他的程式碼都不用改了，這樣就達到了程式碼的重用性，也讓主程式更簡潔了
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.icon_base_url = "http://openweathermap.org/img/wn/"
        self.units = "metric"
        self.lang = lang

    def get_current_weather(self, city_name):
        # get_weather_info() 是我們定義的一個方法，這個方法的功能是根據城市名稱查詢天氣資訊，並且返回一個字典，這個字典裡面包含了我們需要的天氣資訊，例如溫度、濕度、風速等等
        # 這樣就把查詢天氣的功能封裝成一個方法了，當我們需要查詢天氣時，只要呼叫這個方法，傳入城市名稱，就可以得到天氣資訊了，這樣就達到了程式碼的重用性，也讓主程式更簡潔了
        send_url = f"{self.base_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        return response.json()

    def get_icon_url(self, icon_code):
        # 組出天氣圖片網址
        return f"{self.icon_base_url}{icon_code}@4x.png"

    def get_weather_summary(self, city_name):
        # 查詢目前天氣，整理成更容易閱讀的格式，並且回傳一個字串
        info = self.get_current_weather(city_name)

        if "weather" in info and "main" in info:
            return {
                "city_name": info.get("name", city_name),
                "temperature_celsius": round(info["main"].get("temp"), 2),
                "description": info["weather"][0]["description"],
                "icon_code": info["weather"][0]["icon"],
            }

        return None

    def get_icon(self, icon_code):
        # 抓出天氣圖示的圖片資料
        icon_url = self.get_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.status_code == 200:
            return response.content  # 回傳圖片的二進位資料
        else:
            return None  # 如果圖片下載失敗，回傳 None


#######################建立視窗########################

#######################運行應用程式########################
