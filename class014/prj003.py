#######################模組#######################
# asyncio 是 python 內建的非同步工具(不是多執行緒)
# 可以把 asyncio 想成[任務小管家]:如果某事件需要等待網路回應，或是需要等待使用者輸入，
# asyncio 就會幫我們把這個事件暫停，等到事件完成後再繼續執行後續的程式碼
import asyncio
import discord  # pip install -U discord.py (在終端機);此模組是用來與 Discord 進行互動的主要工具
import os  # 讀取環境變數的模組
from dotenv import load_dotenv
import requests
from function.function import WearherAPI, AIAssistant

# function.function(第一個是資料夾，第二個是檔案)，import WearherAPI是選擇要使用的模組
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
bot = discord.Client(intents=intents)
# 建立一個 Discord bot 物件，這個物件是我們與 Discord 進行互動的主要工具
tree = discord.app_commands.CommandTree(bot)
# 建立一個 CommandTree 物件，這個物件是用來管理我們的指令的工具

weather_api = WearherAPI(os.getenv("WEATHER_API_KEY"))
# 建立一個 WearherAPI 的實例，這個實例是我們用來查詢天氣資訊的工具，當我們建立這個實例時，我們需要傳入一個 api_key，這個 api_key 是用來驗證我們的

ai_assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))
# 從環境變數中讀取 OPENAI_API_KEY，這個 api_key 是用來驗證我們的身份的，當我們呼叫 OpenAI 的 API 時，會使用這個 api_key 來驗證我們的身份，確保我們有權限使用這些 API


def build_weather_embed(weather_summary):
    """把整理好的天氣資訊摘要，排成Discord embed的格式，這樣就可以在 Discord 上美觀地顯示天氣資訊了"""
    # embed 是 Discord 上用來顯示豐富內容的工具(卡片)，當我們建立一個 embed 物件時，可以指定它的標題、描述、顏色等等，這裡我們指定了標題為城市名稱加上 "的天氣"，描述為天氣的描述，顏色為藍色，這樣就建立了一個基本的 embed 物件了
    embed = discord.Embed(
        title=f"{weather_summary['city_name']}的天氣",
        description=f"描述:{weather_summary['description']}",
        color=discord.Colour.from_str("#201ad3"),
    )

    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])

    embed.set_thumbnail(url=icon_url)

    embed.add_field(
        name="溫度",
        value=f"{weather_summary['temperature_celsius']} °C",
        inline=False,
    )  # embed.add_field方法是用來在 embed 裡添加欄位的工具，當我們呼叫它時，可以指定欄位的名稱、值，以及是否要把這個欄位顯示在同一行，這裡我們指定了 "溫度" 作為欄位的名稱，然後指定了天氣摘要裡的溫度作為欄位的值，最後指定了 inline=False，這樣這個欄位就會顯示在獨立的一行，而不是和其他欄位顯示在同一行
    return embed


