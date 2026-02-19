import requests
import os

API_KEY = os.getenv("API_KEY")
WEBHOOK = os.getenv("WEBHOOK")

# 🔴 改成你的 Channel ID（UC開頭）
CHANNEL_ID = "UCJitgRp8m5f07mngmtSQf-w"

# 🔴 要標記的人（填 Discord ID）
USERS = [
    "651387834585972736",
    "543491519387009024",
    "1419999773364064307",
    "1447916951405072435",
    "195521855631785985"
]

STORAGE_FILE = "sent_videos.txt"

# ===== 抓最新影片 =====
video_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"
videos = requests.get(video_url).json()

if "items" not in videos or len(videos["items"]) == 0:
    exit()

video = videos["items"][0]

if video["id"]["kind"] != "youtube#video":
    exit()

video_id = video["id"]["videoId"]
title = video["snippet"]["title"]
url = f"https://www.youtube.com/watch?v={video_id}"
thumbnail = video["snippet"]["thumbnails"]["high"]["url"]

# ===== 讀取已發送紀錄 =====
try:
    with open(STORAGE_FILE, "r") as f:
        sent = f.read().splitlines()
except:
    sent = []

if video_id in sent:
    exit()

# ===== 組標記文字 =====
mention_text = " ".join([f"<@{uid}>" for uid in USERS])

# ===== 發送 Discord =====
data = {
    "content": f"{mention_text}\n🔥 New Shorts Alert!",
    "embeds": [{
        "title": title,
        "url": url,
        "image": {"url": thumbnail},
        "color": 16711680
    }],
    "allowed_mentions": {
        "users": USERS
    }
}

requests.post(WEBHOOK, json=data)

# ===== 記錄已發送 =====
with open(STORAGE_FILE, "a") as f:
    f.write(video_id + "\n")
