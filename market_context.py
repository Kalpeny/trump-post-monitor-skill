#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from typing import Any

THEME_RULES = [
    {
        "name": "关税 / 贸易",
        "patterns": [r"\btariff(s)?\b", r"trade", r"import", r"export", r"duty", r"reciprocal"],
        "impact": "宏观风险偏好波动；留意指数、工业、跨境供应链",
        "tickers": ["SPY", "QQQ", "DIA", "IWM", "CAT", "DE", "AAPL", "NVDA"],
        "bias": "risk-off",
        "weight": 4,
    },
    {
        "name": "中国 / 地缘政治",
        "patterns": [r"\bchina\b", r"beijing", r"xi", r"ccp", r"chinese"],
        "impact": "中概、半导体、苹果链、风险偏好敏感",
        "tickers": ["FXI", "KWEB", "BABA", "PDD", "AAPL", "NVDA", "SMH"],
        "bias": "mixed",
        "weight": 3,
    },
    {
        "name": "中东 / 军事冲突 / 原油",
        "patterns": [r"iran", r"israel", r"middle east", r"war", r"missile", r"strike", r"attack", r"oil", r"hormuz", r"nato", r"nuclear powered iran"],
        "impact": "油价、防务、避险情绪可能升温",
        "tickers": ["USO", "XLE", "CVX", "XOM", "LMT", "NOC", "RTX", "GLD"],
        "bias": "risk-off",
        "weight": 6,
    },
    {
        "name": "美联储 / 利率 / 通胀",
        "patterns": [r"fed", r"powell", r"interest rate", r"rates", r"inflation", r"cpi", r"ppi", r"lower rates"],
        "impact": "利率敏感资产和成长股更容易波动",
        "tickers": ["QQQ", "TLT", "IWM", "KRE", "ARKK"],
        "bias": "mixed",
        "weight": 3,
    },
    {
        "name": "财政 / 国会 / 税收",
        "patterns": [r"congress", r"senate", r"house", r"tax", r"budget", r"debt", r"treasury", r"farm bill"],
        "impact": "财政预期与中小盘、银行、国债可能联动",
        "tickers": ["IWM", "KRE", "TLT", "SPY"],
        "bias": "mixed",
        "weight": 1,
    },
    {
        "name": "移民 / 边境 / 执法",
        "patterns": [r"border", r"illegal(s)?", r"immigration", r"ice\b", r"tsa", r"homeland security", r"deport", r"airport security"],
        "impact": "偏政策与执法风险，先看国防执法、航空、劳动力预期与风险偏好",
        "tickers": ["SPY", "IWM", "JETS", "LMT", "NOC"],
        "bias": "mixed",
        "weight": 2,
    },
    {
        "name": "司法 / 选举 / 制度风险",
        "patterns": [r"election", r"voting", r"ballot", r"fraud", r"court", r"judge", r"district attorney", r"mueller", r"investigation", r"indict", r"prison", r"sentenc"],
        "impact": "政治与制度风险升温时，先看指数、波动率与媒体/平台情绪扩散",
        "tickers": ["SPY", "VIX", "DJT", "RUM"],
        "bias": "mixed",
        "weight": 2,
    },
    {
        "name": "科技 / AI / 芯片",
        "patterns": [r"\bai\b", r"chip", r"semiconductor", r"nvidia", r"technology", r"tech"],
        "impact": "科技成长与半导体链更敏感",
        "tickers": ["QQQ", "NVDA", "AMD", "SMH", "MSFT", "META"],
        "bias": "risk-on",
        "weight": 2,
    },
    {
        "name": "加密 / 特朗普币",
        "patterns": [r"\bcrypto\b", r"\bbitcoin\b", r"\bbtc\b", r"\bethereum\b", r"\beth\b", r"\$trump\b", r"\btrump coin\b"],
        "impact": "加密相关风险偏好可能同步变化",
        "tickers": ["BTC", "ETH", "COIN", "MSTR", "IBIT"],
        "bias": "risk-on",
        "weight": 2,
    },
]