def build_forecast_embeds(forecast_summary):
    """把未來多筆天氣預報資訊摘要，排成多個 Discord embed 的格式，這樣就可以在 Discord 上美觀地顯示未來的天氣預報資訊了"""
    # forecast_summary 是一個包含多筆天氣預報資訊的列表，每筆天氣預報資訊都是一個字典，裡面包含了日期、溫度、天氣描述等等資訊，這裡我們把這些資訊整理成多個 Discord embed 的格式，這樣就可以在 Discord 上美觀地顯示未來的天氣預報資訊了
    # 這個函式的邏輯和 build_weather_embed 類似，只是這裡我們處理的是多筆天氣預報資訊，所以我們需要使用一個迴圈來遍歷這些資訊，然後把每筆資訊整理成一個 embed，最後把這些 embed 組合成一個列表返回了
    embeds = []

    for forecast in forecast_summary:
        # 這個函式每跑一次就會建立一個新的 embed，這樣就可以把每筆天氣預報資訊都整理成一個獨立的 embed 了
        embed = discord.Embed(
            title=f"{forecast['city_name']}的天氣預報 - {forecast['datetime']}",
            description=f"描述:{forecast['description']}",
            color=discord.Colour.from_str("#201ad3"),
        )
        # forecast的icon_code也是WeatherAPI整理好的資料，可以直接拿來組圖示網址
        icon_url = weather_api.get_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']} °C",
            inline=False,
        )
        embeds.append(embed)

    return embeds


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
    await interaction.response.send_message("Hey!")
    # 輸入/hello指令，回應hello
    # name和def要是一樣的，這裡我們定義了一個指令，當使用者在 Discord 上使用 /hello 指令時，這個指令處理器就會被呼叫，並且回應 "hello"
    # 當使用者在 Discord 上使用 /hello 指令時，這個指令處理器就會被呼叫，並且回應 "hello"，這裡使用了 await，因為 send_message 方法是一個非同步方法，當我們呼叫它時，會暫停這個函式的執行，讓其他任務有機會執行，直到 send_message 方法完成後，這個函式才會繼續執行
    # interaction:當使用者在 Discord 上使用 /hello 指令時，Discord 會把這個事件封裝成一個 Interaction 物件，然後傳遞給這個指令處理器，讓我們可以從這個物件中獲取有關這次指令的資訊，例如使用者的 ID、指令的參數等等，這裡我們把這個物件命名為 interaction，然後在函式裡使用它來回應指令
    # interaction.response.send_message 方法是用來回應指令的工具，當我們呼叫它時，可以指定要回應的內容，這裡我們指定了 "hello" 作為要回應的內容(要經過網路傳輸，所以需要等待)，當 send_message 方法完成後，這個函式才會繼續執行
    # send_message:傳私訊給使用者


