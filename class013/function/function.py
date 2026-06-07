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
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"
        self.icon_base_url = "http://openweathermap.org/img/wn/"
        self.units = "metric"
        self.lang = lang

    def get_current_weather(self, city_name):
        # get_weather_info() 是我們定義的一個方法，這個方法的功能是根據城市名稱查詢天氣資訊，並且返回一個字典，這個字典裡面包含了我們需要的天氣資訊，例如溫度、濕度、風速等等
        # 這樣就把查詢天氣的功能封裝成一個方法了，當我們需要查詢天氣時，只要呼叫這個方法，傳入城市名稱，就可以得到天氣資訊了，這樣就達到了程式碼的重用性，也讓主程式更簡潔了
        send_url = f"{self.base_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        response.raise_for_status()  # 檢查 API 回應的狀態碼，如果狀態碼不是 200，這個方法就會拋出一個 HTTPError 異常，這樣我們就可以知道我們的 API 請求是否成功了，如果成功了，我們就可以繼續處理回應的資料了
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

    def get_forecast(self, city_name):
        # 查詢天氣預報，整理成更容易閱讀的格式，並且回傳一個字串
        send_url = f"{self.forecast_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        response.raise_for_status()  # 檢查 API 回應的狀態碼，如果狀態碼不是 200，這個方法就會拋出一個 HTTPError 異常，這樣我們就可以知道我們的 API 請求是否成功了，如果成功了，我們就可以繼續處理回應的資料了
        return response.json()

    def get_forecast_summary(self, city_name, count=10):
        """查詢天氣預報，整理成更容易閱讀的格式，並且回傳一個字串"""
        # 這裡和 get_weather_summary的邏輯差不多，只是這裡我們處理的是天氣預報的資料，
        # 所以我們從 API 回應的資料裡面取出預報的列表，然後把每個預報的日期、溫度、天氣描述等等資訊整理成一個字串，
        # 最後把這些字串組合成一個完整的預報摘要字串，這樣就可以讓使用者更容易閱讀了
        forecast_count = max(0, count)
        try:
            info = self.get_forecast(city_name)
        except requests.HTTPError as error:
            response = error.response
            if response is not None and response.status_code == 404:
                return None
            raise  # 只把錯誤訊息傳出去，不處理錯誤，這樣就可以讓這個類別更專注於它的功能了(只提供錯誤訊息，不中斷程式)
        if "city" not in info or "list" not in info:
            return None

        city_label = info["city"].get("name", city_name)
        forecast_summary = []

        for forecast in info["list"][:forecast_count]:
            #:forecast_count的:很像range的用法，但是出來的不是數字，而是小字典，這裡我們從預報列表中取出前 forecast_count 個預報，然後對每個預報進行處理，最後把處理好的預報資訊存儲在 forecast_summary 這個列表裡面，這樣就可以讓使用者更容易閱讀了
            forecast_summary.append(
                {
                    "city_name": city_label,
                    "datetime": forecast.get("dt_txt"),
                    "temperature_celsius": round(forecast["main"].get("temp"), 2),
                    "description": forecast["weather"][0].get("description"),
                    "icon_code": forecast["weather"][0].get("icon"),
                }
            )

        return forecast_summary


#######################建立視窗########################

#######################運行應用程式########################
