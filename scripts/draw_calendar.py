import json
import sys
import calplot
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from leetcode_api import fetch_json

# 1. 設定你的帳號
USERNAME = "Matthiola"
API_URL = f"https://alfa-leetcode-api.onrender.com/{USERNAME}/calendar"

# 2. 呼叫 alfa-leetcode-api 取得資料（重試把睡著的 Render 實例叫醒）
print(f"Fetching data from {API_URL}...")
try:
    data = fetch_json(API_URL)
    # alfa-leetcode-api 的回傳格式通常是 { "submissionCalendar": "{\"1700000000\": 1, ...}" }
    # 注意：裡面的 submissionCalendar 是一個 JSON string，需要再 parse 一次
    calendar_data = json.loads(data['submissionCalendar'])
except Exception as e:
    # 第三方 API 暫時掛掉不該擋 CI：保留上一次的圖，正常結束。
    print(f"Skipping update (API unavailable): {e}")
    sys.exit(0)

# 3. 轉換資料格式 (Timestamp -> DateTime)
events = pd.Series(calendar_data)
events.index = pd.to_datetime(events.index.astype(int), unit='s')

# 4. 使用 calplot 畫出熱力圖
print("Generating heatmap...")
# cmap='YlGn' 是 Yellow-Green (類似 GitHub 風格)
fig, ax = calplot.calplot(events, cmap='YlGn', colorbar=False, yearlabels=True)

# 5. 存檔
plt.savefig("assets/leetcode-heatmap.png", bbox_inches='tight')
print("Saved to leetcode-heatmap.png")
