import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import sys
import os

# --- 設定區 ---
USERNAME = "Matthiola"
API_URL = f"https://alfa-leetcode-api.onrender.com/{USERNAME}/contest/history"
START_FILTER_DATE = datetime(2025, 9, 1) # 依照你上次的要求

print(f"Fetching data from {API_URL}...")

try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(API_URL, headers=headers, timeout=30)
    
    if response.status_code != 200:
        print(f"Error: API status {response.status_code}")
        sys.exit(1)

    data = response.json()
    if 'contestHistory' not in data:
        print("Error: 'contestHistory' not found.")
        sys.exit(1)
        
    history = data['contestHistory']

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# --- 資料處理與過濾 ---
print("Filtering data...")
dates = []
ratings = []

for contest in history:
    if contest['rating'] is not None:
        ts = int(contest['contest']['startTime'])
        dt = datetime.fromtimestamp(ts)
        
        if dt >= START_FILTER_DATE:
            dates.append(dt)
            ratings.append(contest['rating'])

if not dates:
    print("No contest data found in the specified range.")
    # 畫空圖
    plt.figure()
    plt.text(0.5, 0.5, 'No Data', ha='center')
    os.makedirs("assets", exist_ok=True)
    plt.savefig("assets/leetcode-rating.png")
    sys.exit(0)

# --- 畫圖 ---
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(10, 5))

# 1. 計算 Y 軸的上下限 (動態調整)
min_rating = min(ratings)
max_rating = max(ratings)
buffer = 40  # 上下預留 40 分的空間，讓曲線不要頂天立地
bottom_limit = min_rating - buffer
top_limit = max_rating + buffer

# 設定 Y 軸範圍
ax.set_ylim(bottom_limit, top_limit)

# 2. 繪製曲線
ax.plot(dates, ratings, color='#ffa116', linewidth=2, marker='o', markersize=4, label='Rating')

# 3. 填色修正：現在要填滿到 bottom_limit，而不是預設的 0
ax.fill_between(dates, ratings, bottom_limit, color='#ffa116', alpha=0.15)

# 標題與網格
ax.set_title(f"{USERNAME}'s Rating (Since Sep 2025)", fontsize=14, color='white', pad=20)
ax.grid(True, linestyle='--', alpha=0.3)

# X 軸格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=0)

# 存檔
os.makedirs("assets", exist_ok=True)
plt.savefig("assets/leetcode-rating.png", bbox_inches='tight', dpi=150)
print(f"Saved to assets/leetcode-rating.png (Y-axis: {bottom_limit} ~ {top_limit})")
