#######################匯入模組#######################
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機
import sys
import os

#######################設定工作目錄########################
os.chdir(
    sys.path[0]
)  # 設定工作目錄為當前腳本所在的目錄，這樣在打開文件對話框時就會從這個目錄開始


#######################定義函數########################
def show_result():
    entry_text = entry.get()  # 獲取Entry物件中的文本，這裡假設Entry物件的名字是entry
    try:
        result = eval(
            entry_text
        )  # 使用eval函數計算Entry物件中的文本，這裡假設文本是一個有效的Python表達式
        label.config(text=f"計算結果: {result}")  # 更新label的文本為計算結果
    except:
        result = "計算錯誤"  # 如果計算過程中出現錯誤，將result設置為"無效的表達式"
        label.config(text=result)  # 更新label的文本為錯誤信息


#######################建立視窗########################

window = Tk()  # 建立一個新的視窗
window.title("My  GUI")  # 設定視窗的標題（顯示在視窗上方）
#######################設定字型########################
font_size = 20  # 定義字型大小為20
window.option_add(
    "*font", ("Arial", font_size)
)  # 設定視窗中所有元件的字型為Arial，大小為font_size
#######################設定主題########################
style = Style(
    theme="cyborg"
)  # 設定主題為cyborg，這是一個ttkbootstrap提供的主題，可以讓應用程序看起來更現代化和美觀
style.configure(
    "my.TButton", font=("Arial", font_size)
)  # 定義一個名為"my.TButton"的樣式，字型為Arial，大小為20，字體顏色為紅色
#######################建立標籤#######################
label = Label(window, text="計算解果")  # 建立一個標籤，顯示文本"Hello, World!"
label.grid(
    row=2, column=0, columnspan=2, padx=10, pady=10
)  # padx=10, pady=10表示在標籤周圍添加10像素的水平和垂直內邊距，這樣可以讓標籤與其他元件之間有一些空隙，使界面看起來更整潔
#######################建立按鈕#######################
# 顯示計算解果按鈕
button = Button(
    window, text="顯示計算解果", style="my.TButton", command=show_result
)  # 建立一個按鈕，顯示文本"瀏覽"，使用"my.TButton"樣式
button.grid(
    row=1, column=0, columnspan=2, padx=10, pady=10
)  # 使用grid佈局管理器將按鈕放置在第一行第二列，sticky="W"表示將按鈕靠左對齊
#######################建立Entry物件#######################
# Entry物件是一個用於接收用戶輸入的文本框，可以讓用戶在其中輸入數據，然後我們可以通過程式碼來獲取這些數據並進行處理。
entry = Entry(window, width=30)  # 建立一個Entry物件，這是一個
entry.grid(
    row=0, column=0, columnspan=2, padx=10, pady=10
)  # 使用grid佈局管理器將Entry物件放置在第二行第一列，並合併兩列，padx=10, pady=10表示在Entry物件周圍添加10像素的水平和垂直內邊距
#######################運行應用程式########################
window.mainloop()
