#######################匯入模組#######################
import requests  # 匯入requests模組，用於發送HTTP請求(先安裝requests模組：pip install requests)
import sys
import os
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機
from PIL import Image, ImageTk  # pip install Pillow(在終端機)
from tkinter import messagebox  # 匯入messagebox模組，用於顯示消息框

#######################定義常數########################
API_KEY = "5bcad7fe1640dbdb54f65ae164eda027"  # KEY
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"  # URL
ICON_URL = "http://openweathermap.org/img/wn/"  # 圖示URL
UNITS = "metric"  # 定義一個常數UNITS，表示使用公制單位（攝氏度）
LANG = "zh_tw"  # 定義一個常數LANG，表示使用中文語言
os.chdir(
    sys.path[0]
)  # 將當前工作目錄更改為腳本所在的目錄，這樣可以確保在運行腳本時能夠正確找到相關文件
#######################建立視窗########################
window = Tk()  # 建立一個新的視窗
window.title("wather")  # 設定視窗的標題（顯示在視窗上方）
#######################建立變數########################
check_type = (
    StringVar()
)  # 建立一個BooleanVar變數，用於存儲CheckButton的選擇狀態(ttk用來存儲CheckButton的狀態，BooleanVar用來存儲布林值)
check_type.set(
    "攝氏"
)  # 設定check_type變數的初始值為True，表示CheckButton默認為未選中狀態
#######################設定字型########################
font_size = 20  # 定義字型大小為20
window.option_add(
    "*font", ("Arial", font_size)
)  # 設定視窗中所有元件的字型為Arial，大小為font_size
style = Style(
    theme="cyborg"
)  # 設定主題為cyborg，這是一個ttkbootstrap提供的主題，可以讓應用程序看起來更現代化和美觀
style.configure(
    "my.TButton", font=("Arial", font_size)
)  # 定義一個名為"my.TButton"的樣式，字型為Arial，大小為20，字體顏色為紅色


#######################定義函數########################
def on_switch_change():
    # 當CheckButton的狀態改變時，將check_type的值轉換為字符串並顯示在Check_label標籤上
    Check_label.config(text=str(check_type.get()))  # 更新Check_label的文本為check


def wather_info():
    if (
        not entry.get().strip()
    ):  # 檢查Entry物件中的文本是否為空，如果為空，則顯示一個錯誤消息框，提示用戶輸入城市名稱
        messagebox.showerror(
            "錯誤", "請輸入城市名稱！"
        )  # 顯示一個錯誤消息框，標題為"錯誤"，內容為"請輸入城市名稱！"
        return  # 結束函數的執行，返回到調用函數的位置
    city_name = (
        entry.get()
    )  # 從Entry物件中獲取用戶輸入的城市名稱，這裡假設Entry物件的名字是city_name
    send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"  # 根據API的要求構建完整的URL，將城市名稱、API密鑰、單位和語言參數添加到URL中

    print(
        f"發送的URL: {send_url}"
    )  # 打印發送的URL，這樣可以幫助我們檢查URL是否正確構建
    response = requests.get(
        send_url
    )  # 使用requests模組的get方法發送HTTP請求，並將響應存儲在response變量中
    info = response.json()  # 將響應的JSON數據解析為Python字典，並存儲在info變量中
    # 處理顯示資料
    if not (
        info.get("cod") == "404"
    ):  # 檢查info字典中的"cod"鍵是否等於"404"，如果不等於"404"，表示城市存在，繼續處理資料
        current_temperature = info["main"]["temp"]  # 從info字典中提取當前溫度
        weather_description = info["weather"][0][
            "description"
        ]  # 從info字典中提取天氣描述
        icon_code = info["weather"][0]["icon"]  # 從info字典中提取天氣圖示代碼
        print(f"城市名稱: {city_name}")  # 打印城市名稱
        print(f"{city_name}的當前溫度: {current_temperature}°C")  # 打印當前溫度
        print(f"{city_name}的天氣描述: {weather_description}")  # 打印天氣描述
        if (
            check_type.get() == "華氏"
        ):  # 如果check_type的值為"華氏"，則將攝氏溫度轉換為華氏溫度
            current_temperature = current_temperature * 9 / 5 + 32
            unit = "°F"
        else:
            unit = "°C"

        label_temp.config(text=f"溫度：{current_temperature:.1f}{unit}")
        label_desc.config(text=f"描述：{weather_description}")
        # 根據圖標代碼構建圖標URL
        icon_url = f"{ICON_URL}{icon_code}@4x.png"  # 根據圖標代碼構建圖標URL，使用@4x表示使用高解析度的圖標
        # 從圖標URL下載圖標並保存到本地
        print(
            f"圖標URL: {icon_url}"
        )  # 打印圖標URL，這樣可以幫助我們檢查URL是否正確構建
        icon_response = requests.get(icon_url)  # 使用requests模組的get方法下載
        # 若成功下載圖標，則將其保存到本地
        if (
            icon_response.status_code == 200
        ):  # 檢查圖標下載是否成功，HTTP狀態碼200表示成功
            with open(
                f"{city_name}_weather_icon.png", "wb"
            ) as icon_file:  # 打開一個新的文件(用open())，以[二進制寫入模式]保存圖標(二進位模式為wb)
                # with是一個上下文管理器，確保在完成文件操作後自動關閉文件
                icon_file.write(icon_response.content)  # 將下載的圖標內容寫入文件中
                # content裡面是圖標的二進制數據，write()將其寫入文件中
            print(
                f"圖標已保存為 {city_name}_weather_icon.png"
            )  # 打印成功保存圖標的消息
            image = Image.open(
                f"{city_name}_weather_icon.png"
            )  # 讀取名為gay_weather_icon.png的圖片
            weather_photo = ImageTk.PhotoImage(image)
            label3.config(image=weather_photo)  # 更新label3的圖像為下載的天氣圖示
            label3.image = weather_photo  # 將weather_photo對象存儲在label3的image屬性中，這樣可以防止圖片被垃圾回收
        else:
            print(
                f"無法下載圖標，HTTP狀態碼: {icon_response.status_code}"
            )  # 如果圖標下載失敗，打印錯誤信息和HTTP狀態碼
            # 另一種處理方式：
            # weather_photo.raise_for_status()
            # from io import BytesIO
            # image = Image.open(BytesIO(icon_response.content))
    else:
        print(
            f"城市 {city_name} 不存在，請檢查輸入是否正確。"
        )  # 如果城市不存在，打印錯誤信息


