#######################匯入模組#######################
# 從 tkinter 模組中匯入所有功能（*代表全部）
from tkinter import *
import random


#######################定義按鈕點擊事件########################
def show():
    fg_colors = "#" + "".join(
        [random.choice("0123456789ABCDEF") for i in range(6)]
    )  # 隨機生成一個顏色代碼
    # random.choice("0123456789ABCDEF")會從字符串"0123456789ABCDEF"中隨機選擇一個字符，這些字符代表了十六進制顏色代碼中的數字和字母
    # .join()方法將列表中的元素連接成一個字符串，並且在元素之間插入指定的分隔符（這裡是空字符串""）
    # .join用法示例：
    # numbers = ['1', '2', '3']
    # result = "".join(numbers)  # result的值將是"1,2,3"
    """
    比對展開寫法
    fg_colors = "#"
    for i in range(6):
        fg_colors += random.choice("0123456789ABCDEF")
    
    
    """
    bg_colors = "#" + "".join(
        [random.choice("0123456789ABCDEF") for i in range(6)]
    )  # 隨機生成一個顏色代碼
    display.config(
        text="Hello, world!", fg=fg_colors, bg=bg_colors
    )  # 設定標籤的文字為"Hello, world!"，並且使用隨機生成的顏色作為前景色和背景色


#######################建立視窗########################
# 建立一個新的視窗
window = Tk()
# 設定視窗的標題（顯示在視窗上方）
window.title("My first GUI")
# 設定視窗大小：寬 400 像素，高 300 像素
window.geometry("400x300")
window.option_add("*Font", "Arial 20")
# 設定視窗中所有元件的預設字體為Arial，大小為20
# option_add方法用於設定視窗中所有元件的預設屬性，這裡我們設定了字體（Font）屬性，使得所有元件(*)的字體都會使用Arial，大小為20
#######################建立按鈕########################
# 建立按鈕：文字為 "show"，點擊時執行 show 函數
# 注意：command=show 不加括號，因為我們要傳遞函數本身，而不是呼叫它
button1 = Button(window, text="show", command=show)
#######################建立標籤########################
# 建立標籤：初始為空白，點擊按鈕後會顯示文字和顏色
display = Label(window, text="")

#######################將元件加入視窗並運行########################
# 把按鈕放入視窗（pack 會自動調整位置和大小）
button1.pack()
# 把標籤放入視窗
display.pack()
# 進入事件循環：保持視窗顯示，並等待使用者的操作
# 直到使用者關閉視窗，程式才會結束
window.mainloop()
