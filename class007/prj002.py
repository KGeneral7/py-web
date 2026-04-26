#######################匯入模組#######################
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機
import sys
import os
from PIL import Image, ImageTk  # pip install Pillow(在終端機)

#######################設定工作目錄########################
os.chdir(
    sys.path[0]
)  # 將當前工作目錄更改為腳本所在的目錄，這樣可以確保在運行腳本時能夠正確找到相關文件

#######################建立視窗########################
window = Tk()  # 建立一個新的視窗
window.title("photo")  # 設定視窗的標題（顯示在視窗上方）
#######################設定字型########################
font_size = 20  # 定義字型大小為20
window.option_add(
    "*font", ("Arial", font_size)
)  # 設定視窗中所有元件的字型為Arial，大小為font_size
#######################讀取圖片########################
# 使用PIL庫的Image.open()方法讀取圖片，並將其存儲在image變量中
image = Image.open("gay_weather_icon.png")  # 讀取名為gay_weather_icon.png的圖片
weather_photo = ImageTk.PhotoImage(
    image
)  # 將PIL圖像對象轉換為Tkinter可用的PhotoImage對象
#######################建立標籤########################
weather_label = Label(window, image=weather_photo)  # 建立一個標籤，顯示圖片
weather_label.pack(
    padx=10, pady=10
)  # 將標籤放置在視窗中，使用pack()方法進行佈局，並設置內邊距
weather_label.image = weather_photo  # 將weather_photo對象存儲在weather_label的image屬性中，這樣可以防止圖片被垃圾回收
#######################運行應用程式########################
window.mainloop()  # 啟動視窗的主事件循環，讓視窗
