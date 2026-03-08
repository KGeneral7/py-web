#######################匯入模組#######################
#匯入tkinter模組
#*表示匯入模組中的所有函數(變數)和類別(物件)(*是萬用字元，表示所有)
from tkinter import *
#######################定義函數########################
def hi():
    print("Hello, world!")
def show():
    display.config(text="Hello, world!", fg="blue", bg="red")#設定標籤的文字為"Hello, world!"
def clear():
    display.config(text="")#設定標籤的文字為空字串，清除標籤的內容
#######################建立視窗########################
window = Tk() #建立視窗物件
window.title("My first GUI") #設定視窗標題
window.geometry("400x300") #設定視窗大小，格式為"寬x高"
#######################建立按鈕########################
button1 = Button(window, text="show", command=show) #建立按鈕物件，並設定按鈕文字
#指令(def)在這裡裡面不能加()因為我們只是要傳遞函數的參考，而不是呼叫函數
button2 = Button(window, text="clear", command=clear)
#######################建立標籤########################
display = Label(window, text="") #建立標籤物件，並設定標籤文字
#######################運行應用程式########################
button1.pack() #將按鈕放入視窗中，並自動調整位置和大小
button2.pack() #將按鈕放入視窗中，並自動調整位置和大小
display.pack() #將標籤放入視窗中，並自動調整位置和大小
window.mainloop() 
'''
運行應用程式，進入事件循環，有了這行程式碼，視窗才會顯示出來，並且保持運行狀態，
直到使用者關閉視窗為止
'''