def wather_info2():
    wather_info()
    on_switch_change()


#######################建立UI佈局########################
window.geometry("760x380")
window.resizable(False, False)

header_frame = Frame(window)
header_frame.pack(fill="x", padx=16, pady=12)
header_frame.columnconfigure(1, weight=1)

label1 = Label(header_frame, text="請輸入想搜尋的城市：")
label1.grid(row=0, column=0, sticky="w")

entry = Entry(header_frame, width=28)
entry.grid(row=0, column=1, padx=10, sticky="we")
entry.focus()

button = Button(
    header_frame,
    text="獲得天氣資訊",
    bootstyle="success",
    command=wather_info,
)
button.grid(row=0, column=2, padx=10, sticky="e")

result_frame = Frame(window)
result_frame.pack(fill="both", expand=True, padx=16, pady=8)

result_frame.columnconfigure(0, weight=0)
result_frame.columnconfigure(1, weight=1)

icon_frame = Frame(result_frame, width=260, height=260)
icon_frame.grid(row=0, column=0, sticky="nw", padx=(0, 18))
icon_frame.grid_propagate(False)

label3 = Label(
    icon_frame, text="天氣圖示", width=12, compound="center", anchor="center"
)
label3.pack(expand=True, pady=16)

info_frame = Frame(result_frame)
info_frame.grid(row=0, column=1, sticky="nsew")
info_frame.columnconfigure(0, weight=1)
info_frame.columnconfigure(1, weight=1)

label_temp = Label(
    info_frame,
    text="溫度：",
    justify="left",
    anchor="w",
)
label_temp.grid(row=0, column=0, sticky="w", padx=(8, 4), pady=(0, 4))

label_desc = Label(
    info_frame,
    text="描述：",
    justify="left",
    anchor="w",
)
label_desc.grid(row=0, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

check_button = Checkbutton(
    info_frame,
    variable=check_type,
    onvalue="攝氏",
    offvalue="華氏",
    command=wather_info2,
    text="華氏/攝氏",
    bootstyle="info",
)
check_button.grid(row=1, column=0, columnspan=2, sticky="w", pady=(12, 4))

Check_label = Label(info_frame, text="攝氏")
Check_label.grid(row=2, column=0, columnspan=2, sticky="w")

#######################運行應用程式########################
window.mainloop()  # 啟動視窗的主事件循環，讓視窗