@tree.command(name="weather", description="查詢天氣")
async def weather(
    interaction: discord.Interaction,
    city_name: str,
    forecast: bool = False,
    ai: bool = False,
):
    """輸入/weather [城市名稱]指令，回應該城市的天氣"""
    await interaction.response.defer()  # 告訴 Discord 我們已經收到指令了，正在處理中，這樣 Discord 就不會因為我們處理指令需要一點時間而認為我們沒有回應了，然後就顯示 "This interaction failed" 的訊息了
    city = (
        city_name.strip()
    )  # 去除城市名稱前後的空白，這樣就可以避免使用者輸入 " Taipei " 這種帶有空白的城市名稱了，這裡我們使用了 strip() 方法，這個方法會返回一個新的字串，這個字串是原來的字串去除了前後空白後的結果

    if not weather_api.api_key:
        await interaction.followup.send(
            "未設定WEATHER_API_KEY,請先設定在.env檔案中"
        )  # 如果我們在建立 WearherAPI 實例時沒有傳入 api_key，那麼這個實例的 api_key 屬性就會是 None，這裡我們檢查了這個屬性，如果它是 None，就回應一條訊息，告訴使用者天氣功能尚未設定好，請稍後再試，這樣就可以避免因為沒有 api_key 而導致的錯誤了
        return

    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(
                    f"找不到 {city} 的天氣資訊，請確認城市名稱是否正確"
                )  # 如果 get_weather_summary 方法返回了 None，這意味著我們沒有找到對應城市的天氣資訊，這裡我們回應一條訊息，告訴使用者找不到該城市的天氣資訊，請確認城市名稱是否正確，這樣就可以避免因為沒有找到天氣資訊而導致的錯誤了
                return

            embed = build_weather_embed(
                weather_summary
            )  # 把天氣摘要整理成 Discord embed 的格式，這樣就可以在 Discord 上美觀地顯示天氣資訊了
            await interaction.followup.send(
                embed=embed
            )  # 回應天氣資訊，這裡我們使用了 followup.send 方法來回應天氣資訊，這個方法是用來在 defer 之後回應指令的工具，當我們呼叫它時，可以指定要回應的內容，這裡我們指定了 embed=embed，這樣就會把我們整理好的天氣資訊以 embed 的形式回應給使用者了
            return
        if not ai:
            # ai=False的話就回傳天氣預報資訊，ai=True的話就回傳AI生成的天氣預報資訊分析
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                await interaction.followup.send(
                    f"找不到 {city} 的天氣資訊，請確認城市名稱是否正確"
                )
                # 如果 get_weather_summary 方法返回了 None，這意味著我們沒有找到對應城市的天氣資訊，這裡我們回應一條訊息，告訴使用者找不到該城市的天氣資訊，請確認城市名稱是否正確，這樣就可以避免因為沒有找到天氣資訊而導致的錯誤了
                return

            embeds = build_forecast_embeds(forecast_summary)
            # 把天氣摘要整理成 Discord embed 的格式，這樣就可以在 Discord 上美觀地顯示天氣資訊了
            await interaction.followup.send(embeds=embeds[:10])
            # 回應天氣資訊，這裡我們使用了 followup.send 方法來回應天氣資訊，這個方法是用來在 defer 之後回應指令的工具，當我們呼叫它時，可以指定要回應的內容，這裡我們指定了 embed=embed，這樣就會把我們整理好的天氣資訊以 embed 的形式回應給使用者了
            return
        # 取得預報原始資料流程請參考 class012/prj001.py裡的weather指令處理器裡的註解說明
        # 這裡改用 get_forecast_summary 方法來取得未來多筆天氣預報資訊的摘要，這個方法會返回一個包含多筆天氣預報資訊的列表，每筆天氣預報資訊都是一個字典，裡面包含了日期、溫度、天氣描述等等資訊，這樣我們就可以在後續的程式碼裡把這些資訊整理成多個 Discord embed 的格式，然後回應給使用者了
        raw_forecast = weather_api.get_forecast(city)
    except (requests.RequestException, ValueError):
        await interaction.followup.send(
            "查詢天氣資訊時發生錯誤，請稍後再試"
        )  # 如果在查詢天氣資訊的過程中發生了網路錯誤或者資料處理錯誤，我們就會捕捉到這些錯誤，然後回應一條訊息，告訴使用者查詢天氣資訊時發生錯誤，請稍後再試，這樣就可以避免因為這些錯誤而導致的程式崩潰了
        return

    # OpenAI 呼叫失敗的錯誤處理
    # 所以用獨立的try-except來處理OpenAI的呼叫，這樣就可以避免因為 OpenAI 呼叫失敗而導致整個指令處理器崩潰了
    analysis, error = ai_assistant.ask(
        system_prompt="你是一個專業的氣象分析師，請根據使用者提供的未來天氣預報資訊，分析未來幾天的天氣趨勢，並且給出一些建議，例如是否需要攜帶雨具、是否適合戶外活動等等，請用中文回答",
        user_message=f"以下是{city}未來幾天的天氣預報資訊，請根據這些數據提供詳細的天氣分析和建議: \n{raw_forecast}",
    )
    if error:
        # 如果 OpenAI 呼叫失敗了，我們就回應錯誤訊息，告訴使用者 AI 助手目前無法使用了，請稍後再試，這樣就可以避免因為 OpenAI 呼叫失敗而導致的程式崩潰了
        await interaction.followup.send(error)
        return
    else:
        await interaction.followup.send(f"{city}未來幾天的天氣分析和建議:\n{analysis}")
        # 如果 OpenAI 呼叫成功了，我們就回應 AI 助手提供的分析結果，這裡我們使用了 followup.send 方法來回應分析結果，這個方法是用來在 defer 之後回應指令的工具，當我們呼叫它時，可以指定要回應的內容，這裡我們指定了 analysis 作為要回應的內容(要經過網路傳輸，所以需要等待)，當 send_message 方法完成後，這個函式才會繼續執行


#######################啟動#######################
def main():
    bot.run(
        os.getenv("DC_BOT_TOKEN")
    )  # 啟動 bot，這裡我們從環境變數中讀取 DISCORD_TOKEN，這個 token 是用來驗證我們的 bot 的身份的，當我們呼叫 bot.run() 方法時，Discord bot 就會開始運行，並且連接到 Discord 上，等待事件的發生


if (
    __name__ == "__main__"
):  # __是python內建的特殊變數，當這個程式被直接執行時，__name__ 的值會是 "__main__"，而當這個程式被當作模組匯入到其他程式時，__name__ 的值會是模組的名稱，所以我們可以利用這個特性來控制程式的執行，當這個程式被直接執行時，就會呼叫 main 函式，啟動 bot，但被當模組時就不會啟動，這樣我們就可以在其他程式裡匯入這個模組，然後使用裡面的功能，而不會啟動 bot
    main()  # 當這個程式被直接執行時，就會呼叫 main 函式，啟動 bot，但被當模組時就不會啟動，這樣我們就可以在其他程式裡匯入這個模組，然後使用裡面的功能，而不會啟動 bot
