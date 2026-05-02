import discord
import csv
import io
import os
import random
import urllib.request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# --- 設定 ---
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3eRvVcQUfCRU42X_jiZa2-l84LvrA2zLn_dblRsgQ5w-9OLxw2PQ_kOSWAsMmi1fJ9-RIS84W5t_T/pub?gid=0&single=true&output=csv"

# --- CSVを取得する ---
def get_programs():
    with urllib.request.urlopen(CSV_URL) as res:
        content = res.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    return list(reader)

# --- Bot設定 ---
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# --- 投稿処理 ---
async def weekly_post():
    channel = client.get_channel(CHANNEL_ID)
    programs = get_programs()
    if not programs:
        await channel.send("番組リストが空です！")
        return
    pick = random.choice(programs)
    await channel.send(
        f"📺 **今週のおすすめ番組！**\n\n"
        f"🎬 **{pick['タイトル']}**\n"
        f"🔗 {pick['URL']}"
    )

@client.event
async def on_ready():
    print(f"Bot起動: {client.user}")
    scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(
        weekly_post,
        CronTrigger(day_of_week="mon", hour=9, minute=0)  # 毎週月曜9時
    )
    scheduler.start()

client.run(DISCORD_TOKEN)
