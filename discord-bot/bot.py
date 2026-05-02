import discord
import csv
import io
import os
import random
import urllib.request
from discord.ext import tasks

# --- 設定 ---
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = 123456789012345678  # 投稿したいチャンネルIDに変更
CSV_URL = "ここに先ほどコピーしたURLを貼る"

# --- CSVを取得して未紹介のものを返す ---
def get_pending():
    with urllib.request.urlopen(CSV_URL) as res:
        content = res.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)
    return [r for r in rows if r.get("紹介済み", "").upper() != "TRUE"]

# --- Bot設定 ---
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(hours=168)
async def weekly_post():
    channel = client.get_channel(CHANNEL_ID)
    pending = get_pending()

    if not pending:
        await channel.send("✅ 全ての番組を紹介し終わりました！")
        return

    pick = random.choice(pending)

    await channel.send(
        f"📺 **今週のおすすめ番組！**\n\n"
        f"🎬 **{pick['タイトル']}**\n"
        f"🔗 {pick['URL']}"
    )

@client.event
async def on_ready():
    print(f"Bot起動: {client.user}")
    if not weekly_post.is_running():
        weekly_post.start()

client.run(DISCORD_TOKEN)