POSITIVE_HINTS = [r"deal", r"relief", r"good", r"win", r"success", r"growth", r"strong", r"lower rates"]
NEGATIVE_HINTS = [r"tariff", r"war", r"attack", r"crisis", r"sanction", r"threat", r"investigation", r"emergency", r"missile", r"iran", r"oil prices", r"prison", r"fraud", r"deport", r"illegal"]
NOISE_PATTERNS = [
    r"epstein",
    r"endorsement",
    r"free tina",
    r"rino",
    r"campaign trail",
    r"make america great again",
    r"citynewsokc",
    r"townhall\.com",
    r"abcnews\.com",
    r"gold star mom",
    r"wonderful and patriotic",
]
HIGH_SIGNAL_PATTERNS = [r"iran", r"hormuz", r"oil", r"tariff", r"fed", r"rates", r"inflation", r"china", r"nato", r"missile", r"attack", r"war", r"border", r"ice\b", r"homeland security", r"election", r"voting", r"fraud", r"investigation", r"mueller"]
POLITICAL_STUMP_PATTERNS = [r"endorsement", r"campaign trail", r"re-election", r"congressman", r"vote for", r"maga", r"supporting .* re-election"]
STRONG_MARKET_PATTERNS = [r"iran", r"hormuz", r"oil", r"tariff", r"fed", r"rates", r"inflation", r"china", r"missile", r"attack", r"war", r"nato", r"border", r"ice\b", r"homeland security", r"election", r"voting", r"fraud", r"investigation"]


def parse_posts(stdin_text: str) -> list[dict[str, str]]:
    lines = stdin_text.splitlines()
    posts = []
    i = 0
    while i + 2 < len(lines):
        created = lines[i].strip()
        content = lines[i + 1].strip()
        sep = lines[i + 2].strip()
        if created and sep == "---":
            posts.append({"created_at": created, "content": content})
            i += 3
        else:
            i += 1
    return posts


def normalize_content(text: str) -> str:
    text = text.lower().replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip()


