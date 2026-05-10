# 認識裝飾詞 (Decorator)的用法
# 重要觀念:函數可以項變數一樣被傳遞

# 第一階段


# 定義一個函數，名稱為hello，功能是印出Hello
def hello():
    print("Hello")


# 定義一個函數，可以接收函數作為參數，名稱為call_func，功能是呼叫傳入的函數
def call_func(func):
    print("呼叫傳入的函數")
    func()  # 呼叫傳入的函數
    print("呼叫結束")


print("直接呼叫hello函數")
hello()
# 呼叫call_func函數，傳入hello函數作為參數
print()
print("呼叫call_func函數，傳入hello函數作為參數")
call_func(hello)
# 注意這裡傳入的是函數名稱，不帶括號，因為我們是傳遞函數本身，而不是呼叫它的結果

# 第二階段


# 核心概念:裝飾詞是一種特殊的函數，可以用來修改其他函數的行為，而不需要改變被裝飾的函數的程式碼
# (把函數用一個函數包裝起來)
def gift_wrapper(func):
    def wrapper():
        print("這是裝飾詞的前置動作")
        func()  # 呼叫被裝飾的函數
        print("這是裝飾詞的後置動作")

    return wrapper  # 回傳包裝後的函數


def hello():
    print("Hi")


hello = gift_wrapper(hello)  # 使用裝飾詞包裝hello函數進去
hello()  # 印出包裝後的函數

# 第三階段


# Python提供了一個語法，可以讓我們更簡潔地使用裝飾詞，那就是使用@符號
# 在函數定義的上方使用@符號，後面接上裝飾詞的名稱，就可以直接將該函數包裝起來
@gift_wrapper  # 等於say_hi = gift_wrapper(say_hi)，如果沒有第32行到38行的函數定義，這裡會報錯，因為裝飾詞需要一個函數作為參數
def hello():
    print("Hi")


hello()  # 印出包裝後的函數

# 第四階段


# 外層:接收裝飾詞的參數(在這裡:name、description)
# 中層:接收被裝飾的函數(在這裡:func)
# 內層:執行被裝飾的函數，並在前後加上裝飾詞的功能(在這裡:wrapper)
def gift_wrapper(name, description):  # 外層函數，接收裝飾詞的參數
    print(f"[登記]這是{name}的前置動作，功能是{description}")

    def decorator(func):  # 中層函數，接收被裝飾的函數
        def wrapper():  # 內層函數，執行被裝飾的函數，並在前後加上裝飾詞的功能
            print(f"[執行]這是執行{name}的動作，功能是{description}")
            func()  # 呼叫被裝飾的函數

        return wrapper  # 回傳包裝後的函數(內層)

    return decorator  # 回傳裝飾詞(中層)


# @gift_wrapper(name = "hello", description = "打招呼")  # 使用裝飾詞，傳入參數
# 等於
#   step1: hello = gift_wrapper(name = "hello", description = "打招呼")  # 呼叫外層函數，傳入參數，回傳中層函數(裝飾詞)(會被打包，所以會印出登記的訊息)
#   step2: hello = hello(hello_command)  # 呼叫中層函數(裝飾詞)，傳入被裝飾的函數，回傳內層函數(包裝後的函數)
@gift_wrapper(name="hello", description="打招呼")  # 使用裝飾詞，傳入參數
def hello_command():
    print("Hi(這是指令的內容)")


hello_command()  # 印出包裝後的函數
