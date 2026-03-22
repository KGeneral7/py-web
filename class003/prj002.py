#######################匯入模組#######################
# 從 tkinter 模組中匯入所有功能（*代表全部）
from tkinter import *
import sys
import os
from PIL import Image, ImageTk

# pip install pillow(在終端機執行這行命令安裝Pillow庫，Pillow是Python Imaging Library的分支，提供了更多的圖像處理功能和支持更多的圖像格式)
#######################設定工作目錄#######################
os.chdir(sys.path[0])  # 設定工作目錄為當前腳本所在的目錄
"""
 sys.path[0]會返回當前腳本所在的目錄路徑，os.chdir()函數用於更改當前工作目錄，
 因此這行代碼的作用是將工作目錄設置為當前腳本所在的目錄，
 這樣在後續的文件操作中就可以使用相對路徑來訪問文件，而不需要擔心當前工作目錄的問題
shdir為change directory的縮寫，表示更改目錄。
這行代碼的作用是將當前工作目錄更改為當前腳本所在的目錄，
這樣在後續的文件操作中就可以使用相對路徑來訪問文件，
而不需要擔心當前工作目錄的問題   
"""


#######################定義函數########################
# 定義一個函數，用於移動圓形
def move_circle(
    event,
):  # bind_all("<Key>",move_circle)綁定鍵盤事件，當按下任意鍵時，觸發move_circle函數(回傳event物件，包含按鍵的相關資訊)
    # 取得按鍵的名稱
    key = event.keysym
    print(f"按下了 {key} 鍵")
    # 根據按鍵的名稱來移動圓形
    if key == "Up":
        canvas.move(circle, 0, -10)  # 向上移動圓形，x方向不變，y方向減少10像素
    elif key == "Down":
        canvas.move(circle, 0, 10)  # 向下移動圓形，x方向不變，y方向增加10像素
    elif key == "Left":
        canvas.move(circle, -10, 0)  # 向左移動圓形，x方向減少10像素，y方向不變
    elif key == "Right":
        canvas.move(circle, 10, 0)  # 向右移動圓形，x方向增加10像素，y方向不變


#######################建立視窗########################
# 建立一個新的視窗
window = Tk()
# 設定視窗的標題（顯示在視窗上方）
window.title("My first GUI")
canvas = Canvas(window, width=400, height=300, bg="white")
canvas.pack()
#######################建立畫布########################
# 設定視窗圖片
window.iconbitmap("crocodile2.ico")  # 設定視窗的圖標，文件名為"crocodile.ico"
#######################載入圖片########################
"""原始:
        # tkinter內建的PhotoImage類別用於載入和顯示圖片，支持的格式:PNG、GIF和PPM、PGM(不支持JPEG、JPG等格式)
        img = PhotoImage(
            file="crocodile2.png"
        )  # 載入圖片，文件名為"crocodile.png"，並將其存儲在變量img中
"""
# 使用pillow庫載入圖片，支持更多的圖像格式
# pillow的好處:支持更多的圖像格式（如JPEG、BMP等），提供了更多的圖像處理功能（如旋轉、縮放、裁剪等），並且在性能方面也有優化。
# 可以在顯示前對圖像進行處理，例如調整大小、旋轉、裁剪等，這些功能在Tkinter的PhotoImage中是有限的。
img = Image.open("crocodile2.png")  # 載入圖片
img = img.resize((200, 150))  # 調整圖片大小為200x150像素
img = ImageTk.PhotoImage(img)  # 將Pillow圖像轉換為Tkinter可用的格式
# 注意:需保留對img的參照，否則圖片可能不會顯示，因為Python的垃圾回收機制可能會回收掉img對象，導致圖片無法顯示。
#######################畫圖形########################
circle = canvas.create_oval(
    50, 50, 150, 150, fill="red"
)  # 在畫布上繪製一個紅色的圓形，位置為(50, 50)到(150, 150)
rect = canvas.create_rectangle(
    250, 50, 350, 150, fill="blue"
)  # 在畫布上繪製一個藍色的矩形，位置為(250, 50)到(350, 150)
msg = canvas.create_text(
    200, 250, text="Hello, World!", font=("Arial", 20), fill="green"
)  # 在畫布上繪製一段文字，位置為(200, 250)，文字內容為"Hello, World!"，字體為Arial，大小為20，顏色為綠色
#######################綁定按鈕事件########################
canvas.bind_all(
    "<Key>", move_circle
)  # 綁定鍵盤事件，當按下任意鍵時，觸發move_circle函數
#######################放上畫布########################
my_img = canvas.create_image(
    200, 150, image=img
)  # 在畫布上放置圖片，位置為(200, 150)，即畫布的中心

#######################運用應用程式########################

window.mainloop()
