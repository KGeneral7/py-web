#######################匯入模組#######################
# 匯入tkinter模組
# *表示匯入模組中的所有函數(變數)和類別(物件)(*是萬用字元，表示所有)
from tkinter import *


#######################定義函數########################
def show():
    if display.cget("bg") == "red":
        display.config(
            text="Hello, world!", fg="red", bg="blue"
        )  # 偵測到背景是紅色，則切換為藍色背景和紅色文字
    elif display.cget("bg") == "blue":
        display.config(
            text="Hello, world!", fg="blue", bg="red"
        )  # 偵測到背景是藍色，則切換為紅色背景和藍色文字


#######################建立視窗########################
window = Tk()  # 建立視窗物件
window.title("My first GUI")  # 設定視窗標題
window.geometry("400x300")  # 設定視窗大小，格式為"寬x高"
#######################建立按鈕########################
button1 = Button(window, text="show", command=show)  # 建立按鈕物件，並設定按鈕文字
# 指令(def)在這裡裡面不能加()因為我們只是要傳遞函數的參考，而不是呼叫函數
#######################建立標籤########################
display = Label(
    window, text="Hello, world!", fg="blue", bg="red"
)  # 建立標籤物件，並設定標籤文字

#######################運行應用程式########################
button1.pack()  # 將按鈕放入視窗中，並自動調整位置和大小
display.pack()  # 將標籤放入視窗中，並自動調整位置和大小
window.mainloop()
"""
運行應用程式，進入事件循環，有了這行程式碼，視窗才會顯示出來，並且保持運行狀態，
直到使用者關閉視窗為止
"""
