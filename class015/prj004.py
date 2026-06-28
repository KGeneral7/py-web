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

# 限制可讀取歷史紀錄上數量為20筆，這樣就不會因為歷史紀錄太多而導致效能問題了
CHANNEL_HISTORY_LIMIT = 20

# 更換模型，其他維持原本的狀況
OPEN_MODEL = "gpt-5.5"
OPEN_TEMPERATURE = 1  # gpt-5.5 目前使用預設的 temperature，不調成0.2或0.5
# 因為gpt-5.5的temperature是不能自己設的所以要改為預設的1
# system_prompt是給AI的指令，告訴AI我們希望它怎麼回答，這個訊息會影響AI的回答風格和內容，所以我們要把它放在第一個位置，讓AI先知道我們的要求。 # system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個在 Discord 群組頻道中協助大家的 AI 助手。
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，語氣自然、簡短、適合國小學生閱讀。
每次回覆需控制在500個中文字以內，避免 Discord 訊息過長。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，不要寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""

# 允許AI回覆中提到"使用者"或"其他bot"，但不允許AI回覆中提到"everyone"、"here"或角色標記，這樣就可以避免AI回覆中出現不適當的提及了
# bot 在 Discord 裡也屬於 user ，所以 user=True就可以提到其他bot
AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    users=True,
    roles=False,
    everyone=False,
    replied_user=True,
)


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


async def get_channel_history(channel, bot_user, limit=15, before=None):
    """取得頻道歷史訊息，這樣就可以讓 AI 助手參考這些歷史訊息來回答問題了(整理成messgaes)"""
    old_messages = []
    history_messages = []
    # Discord API 讀取頻道訊息時，預先拿較新的訊息
    # 這裡先明確抓"最近幾則"的訊息，把"抓資料"和"排成對話順序"分成兩步
    # oldest_first=False代表先拿取最接近before參數的訊息，也就是較新的訊息，這樣就可以確保我們拿到的訊息是最近的了
    # 下面再反轉成"舊到新"交給AI，這樣就可以確保AI參考的歷史訊息是按照時間順序排列的了
    async for old_message in channel.history(
        limit=limit,
        before=before,
        oldest_first=False,
    ):
        old_messages.append(old_message)

    # Discord 抓回來看的是"新到舊"，所以要反轉成"舊到新"的順序，這樣才是對話的正確順序
    for old_message in reversed(
        old_messages
    ):  # reversed是python內建的函式，可以把一個可迭代的物件反轉，這裡我們把抓回來的訊息列表反轉成從舊到新的順序，這樣就可以確保我們參考的歷史訊息是按照時間順序排列的了
        # 這裡使用message.content，而不是message.clean_content，是因為clean_content會把訊息裡的mention轉換成純文字，這樣AI就無法知道訊息裡提到了誰了，所以我們需要使用原始的content，這樣AI才能正確地參考歷史訊息來回答問題了
        # message.content 會保留<@使用者ID>這種真正的mention格式，這樣AI就可以知道訊息裡提到了誰了，這樣AI在回答問題的時候就可以參考這些歷史訊息來回答問題了
        content = (
            old_message.content.strip()
        )  # 去除訊息內容前後的空白，這樣就可以避免因為訊息內容有多餘的空白而導致 AI 參考歷史訊息時出現問題了，這裡我們使用了 strip() 方法，這個方法會返回一個新的字串，這個字串是原來的字串去除了前後空白後的結果
        if (
            not content
        ):  # 如果訊息內容是空的，就跳過這個訊息，這樣就可以避免因為訊息內容是空的而導致 AI 參考歷史訊息時出現問題了
            continue

        if old_message.author.id == bot_user.id:
            # 機器人自己以前說過的話，用 assistant 的角色來標記，這樣AI就可以知道這是機器人自己以前說過的話了，這樣AI在回答問題的時候就可以參考這些歷史訊息來回答問題了
            history_messages.append({"role": "assistant", "content": content})
        else:
            # 其他同學和其他bot都標籤上名字，AI才知道是誰說的。
            speaker_type = "機器人" if old_message.author.bot else "同學"
            speaker_mention = (
                old_message.author.mention
            )  # 這裡我們使用了 message.author.mention，這個屬性會返回一個字符串，這個字符串是用來提及這個使用者的格式，例如 <@使用者ID>，這樣AI就可以知道訊息裡提到了誰了，這樣AI在回答問題的時候就可以參考這些歷史訊息來回答問題了
            user_content = (
                f"{old_message.author.display_name}"
                f"({speaker_type} ，mention:{speaker_mention})說: {content}"
            )
            history_messages.append({"role": "user", "content": user_content})

    return history_messages


async def ask_with_discord_history(message):
    """當機器人被提到時，整理 Discord 歷史，再交給 AI 助手回答。"""
    history_messages = await get_channel_history(
        channel=message.channel,
        bot_user=bot.user,
        limit=CHANNEL_HISTORY_LIMIT,
        before=message,
    )

    # Discord 提到機器人時，訊息會出現<@機器人ID>。
    # 這個標記是給 Discord 辨識用的，交給 AI 前先拿掉，問題會比較乾淨。
    # replace("這裡是原本的內容","這裡是替換完的內容")
    user_question = message.content.replace(f"<@{bot.user.id}>", "").strip()
    if not user_question:
        user_question = "清根據目前頻道對話，接著回應大家。"

    # 把提問使用者名字也放進內容中， AI 回覆聊天多人聊天時比較清楚。
    user_message = (
        f"{message.author.display_name} "
        f"(mention:{message.author.mention})提到你: {user_question}"
    )

    # 上一堂課的 ask() 多了 history_messages 參數;
    # 沒有歷史時可以不傳，有歷史時就把整理好的舊對話一起交給 AI。
    return ai_assistant.ask(
        system_prompt=CHAT_SYSTEM_PROMPT,
        user_message=user_message,
        history_message=history_messages,
        temperature=OPEN_TEMPERATURE,
        model=OPEN_MODEL,
    )


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
    elif bot.user in message.mentions:
        # 只有在群組頻道中被 @ 時，才讀取前面的頻道訊息當作上下文。
        async with message.channel.typing():  # typing是加入讓 AI 輸入時加上 ....再輸入中的提示
            answer, error = await ask_with_discord_history(message)

        if error:
            await message.channel.send(error)
        else:
            # 用 reply 可以清楚接在發問者的訊息下面;
            # allowed_mentions 則控制 AI 回覆裡那些 mention 真的會生效。
            await message.reply(
                answer,
                mention_author=True,
                allowed_mentions=AI_REPLY_ALLOWED_MENTIONS,
            )


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
        system_prompt="你是一個專業的氣象分析師，請根據使用者提供的未來天氣預報資訊，分析未來幾天的天氣趨勢，並且給出一些建議，例如是否需要攜帶雨具、是否適合戶外活動等等，請用中文回答(控制在500字以內)",
        user_message=f"以下是{city}未來幾天的天氣預報資訊，請根據這些數據提供詳細的天氣分析和建議: \n{raw_forecast}",
        temperature=OPEN_TEMPERATURE,
        model=OPEN_MODEL,
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
