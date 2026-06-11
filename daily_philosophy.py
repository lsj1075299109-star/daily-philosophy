#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日哲学推送 - 用于 GitHub Actions"""

import json
import urllib.request, urllib.parse
import datetime
import random
import os
import sys

SENDKEY = os.environ.get("SENDKEY", "")
QUOTES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quotes.json")

CLOSINGS = [
    "早安，愿哲学照亮你的一天。",
    "新的一天，保持思想上的清醒。",
    "与古往今来的思想者对话，是为师送你最好的早晨。",
    "思想就是自由本身。",
    "读哲学的人，永远不会孤独。",
    "乖徒儿，今天也要好好思考。",
    "这是今日的哲学时刻。",
    "哲学始于惊奇——保持好奇心。",
    "真理不在彼岸，就在你的每一次追问之中。",
    "思考不是为了得到答案，而是为了保持问题本身的活力。",
]

def load_quotes():
    with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def pick_daily_quote(quotes):
    today = datetime.date.today()
    rng = random.Random(today.strftime("%Y-%m-%d"))
    return rng.choice(quotes)

def send_wechat(title, content):
    data = urllib.parse.urlencode({
        'title': title,
        'desp': content,
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://sctapi.ftqq.com/' + SENDKEY + '.send',
        data=data, method='POST'
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode('utf-8'))

def main():
    if not SENDKEY:
        print("错误：未设置 SENDKEY 环境变量")
        sys.exit(1)
    
    quotes = load_quotes()
    entry = pick_daily_quote(quotes)
    rng = random.Random(datetime.date.today().strftime("%Y-%m-%d"))
    closing = rng.choice(CLOSINGS)
    
    today_str = datetime.date.today().strftime("%Y年%m月%d日")
    content = (
        "每日哲学 · " + today_str + "\n\n"
        "作者：" + entry["author"] + "（" + entry["era"] + "）\n\n"
        "---\n\n" + entry["text"] + "\n\n"
        "---\n\n" + closing + "\n\n"
        "——你的师尊"
    )
    
    result = send_wechat("每日哲学 | " + entry["author"], content)
    code = result.get("code", -1)
    if code == 0:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " 发送成功：" + entry["author"])
    else:
        print("发送失败：" + str(result))
        sys.exit(1)

if __name__ == "__main__":
    main()
