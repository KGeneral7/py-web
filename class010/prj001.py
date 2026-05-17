#######################模組#######################
# asyncio 是 python 內建的非同步工具(不是多執行緒)
# 可以把 asyncio 想成[任務小管家]:如果某事件需要等待網路回應，或是需要等待使用者輸入，
# asyncio 就會幫我們把這個事件暫停，等到事件完成後再繼續執行後續的程式碼
import asyncio
import discord  # pip install -U discord.py (在終端機);此模組是用來與 Discord 進行互動的主要工具
import os  # 讀取環境變數的模組
from dotenv import load_dotenv

# pip install -U python-dotenv(在終端機);此模組是用來從 .env 文件中讀取環境變數的工具

#######################初始化#######################
load_dotenv()  # 從 .env 文件中讀取環境變數(在這裡是讀取 DISCORD_TOKEN等東西)

# event loop 可以想成是非同步任務的轉盤:
# 哪個任務需要等待，就把它放在轉盤上，等到它完成後再繼續執行後續的程式碼
# python 3.10+在主程式裡不一定會先準備好 event loop，所以我們需要自己準備一個
# 所以我們要先建立一個 event loop，然後在這個 loop 裡運行我們的 Discord bot
asyncio.set_event_loop(asyncio.new_event_loop())
intents = (
    discord.Intents.default()
)  # 建立一個 intents 物件，這個物件是用來告訴 Discord bot 我們想要接收哪些事件的工具
intents.message_content = (
    True  # 啟用 message_content intent，這樣我們的 bot 才能接收訊息內容相關的事件
)
bot = discord.Client(
    intents=intents
)  # 建立一個 Discord bot 物件，這個物件是我們與 Discord 進行互動的主要工具
tree = discord.app_commands.CommandTree(
    bot
)  # 建立一個 CommandTree 物件，這個物件是用來管理我們的指令的工具


#######################事件#######################
# @bot.event這個裝飾器是用來註冊事件的工具，當我們在函式上使用這個裝飾器時，就會把這個函式註冊為一個事件處理器，當對應的事件發生時，這個函式就會被呼叫
# def 是一般函式，通常會按照順序執行，當程式執行到這裡時，就會定義一個函式，但不會立即執行這個函式，只有當對應的事件發生時，這個函式才會被呼叫
# async def 是非同步函式，這種函式可以在執行過程中暫停，讓其他任務有機會執行，當程式執行到這裡時，就會定義一個非同步函式，但不會立即執行這個函式，只有當對應的事件發生時，這個函式才會被呼叫
# async要搭配await使用，當我們在非同步函式裡使用await時，就會暫停這個函式的執行，讓其他任務有機會執行，直到await後面的任務完成後，這個函式才會繼續執行(可以先暫停， 之後再繼續執行)
@bot.event
async def on_ready():
    print(
        f"{bot.user} 已經準備好了！"
    )  # 當 bot 成功連接到 Discord 並且準備好接收事件時，這個事件處理器就會被呼叫，並且在終端機輸出一條訊息，告訴我們 bot 已經準備好了
    await tree.sync()  # 同步指令，這樣我們的指令才會生效，這個方法會把我們在 CommandTree 裡定義的指令同步到 Discord 上，讓它們可以被使用
    # await:等待事件完成，再繼續執行後續的程式碼，這裡我們等待 tree.sync() 方法完成，這樣我們就確保指令已經同步到 Discord 上了，才會繼續執行後續的程式碼
    # return:結束函式的執行，這裡我們沒有使用 return，因為我們希望在 on_ready 事件處理器裡繼續執行後續的程式碼，直到整個函式執行完成後才結束


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # 如果訊息的作者是 bot 自己，就不處理這個訊息，這樣可以避免 bot 回應自己的訊息，造成無限迴圈
    if message.content == "hello":
        await message.channel.send(
            "hello"
        )  # 如果訊息的內容是 "hello"，就回應 "hello"，這裡使用了 await，因為 send 方法是一個非同步方法，當我們呼叫它時，會暫停這個函式的執行，讓其他任務有機會執行，直到 send 方法完成後，這個函式才會繼續執行
        # send 方法是用來發送訊息的工具，當我們呼叫它時，可以指定要發送到哪個頻道，以及要發送的內容，這裡我們指定了 message.channel，這樣就會把訊息發送到與原始訊息相同的頻道，然後指定了 "hello" 作為要發送的內容(要經過網路傳輸，所以需要等待)，當 send 方法完成後，這個函式才會繼續執行
        # channel.send:傳進去channel


#######################指令#######################
@tree.command(name="hello", description="回應 hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("hello")
    # 輸入/hello指令，回應hello
    # name和def要是一樣的，這裡我們定義了一個指令，當使用者在 Discord 上使用 /hello 指令時，這個指令處理器就會被呼叫，並且回應 "hello"
    # 當使用者在 Discord 上使用 /hello 指令時，這個指令處理器就會被呼叫，並且回應 "hello"，這裡使用了 await，因為 send_message 方法是一個非同步方法，當我們呼叫它時，會暫停這個函式的執行，讓其他任務有機會執行，直到 send_message 方法完成後，這個函式才會繼續執行
    # interaction:當使用者在 Discord 上使用 /hello 指令時，Discord 會把這個事件封裝成一個 Interaction 物件，然後傳遞給這個指令處理器，讓我們可以從這個物件中獲取有關這次指令的資訊，例如使用者的 ID、指令的參數等等，這裡我們把這個物件命名為 interaction，然後在函式裡使用它來回應指令
    # interaction.response.send_message 方法是用來回應指令的工具，當我們呼叫它時，可以指定要回應的內容，這裡我們指定了 "hello" 作為要回應的內容(要經過網路傳輸，所以需要等待)，當 send_message 方法完成後，這個函式才會繼續執行
    # send_message:傳私訊給使用者


#######################啟動#######################
def main():
    bot.run(
        os.getenv("DC_BOT_TOKEN")
    )  # 啟動 bot，這裡我們從環境變數中讀取 DISCORD_TOKEN，這個 token 是用來驗證我們的 bot 的身份的，當我們呼叫 bot.run() 方法時，Discord bot 就會開始運行，並且連接到 Discord 上，等待事件的發生


if (
    __name__ == "__main__"
):  # __是python內建的特殊變數，當這個程式被直接執行時，__name__ 的值會是 "__main__"，而當這個程式被當作模組匯入到其他程式時，__name__ 的值會是模組的名稱，所以我們可以利用這個特性來控制程式的執行，當這個程式被直接執行時，就會呼叫 main 函式，啟動 bot，但被當模組時就不會啟動，這樣我們就可以在其他程式裡匯入這個模組，然後使用裡面的功能，而不會啟動 bot
    main()  # 當這個程式被直接執行時，就會呼叫 main 函式，啟動 bot，但被當模組時就不會啟動，這樣我們就可以在其他程式裡匯入這個模組，然後使用裡面的功能，而不會啟動 bot
