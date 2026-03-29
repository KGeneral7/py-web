#######################匯入模組#######################
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機執行這行命令安裝ttkbooststrap庫，ttkbooststrap是基於tkinter的GUI框架，提供了更多的主題和樣式選項，可以讓開發者更輕鬆地創建美觀的GUI應用程序)
import sys
import os


#######################定義函數########################
def test():
    print("test")


#######################建立視窗########################
window = Tk()  # 建立一個新的視窗
window.title("My first GUI")  # 設定視窗的標題（顯示在視窗上方）
#######################設定字型########################
font_size = 20  # 定義字型大小為20
window.option_add(
    "*font", ("Arial", font_size)
)  # 設定視窗中所有元件的字型為Arial，大小為font_size
#######################設定主題########################
style = Style(
    theme="cyborg"
)  # 設定主題為cyborg，這是一個ttkbootstrap提供的主題，可以讓應用程序看起來更現代化和美觀
# "my.TButton"的命名邏輯:
# 就像是幫東西貼一個標籤一樣，分成兩個部分，用"."隔開:
#   前半段"my"  ->自己取的名字，可以換成其他的任何名字，這裡用"my"表示這是一個自定義的樣式
#   後半段"TButton" -> ttkbootstrap中定義的元件類型，這裡是TButton，表示這個樣式是用於按鈕的
#                      T是Ttk(一種按鈕工具箱)的縮寫
#                      就像的品牌一樣，T是品牌名的開頭字母
# 常見元件後半段寫法:
#   按鈕 -> TButton 標籤 -> TLabel 輸入框 -> TEntry
style.configure(
    "my.TButton", font=("Arial", font_size)
)  # 定義一個名為"my.TButton"的樣式，字型為Arial，大小為20，字體顏色為紅色
#######################建立標籤########################
label = Label(window, text="Hello, World!")  # 建立一個標籤，顯示文本"Hello, World!"
label.grid(
    row=0, column=0, sticky="W"
)  # 使用grid佈局管理器將標籤放置在第一行第一列，sticky="W"表示將標籤靠左對齊
#######################建立按鈕########################
button = Button(
    window, text="瀏覽", style="my.TButton", command=test
)  # 建立一個按鈕，顯示文本"瀏覽"，使用"my.TButton"樣式
button.grid(
    row=0, column=1, sticky="W"
)  # 使用grid佈局管理器將按鈕放置在第一行第二列，sticky="W"表示將按鈕靠左對齊
button2 = Button(
    window, text="顯示", command=test, style="my.TButton"
)  # 建立一個按鈕，顯示文本"下載"，使用"my.TButton"樣式
button2.grid(
    row=1, column=0, columnspan=2, sticky="EW"
)  # 使用grid佈局管理器將按鈕放置在第一行(col)第零列(row)，再決定要幾個col合併起來(columnspan2)，sticky="EW"表示將按鈕靠中間對齊
#######################運行應用程式########################
window.mainloop()