def dedupe_posts(posts: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped = []
    seen = set()
    for post in posts:
        key = normalize_content(post["content"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(post)
    return deduped


def is_noise_post(text: str) -> bool:
    lower = text.lower()
    if len(lower) < 40:
        return True
    has_high_signal = any(re.search(p, lower, re.I) for p in HIGH_SIGNAL_PATTERNS)
    if has_high_signal:
        return False
    return any(re.search(p, lower, re.I) for p in NOISE_PATTERNS)


def score_post(content: str) -> dict[str, Any]:
    text = content.lower()
    matched = []
    tickers = []
    theme_weights = Counter()
    bias_scores = Counter()

    for rule in THEME_RULES:
        if any(re.search(p, text, re.I) for p in rule["patterns"]):
            matched.append(rule)
            tickers.extend(rule["tickers"])
            theme_weights[rule["name"]] += rule["weight"]
            bias_scores[rule["bias"]] += rule["weight"]

    pos = sum(1 for p in POSITIVE_HINTS if re.search(p, text, re.I))
    neg = sum(1 for p in NEGATIVE_HINTS if re.search(p, text, re.I))
    noise = is_noise_post(text)
    high_signal = any(re.search(p, text, re.I) for p in HIGH_SIGNAL_PATTERNS)
    political_stump = any(re.search(p, text, re.I) for p in POLITICAL_STUMP_PATTERNS)
    strong_market = any(re.search(p, text, re.I) for p in STRONG_MARKET_PATTERNS)

    urgency = "low"
    if matched:
        urgency = "medium"
    if sum(theme_weights.values()) >= 6 or neg >= 2 or re.search(r"emergency|war|attack|missile|tariff|iran|oil|hormuz|nato", text, re.I):
        urgency = "high"
    elif re.search(r"border|ice\b|homeland security|election|voting|fraud|investigation|district attorney|mueller|prison", text, re.I):
        urgency = "medium"
    if noise and not high_signal and urgency != "high":
        urgency = "low"

    if not matched:
        bias = "neutral"
    else:
        risk_off = bias_scores["risk-off"]
        risk_on = bias_scores["risk-on"]
        mixed = bias_scores["mixed"]
        if risk_off >= max(risk_on + 2, mixed + 1):
            bias = "risk-off"
        elif risk_on >= max(risk_off + 3, mixed + 1):
            bias = "risk-on"
        else:
            bias = "mixed"

    if pos > neg and bias == "mixed" and not re.search(r"war|attack|missile|iran|oil|hormuz|tariff", text, re.I):
        bias = "risk-on"
    elif neg > pos and bias in {"mixed", "neutral"}:
        bias = "risk-off"

    strongest_themes = [k for k, _ in theme_weights.most_common(3)]

    score = sum(theme_weights.values()) + neg - (3 if noise and not high_signal else 0)
    if high_signal:
        score += 2
    if re.search(r"iran|hormuz|oil|tariff|fed|rates|inflation", text, re.I):
        score += 2
    if re.search(r"border|ice\b|homeland security|election|voting|fraud|investigation|district attorney|mueller|prison", text, re.I):
        score += 2
    if political_stump and not strong_market:
        score -= 6
    elif political_stump:
        score -= 3

    market_value = "low"
    if score >= 8 or urgency == "high":
        market_value = "high"
    elif score >= 4:
        market_value = "medium"

    if noise and not high_signal and score < 6:
        market_value = "low"
    if political_stump and not strong_market:
        market_value = "low"
    elif political_stump and market_value == "high":
        market_value = "medium"

    notes = []
    if bias == "risk-off":
        notes.append("优先留意指数回撤、波动率抬升、防务/能源/黄金相对强势")
    elif bias == "risk-on":
        notes.append("优先留意成长、科技、加密风险偏好抬升")
    elif matched:
        notes.append("主题已命中，但方向不单一，建议结合盘前价格与新闻流确认")

    for theme_name in strongest_themes:
        for rule in matched:
            if rule["name"] == theme_name and rule["impact"] not in notes:
                notes.append(rule["impact"])
                break

    return {
        "themes": [r["name"] for r in matched],
        "strongest_themes": strongest_themes,
        "tickers": list(dict.fromkeys(tickers))[:8],
        "bias": bias,
        "urgency": urgency,
        "notes": notes[:4],
        "noise": noise,
        "score": score,
        "market_value": market_value,
    }


def aggregate(posts: list[dict[str, str]]) -> dict[str, Any]:
    posts = dedupe_posts(posts)
    theme_counter = Counter()
    strongest_theme_counter = Counter()
    ticker_counter = Counter()
    weighted_bias = Counter()
    urgency_rank = {"low": 0, "medium": 1, "high": 2}
    top_urgency = "low"
    scored_posts = []

    for post in posts:
        s = score_post(post["content"])
        row = {"created_at": post["created_at"], "content": post["content"], **s}
        scored_posts.append(row)
        theme_counter.update(s["themes"])
        strongest_theme_counter.update(s["strongest_themes"][:1])
        ticker_counter.update(s["tickers"])
        weighted_bias[s["bias"]] += max(s["score"], 0)
        if urgency_rank[s["urgency"]] > urgency_rank[top_urgency]:
            top_urgency = s["urgency"]

    scored_posts.sort(key=lambda x: (x["market_value"] == "high", x["score"], urgency_rank[x["urgency"]]), reverse=True)

    important_posts = [x for x in scored_posts if x["market_value"] == "high"][:3]
    if not important_posts:
        important_posts = [x for x in scored_posts if x["market_value"] != "low"][:2]
    if not important_posts:
        important_posts = scored_posts[:1]

    risk_off = weighted_bias["risk-off"]
    risk_on = weighted_bias["risk-on"]
    mixed = weighted_bias["mixed"]
    if risk_off >= max(risk_on + 3, mixed + 1):
        dominant_bias = "risk-off"
    elif risk_on >= max(risk_off + 4, mixed + 1):
        dominant_bias = "risk-on"
    elif weighted_bias:
        dominant_bias = weighted_bias.most_common(1)[0][0]
    else:
        dominant_bias = "neutral"

    themes = [k for k, _ in strongest_theme_counter.most_common(4)] or [k for k, _ in theme_counter.most_common(4)]

    notes = []
    if dominant_bias == "risk-off":
        notes.append("主线仍按 risk-off 理解更稳，优先看能源、防务、黄金与指数回撤反应")
    elif dominant_bias == "risk-on":
        notes.append("若盘前量能与期货配合，可优先看科技成长和高 beta 方向")
    elif themes:
        notes.append("主线存在但方向未完全一致，先看盘前价格反馈再决定是否动作")

    for post in important_posts:
        for n in post["notes"]:
            if n not in notes:
                notes.append(n)

    return {
        "themes": themes,
        "watchlist": [k for k, _ in ticker_counter.most_common(8)],
        "bias": dominant_bias,
        "urgency": top_urgency,
        "notes": notes[:5],
        "post_count": len(posts),
        "important_posts": [
            {
                "created_at": x["created_at"],
                "content": x["content"],
                "bias": x["bias"],
                "urgency": x["urgency"],
                "score": x["score"],
                "strongest_themes": x["strongest_themes"],
                "market_value": x["market_value"],
                "noise": x["noise"],
            }
            for x in important_posts
        ],
        "noise_posts": sum(1 for x in scored_posts if x["noise"]),
        "trading_posts": sum(1 for x in scored_posts if x["market_value"] != "low"),
    }


if __name__ == "__main__":
    raw = sys.stdin.read()
    posts = parse_posts(raw)
    print(json.dumps(aggregate(posts), ensure_ascii=False))
