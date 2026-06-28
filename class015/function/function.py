#######################匯入模組#######################
import requests
import openai  # pip install openai(在終端機);此模組是用來與 OpenAI 進行互動的主要工具


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


class AIAssistant:
    """把 OpenAI API 的功能包裝成一個工具類別(可重複使用)"""

    def __init__(self, api_key):  # 初始化 OpenAI的設定
        self.api_key = (
            api_key  # 把API_KEY存成類別的屬性，這樣就可以在類別的其他方法裡面使用了
        )
        openai.api_key = (
            self.api_key
        )  # 把API_KEY設定給openai模組，這樣我們就可以使用openai模組提供的功能了

    def ask(
        self,
        system_prompt,
        user_message,
        history_message=None,
        temperature=1,
        model="gpt-5.5",
    ):
        """進行一次AI對話，也可以帶入整理好的話紀錄"""
        # 這個方法讓我們可以問AI一個問題，並得到一次性回應
        # system_prompt是我們給AI的指令，告訴AI我們希望它怎麼回答，user_message是我們問AI的問題，temperature是控制AI回答的隨機程度，model是我們使用的AI模型，history_message是我們之前的對話紀錄，這樣我們就可以讓AI在回答問題的時候參考之前的對話紀錄了，這樣就可以讓AI的回答更有連貫性了

        # 如果沒有設定金鑰，直接回傳錯誤訊息
        if not self.api_key:
            return (
                None,
                "Error: OpenAI API key is not set.請先在.env檔案裡面設定OPENAI_API_KEY，然後重新啟動程式。",
            )

        if history_message is None:
            history_message = (
                []
            )  # 如果沒有提供對話紀錄，就使用一個空的列表，這樣就不會有對話紀錄了，這樣就可以讓這個方法更靈活了，因為有些時候我們可能不需要對話紀錄，只想要問AI一個問題，那麼我們就可以直接呼叫這個方法，而不需要提供對話紀錄了

        # messages的順序很重要:
        # 1. system_prompt: 這是給AI的指令，告訴AI我們希望它怎麼回答，這個訊息會影響AI的回答風格和內容，所以我們要把它放在第一個位置，讓AI先知道我們的要求。
        # 2. history_message: 這是之前的對話紀錄，這個訊息會讓AI知道之前的對話內容，這樣AI在回答問題的時候就可以參考之前的對話紀錄了，這樣就可以讓AI的回答更有連貫性了，所以我們要把它放在第二個位置，讓AI在知道我們的要求之後，再來處理之前的對話紀錄。
        # 3. user_message: 這是我們問AI的問題，這個訊息會讓AI知道我們現在想要問什麼問題，所以我們要把它放在最後一個位置，讓AI在知道我們的要求和之前的對話紀錄之後，再來處理我們現在的問題。

        input_messages = history_message + [{"role": "user", "content": user_message}]

        print("####Messages sent to OpenAI API:####")
        print(f"system:{system_prompt}")
        for msg in input_messages:
            print(f"{msg['role']}: {msg['content']}")
        print("####End of messages####")
        try:
            # 向 OPENAI API 發送請求
            response = openai.responses.create(
                model=model,
                instructions=system_prompt,
                input=input_messages,
                tools=[{"type": "web_search"}],
                tool_choice="auto",
            )

            # 從 API 回應中取出 AI 的回答
            assistant_message = response.output_text

            return assistant_message, None  # 回傳 AI 的回答和 None 表示沒有錯誤

        except Exception as e:
            return (
                None,
                f"Error: {e}",
            )  # 如果OPENAI呼叫失敗，回傳 None 表示沒有回答，和錯誤訊息
