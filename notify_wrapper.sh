#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR"
cd "$BASE_DIR" || exit 1

LOCK_FILE="$BASE_DIR/.notify_wrapper.lock"
LOG_DIR="$BASE_DIR/logs"
LOG_FILE="$LOG_DIR/notify_wrapper.log"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-120}"
MAX_EXPAND_POSTS="${MAX_EXPAND_POSTS:-2}"
mkdir -p "$LOG_DIR"

log() {
    printf '[%s] %s\n' "$(date '+%F %T %z')" "$*" >> "$LOG_FILE"
}

fail() {
    log "error: $*"
    exit 1
}

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    log "skip: previous notify_wrapper still running"
    exit 0
fi

PREV_LAST_SEEN=""
if [ -f "data/rt_last_seen.txt" ]; then
    PREV_LAST_SEEN=$(cat "data/rt_last_seen.txt" 2>/dev/null || true)
fi

if [ ! -f "venv/bin/activate" ]; then
    fail "missing venv/bin/activate"
fi
# shellcheck disable=SC1091
source "venv/bin/activate"

if ! command -v jq >/dev/null 2>&1; then
    fail "jq not found"
fi

if [ ! -f "realtime_loop.py" ]; then
    fail "missing realtime_loop.py"
fi

if ! OUTPUT=$(timeout "$TIMEOUT_SECONDS" python3 realtime_loop.py --once 2>&1); then
    status=$?
    case "$status" in
        124) fail "timeout after ${TIMEOUT_SECONDS}s running realtime_loop.py --once" ;;
        *)
            log "realtime_loop failed with exit=$status"
            printf '%s\n' "$OUTPUT" | tail -n 80 >> "$LOG_FILE"
            exit 1
            ;;
    esac
fi

printf '%s\n' "$OUTPUT" | tail -n 80 >> "$LOG_FILE"

if ! printf '%s\n' "$OUTPUT" | grep -q "🆕 偵測到 .* 篇新推文！"; then
    log "no new post detected"
    exit 0
fi

NEW_POSTS_RAW=$(python3 - "$PREV_LAST_SEEN" <<'PY'
import json, sys
from pathlib import Path
prev = sys.argv[1] if len(sys.argv) > 1 else ''
p = Path('data/trump_posts_all.json')
if not p.exists():
    sys.exit(0)
with p.open('r', encoding='utf-8') as f:
    data = json.load(f)
posts = data.get('posts', [])
new_posts = [x for x in posts if x.get('created_at', '') > prev]
new_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
for x in new_posts[:5]:
    created = x.get('created_at', '')
    content = (x.get('content', '') or '').replace('\n', ' ').strip()
    print(created)
    print(content)
    print('---')
PY
)

if [ -z "$NEW_POSTS_RAW" ]; then
    log "new post detected in realtime_loop output but failed to extract posts newer than previous rt_last_seen"
    exit 0
fi

POST_COUNT=$(printf '%s\n' "$OUTPUT" | sed -n 's/.*🆕 偵測到 \([0-9][0-9]*\) 篇新推文！.*/\1/p' | head -n 1)
[ -z "$POST_COUNT" ] && POST_COUNT=$(printf '%s\n' "$NEW_POSTS_RAW" | grep -c '^---$' || true)

MARKET_JSON=$(printf '%s\n' "$NEW_POSTS_RAW" | python3 market_context.py)
SPY=$(printf '%s\n' "$OUTPUT" | grep 'SPY:' | head -n 1 | grep -o 'SPY: [^|]*' | sed -e 's/^[[:space:]]*//' -e 's/SPY: //')
VIX=$(printf '%s\n' "$OUTPUT" | grep 'VIX:' | head -n 1 | grep -o 'VIX: [^ ]*' | sed -e 's/^[[:space:]]*//' -e 's/VIX: //')

