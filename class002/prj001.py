#######################匯入模組#######################
# 從 tkinter 模組中匯入所有功能（*代表全部）
from tkinter import *


#######################定義按鈕點擊事件########################
def show():
    # 宣告 a 為全域變數，這樣在函數內才能修改它的值
    global a
    if a:
        # 第一次點擊：顯示藍字在紅背景
        display.config(text="Hello, world!", fg="blue", bg="red")
        a = not a  # 切換 a 的值（True變False）
    else:
        # 再次點擊：顯示紅字在藍背景
        display.config(text="Hello, world!", fg="red", bg="blue")
        a = not a  # 切換 a 的值（False變True）


# 全域變數：控制顏色狀態（True表示第一種配色，False表示第二種配色）
a = True

#######################建立視窗########################
# 建立一個新的視窗
window = Tk()
# 設定視窗的標題（顯示在視窗上方）
window.title("My first GUI")
# 設定視窗大小：寬 400 像素，高 300 像素
window.geometry("400x300")
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
