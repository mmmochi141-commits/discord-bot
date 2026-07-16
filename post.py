import csv
import io
import os
import random
import urllib.request
import json

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3eRvVcQUfCRU42X_jiZa2-l84LvrA2zLn_dblRsgQ5w-9OLxw2PQ_kOSWAsMmi1fJ9-RIS84W5t_T/pub?gid=0&single=true&output=csv"
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

# --- デバッグ: トークンが有効か確認 ---
test_req = urllib.request.Request(
    "https://discord.com/api/v10/users/@me",
    headers={"Authorization": f"Bot {DISCORD_TOKEN}"}
)
try:
    with urllib.request.urlopen(test_req) as res:
        print("トークンは有効:", res.read().decode())
except urllib.error.HTTPError as e:
    print("トークンエラー:", e.code, e.read().decode())

# --- デバッグ: チャンネル情報を取得できるか確認 ---
channel_req = urllib.request.Request(
    f"https://discord.com/api/v10/channels/{CHANNEL_ID}",
    headers={"Authorization": f"Bot {DISCORD_TOKEN}"}
)
try:
    with urllib.request.urlopen(channel_req) as res:
        print("チャンネル情報取得成功:", res.read().decode())
except urllib.error.HTTPError as e:
    print("チャンネルエラー:", e.code, e.read().decode())

# --- 本来の投稿処理 ---
def get_programs():
    with urllib.request.urlopen(CSV_URL) as res:
        content = res.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    return list(reader)

programs = get_programs()
pick = random.choice(programs)

data = {
    "content": f"📺 **今週のおすすめ番組！**\n\n🎬 **{pick['タイトル']}**\n🔗 {pick['URL']}"
}

url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
req = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json",
    },
    method="POST",
)
urllib.request.urlopen(req)