FINAL_MSG=$(python3 - "$MARKET_JSON" "$SPY" "$VIX" "$MAX_EXPAND_POSTS" <<'PY'
import sys, json, re

market_data = json.loads(sys.argv[1])
spy = sys.argv[2] or "N/A"
vix = sys.argv[3] or "N/A"
max_posts = int(sys.argv[4])

themes = ' / '.join(market_data.get('themes', []))
bias = market_data.get('bias', 'neutral')
urgency = market_data.get('urgency', 'low')
important_posts = market_data.get('important_posts', [])
notes = market_data.get('notes', [])
trading_posts = int(market_data.get('trading_posts', 0) or 0)
post_count = int(market_data.get('post_count', 0) or 0)

if urgency == 'low' and trading_posts == 0:
    print('NO_REPLY')
    raise SystemExit

if bias == 'risk-on':
    bias_label = '🟢 偏 Risk-On / 风险偏好回升'
    action_hint = '若盘前量价配合，优先做多成长与高 beta 标的，警惕避险资产回落。'
elif bias == 'risk-off':
    bias_label = '🔴 偏 Risk-Off / 规避风险'
    action_hint = '若油价/防务/黄金走强，顺势按防御避险思路应对，警惕科技股承压。'
elif bias == 'mixed':
    bias_label = '🟡 多空混合 / 需等待确认'
    action_hint = '方向不明，先看盘前期货与新闻流是否共振再动作。'
else:
    bias_label = '⚪️ 中性 / 暂无明显方向'
    action_hint = '暂无明确方向，维持现有策略观察。'

msg = []
if urgency == 'high':
    msg.append("🚨 **TRUMP MARKET ALERT** 🚨")
elif urgency == 'medium' and trading_posts > 0:
    msg.append("⚠️ **TRUMP MARKET WATCH** ⚠️")
else:
    msg.append("📰 **TRUMP POST UPDATE**")

if themes:
    msg.append(f"\n[ 核心催化剂 ]\n{themes}")

msg.append(f"\n[ 市场定调 ]\n{bias_label}")

watchlist = market_data.get('watchlist', [])
if watchlist:
    defense = [t for t in watchlist if t in ['USO', 'XLE', 'CVX', 'XOM', 'LMT', 'NOC', 'RTX', 'GLD', 'TLT']]
    tech = [t for t in watchlist if t in ['SPY', 'QQQ', 'NVDA', 'AAPL', 'MSFT', 'AMD', 'SMH']]
    crypto = [t for t in watchlist if t in ['BTC', 'ETH', 'COIN', 'MSTR', 'IBIT']]
    others = [t for t in watchlist if t not in defense and t not in tech and t not in crypto]

    msg.append("\n[ 关注标的 ]")
    if defense: msg.append(f"🛡️ 防务/能源/避险: {', '.join(defense)}")
    if tech: msg.append(f"🚀 大盘/科技: {', '.join(tech)}")
    if crypto: msg.append(f"🪙 加密资产: {', '.join(crypto)}")
    if others: msg.append(f"📌 其他相关: {', '.join(others)}")

if important_posts:
    msg.append("\n[ 原文速递 ]")
    for i, p in enumerate(important_posts[:max_posts]):
        created = p.get('created_at', '')
        short_time = re.sub(r'.*-(\d{2}-\d{2})T(\d{2}:\d{2}).*', r'\1 \2', created)
        content = p.get('content', '')
        if len(content) > 1500: content = content[:1499] + '…'
        msg.append(f"🕒 {short_time}\n{content}")
        if i < len(important_posts[:max_posts]) - 1:
            msg.append("---")

msg.append("\n[ 交易推演 ]")
if len(notes) > 0:
    msg.append(f"▸ 逻辑：{notes[0]}")
if len(notes) > 1:
    msg.append(f"▸ 细节：{notes[1]}")
msg.append(f"▸ 策略：{action_hint}")

msg.append(f"\n📊 大盘: SPY {spy} | VIX {vix}")
print('\n'.join(msg))
PY
)

BIAS=$(printf '%s' "$MARKET_JSON" | jq -r '.bias // "unknown"')
URGENCY=$(printf '%s' "$MARKET_JSON" | jq -r '.urgency // "unknown"')
log "alert generated successfully for ${POST_COUNT} new post(s); bias=${BIAS} urgency=${URGENCY}"
printf '%b\n' "$FINAL_MSG"
