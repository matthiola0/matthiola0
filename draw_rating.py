import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 1. 設定你的帳號
USERNAME = "Matthiola"
API_URL = f"https://alfa-leetcode-api.onrender.com/{USERNAME}/contest/history"

# 2. 呼叫 API 取得資料
print(f"Fetching data from {API_URL}...")
try:
    response = requests.get(API_URL)
    data = response.json()
    
    # alfa-leetcode-api 的回傳格式通常會有 'contestHistory' 陣列
    if 'contestHistory' not in data or not data['contestHistory']:
        print("No contest history found or API error.")
        # 如果沒資料，畫一張空圖避免報錯
        plt.figure()
        plt.text(0.5, 0.5, 'No Contest Data', ha='center')
        plt.savefig("leetcode-rating.png")
        exit(0)
        
    history = data['contestHistory']
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

# 3. 整理數據 (時間 與 積分)
dates = []
ratings = []

for contest in history:
    # 確保這場比賽有計算積分 (有些是 null)
    if contest['rating'] is not None:
        # Timestamp 轉 Date
        ts = int(contest['contest']['startTime'])
        dates.append(datetime.fromtimestamp(ts))
        ratings.append(contest['rating'])

# 4. 開始畫圖 (模仿 LeetCode 風格)
plt.style.use('dark_background') # 使用深色背景
fig, ax = plt.subplots(figsize=(10, 5))

# 繪製曲線
ax.plot(dates, ratings, color='#ffa116', linewidth=2, marker='o', markersize=3, label='Rating')

# 填充曲線下方的顏色 (漸層感)
ax.fill_between(dates, ratings, color='#ffa116', alpha=0.1)

# 設定標題與標籤
ax.set_title(f"{USERNAME}'s LeetCode Rating", fontsize=14, color='white', pad=20)
ax.grid(True, linestyle='--', alpha=0.3)

# 格式化日期軸
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# 5. 存檔
plt.savefig("assets/leetcode-rating.png", bbox_inches='tight', dpi=150)
print("Saved to leetcode-rating.png")
