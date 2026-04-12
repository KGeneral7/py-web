#######################匯入模組#######################
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機執行這行命令安裝ttkbooststrap庫，ttkbooststrap是基於tkinter的GUI框架，提供了更多的主題和樣式選項，可以讓開發者更輕鬆地創建美觀的GUI應用程序)
import sys
import os
from tkinter import (
    filedialog,
)  # 匯入filedialog模組，這個模組提供了文件對話框的功能，可以讓用戶選擇文件或目錄
from PIL import (
    Image,
    ImageTk,
)  # pip install Pillow -U(在終端機執行這行命令安裝Pillow庫，Pillow是Python Imaging Library的分支，提供了圖像處理功能，可以讓開發者輕鬆地打開、操作和保存各種圖像格式)


#######################定義函數########################
def open_file():
    global file_path  # 定義一個全局變量file_path，用於存儲選擇的文件路徑
    file_path = filedialog.askopenfilename(
        initialdir=sys.path[0]
    )  # 打開文件對話框，讓用戶選擇一個文件，並將選擇的文件路徑存儲在file_path變量中
    label2.config(text=file_path)  # 更新label2的文本為選擇的文件路徑


def show_image():
    global file_path  # 定義一個全局變量file_path，用於存儲選擇的文件路徑
    image = Image.open(
        file_path
    )  # 使用Pillow庫的Image模組打開選擇的圖像文件，並將圖像對象存儲在image變量中
    # 調整圖片大小，讓它適應畫布的大小
    # Image.LANCZOS 是一種高質量的重採樣濾波器，適用於縮小圖像時，可以保持圖像的細節和清晰度(會仔細把顏色混和好，讓圖片縮小後還是清楚好看，不會變得糊糊或鋸齒狀)
    image = image.resize(
        (canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS
    )  # 調整圖像的大小，使其適應畫布的寬度和高度
    # 轉換成tkinter可以顯示的格式
    photo = ImageTk.PhotoImage(
        image
    )  # 將Pillow圖像對象轉換為Tkinter可以顯示的圖像對象，並將其存儲在image_tk變量中
    # 在畫布上顯示圖片，圖片左上角會對齊畫布的左上角
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo  # 將image_tk存儲在canvas的image屬性中，這樣可以防止圖像被垃圾回收機制回收，確保圖像在畫布上持續顯示


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
label = Label(window, text="選擇檔案:")  # 建立一個標籤，顯示文本"Hello, World!"
label.grid(
    row=0, column=0, sticky="E"
)  # 使用grid佈局管理器將標籤放置在第一行第一列，sticky="W"表示將標籤靠左對齊

label2 = Label(window, text="無")  # 建立一個標籤，顯示文本"Hello, World!"
label2.grid(
    row=0, column=1, sticky="E"
)  # 使用grid佈局管理器將標籤放置在第一行第一列，sticky="W"表示將標籤靠左對齊
#######################建立按鈕########################
button = Button(
    window, text="瀏覽", style="my.TButton", command=open_file
)  # 建立一個按鈕，顯示文本"瀏覽"，使用"my.TButton"樣式
button.grid(
    row=0, column=2, sticky="E"
)  # 使用grid佈局管理器將按鈕放置在第一行第二列，sticky="W"表示將按鈕靠左對齊

button2 = Button(
    window, text="顯示", command=show_image, style="my.TButton"
)  # 建立一個按鈕，顯示文本"下載"，使用"my.TButton"樣式
button2.grid(
    row=1, column=0, columnspan=3, sticky="EW"
)  # 使用grid佈局管理器將按鈕放置在第一行(col)第零列(row)，再決定要幾個col合併起來(columnspan2)，sticky="EW"表示將按鈕靠中間對齊

canvas = Canvas(
    window, width=600, height=600
)  # 建立一個畫布，寬度為400像素，高度為400像素
canvas.grid(
    row=2, column=0, columnspan=3
)  # 使用grid佈局管理器將畫布放置在第三行第一列，並合併三列
#######################運行應用程式########################
window.mainloop()
