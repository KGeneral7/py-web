#######################匯入模組#######################
from ttkbootstrap import *  # pip install ttkbootstrap -U(在終端機
import sys
import os

#######################設定工作目錄########################
os.chdir(
    sys.path[0]
)  # 將當前工作目錄更改為腳本所在的目錄，這樣可以確保在運行腳本時能夠正確找到相關文件


#######################定義函數########################
def on_switch_change():
    # 當CheckButton的狀態改變時，將check_type的值轉換為字符串並顯示在Check_label標籤上
    Check_label.config(text=str(check_type.get()))  # 更新Check_label的文本為check


#######################建立視窗########################
window = Tk()  # 建立一個新的視窗
window.title("CheckButton")  # 設定視窗的標題（顯示在視窗上方）
#######################設定字型########################
font_size = 20  # 定義字型大小為20
window.option_add(
    "*font", ("Arial", font_size)
)  # 設定視窗中所有元件的字型為Arial，大小為font_size
#######################設定主題########################
style = Style("superhero")  # 設定視窗的主題為superhero
# 設定按鈕和checkbutton的樣式
style.configure(
    "TButton", font=("Arial", font_size)
)  # 設定TButton的字型為Arial，大小為20
style.configure(
    "TCheckbutton", font=("Arial", font_size)
)  # 設定TCheckbutton的字型為Arial，大小為20
#######################建立變數########################
check_type = (
    BooleanVar()
)  # 建立一個BooleanVar變數，用於存儲CheckButton的選擇狀態(ttk用來存儲CheckButton的狀態，BooleanVar用來存儲布林值)
check_type.set(
    True
)  # 設定check_type變數的初始值為True，表示CheckButton默認為未選中狀態
#######################建立標籤########################
# 建立一個標籤，顯示CheckButton的選擇狀態
Check_label = Label(window, text="True")  # 建立一個標籤，顯示CheckButton的選擇狀態
# 將標籤放置在視窗中，使用grid()方法進行佈局
Check_label.grid(
    row=1, column=2, padx=10, pady=10
)  # 將標籤放置在視窗的第一行第一列，並設置內邊距
#######################建立Checkbutton########################
# 建立一個CheckButton，會和check_type變數綁定，當CheckButton的狀態改變時，check_type的值也會改變
# 勾選CheckButton時，check_type的值為True；取消勾選時，check_type的值為False
check_button = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
)  # 建立一個CheckButton，綁定check_type變數，顯示文字"CheckButton"
# 將CheckButton放置在視窗中，使用grid()方法進行佈局
check_button.grid(
    row=1, column=1, padx=10, pady=10
)  # 將CheckButton放置在視窗的第一行第一列，並設置內邊距

#######################運行應用程式########################
window.mainloop()  # 啟動視窗的事件循環，使視窗保持開啟狀態，等待用戶操作
