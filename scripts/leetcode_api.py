"""共用的 LeetCode API 呼叫工具。

alfa-leetcode-api 跑在 Render 免費方案上，閒置會休眠，冷啟動時常回空 body / 502，
所以這裡用「重試 + 退避」把睡著的實例叫醒，並把暫時性失敗和真正的成功分開。
"""
import time
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_json(url, retries=4, backoff=5, timeout=30):
    """抓取 url 並回傳解析後的 JSON。

    成功回傳 dict/list；重試用盡仍失敗時 raise，由呼叫端決定要不要擋 CI。
    """
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout)
            # Render 冷啟動 / 限流時常見 5xx，值得重試
            if resp.status_code >= 500:
                raise RuntimeError(f"API status {resp.status_code}")
            resp.raise_for_status()
            return resp.json()  # 空 body 會在這裡丟 JSONDecodeError
        except Exception as e:  # noqa: BLE001 - 連線/JSON/狀態碼一律重試
            last_err = e
            wait = backoff * attempt
            print(f"  [attempt {attempt}/{retries}] failed: {e}; retrying in {wait}s...")
            if attempt < retries:
                time.sleep(wait)
    raise RuntimeError(f"giving up after {retries} attempts: {last_err}")
