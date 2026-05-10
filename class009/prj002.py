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
asyncio.set.set_event_loop(asyncio.new_event_loop())

#######################事件#######################

#######################指令#######################

#######################啟動#######################
