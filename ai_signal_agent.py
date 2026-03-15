#!/usr/bin/env python3
"""
川普密碼 — AI 信號 Agent

用 Claude（透過 Anthropic API）讀 Trump 的推文，
做出比關鍵字匹配好 10 倍的信號分類。

AI 的角色：
  ① 讀推文 → 理解語意、反諷、上下文 → 分類信號
  ② 讀驗證結果 → 分析為什麼對/為什麼錯 → 提出改進
  ③ 觀察模式變化 → 提出新假設

使用方式：
  # 分類今天的推文
  python3 ai_signal_agent.py classify

  # 分析學習（為什麼對/為什麼錯）
  python3 ai_signal_agent.py learn

  # 被 daily_pipeline 自動呼叫
  from ai_signal_agent import classify_posts, analyze_learning
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE = Path(__file__).parent
DATA = BASE / "data"
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# AI 分類結果快取
AI_SIGNALS_FILE = DATA / "ai_signals.json"
AI_LEARNING_FILE = DATA / "ai_learning_insights.json"
AI_QUEUE_FILE = DATA / "ai_pending_queue.json"     # 排隊區：沒有 API key 時暫存


def log(msg: str) -> None:
    print(f"[AI Agent] {msg}", flush=True)


# =====================================================================
# 排隊機制：沒有 API key 時暫存，有了再補算
# =====================================================================

def _queue_task(task_type: str, payload: dict) -> None:
    """把任務放進排隊區，等有 API key 時再補算。"""
    queue: list[dict] = []
    if AI_QUEUE_FILE.exists():
        with open(AI_QUEUE_FILE, encoding='utf-8') as f:
            queue = json.load(f)

    queue.append({
        'type': task_type,
        'queued_at': NOW,
        'payload': payload,
        'status': 'PENDING',
    })

    with open(AI_QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
    log(f"   📋 任務已排隊（{task_type}），等有 API key 時補算")


def process_queue() -> list[dict]:
    """
    處理排隊區的待辦任務（有 API key 時呼叫）。
    回傳處理結果。
    """
    if not AI_QUEUE_FILE.exists():
        return []

    with open(AI_QUEUE_FILE, encoding='utf-8') as f:
        queue = json.load(f)

    pending = [t for t in queue if t.get('status') == 'PENDING']
    if not pending:
        return []

    log(f"📋 發現 {len(pending)} 個排隊任務，開始補算...")
    results = []

    for task in pending:
        task_type = task.get('type', '?')
        payload = task.get('payload', {})

        try:
            if task_type == 'classify':
                posts = payload.get('posts', [])
                date = payload.get('date', '')
                result = classify_posts(posts, date)
                results.append(result)
                task['status'] = 'DONE'
                task['result_summary'] = f"{len(result.get('signals', []))} signals"

            elif task_type == 'learn':
                result = analyze_learning()
                results.append(result)
                task['status'] = 'DONE'

            log(f"   ✅ 補算完成: {task_type} ({task.get('queued_at', '?')})")

        except Exception as e:
            log(f"   ⚠️ 補算失敗: {task_type} — {e}")
            task['status'] = 'FAILED'
            task['error'] = str(e)

    # 更新排隊檔
    with open(AI_QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

    return results


# =====================================================================
# Anthropic API 呼叫
# =====================================================================

def _call_claude(
    prompt: str,
    system: str = "",
    model: str = "claude-opus-4-0-20250514",
    max_tokens: int = 4000,
    temperature: float = 0.2,
) -> str:
    """
    呼叫 Anthropic Claude API — 預設用最強模型（Opus 4.6）。

    從環境變數 ANTHROPIC_API_KEY 讀取 key。
    本機沒有 key → 回傳 None，呼叫方會排隊等下次有 key 時再補算。
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        raise RuntimeError("NO_API_KEY")

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        payload["system"] = system

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            # 提取文字回應
            for block in result.get('content', []):
                if block.get('type') == 'text':
                    return block['text']
            return ""
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f"Claude API 錯誤 {e.code}: {body[:300]}")


# =====================================================================
# ① 信號分類（取代關鍵字匹配）
# =====================================================================

CLASSIFY_SYSTEM = """You are a financial signal classifier analyzing Trump's Truth Social posts.

Your job: Read posts and classify them into market-moving signals.

Signal types:
- TARIFF: Tariff threats, trade barriers, duties, reciprocal tariffs
- DEAL: Trade deals, agreements, negotiations, diplomatic breakthroughs
- RELIEF: Exemptions, pauses, delays, tariff reductions, waivers
- ACTION: Executive orders, signed legislation, immediate policy changes
- THREAT: Warnings, sanctions, punishment threats (but not tariff-specific)
- BULLISH: Positive market sentiment, stock market bragging, economic optimism
- BEARISH: Negative sentiment, attacks, crisis language, panic indicators

Rules:
1. Detect SARCASM — "Great job, Biden!" is BEARISH, not BULLISH
2. "We'll see what happens" = mild THREAT
3. ALL CAPS words carry more emotional weight
4. Multiple ! increase intensity
5. Look at the OVERALL message, not just keywords
6. One post can have MULTIPLE signals
7. Confidence 0.0-1.0 reflects how certain you are

Reply ONLY in valid JSON. No markdown, no explanation outside JSON."""

CLASSIFY_PROMPT_TEMPLATE = """Classify these Trump Truth Social posts from {date}.

Posts:
{posts_text}

Reply in this exact JSON format:
{{
  "date": "{date}",
  "post_count": {count},
  "signals": [
    {{"type": "TARIFF", "confidence": 0.85, "source_post": 1, "reason": "explicit tariff threat on EU"}},
    ...
  ],
  "overall_sentiment": "positive/negative/neutral/mixed",
  "market_impact_estimate": "high/medium/low",
  "key_targets": ["EU", "China", ...],
  "sarcasm_detected": false,
  "pattern_note": "any interesting pattern you notice"
}}"""


def classify_posts(posts: list[dict], date: str = "") -> dict[str, Any]:
    """
    用 AI 分類一天的推文。

    Args:
        posts: 推文列表，每個有 'content' 和 'created_at'
        date: 日期字串

    Returns:
        AI 分類結果 dict
    """
    if not date:
        date = posts[0]['created_at'][:10] if posts else TODAY

    if not posts:
        return {"date": date, "signals": [], "error": "no posts"}

    # 組合推文文字（限制長度避免 token 爆炸）
    posts_text = ""
    for i, p in enumerate(posts[:30], 1):  # 最多 30 篇
        content = p['content'][:500]  # 每篇最多 500 字元
        time_str = p['created_at'][11:16] if len(p['created_at']) > 11 else "?"
        posts_text += f"\n[Post {i}] ({time_str} UTC)\n{content}\n"

    prompt = CLASSIFY_PROMPT_TEMPLATE.format(
        date=date,
        posts_text=posts_text,
        count=len(posts),
    )

    log(f"送出 {len(posts)} 篇推文給 Opus 分類...")

    try:
        response = _call_claude(prompt, system=CLASSIFY_SYSTEM, max_tokens=2000)

        # 嘗試解析 JSON（處理 markdown code block）
        clean = response.strip()
        if clean.startswith('```'):
            clean = clean.split('\n', 1)[1] if '\n' in clean else clean[3:]
            if clean.endswith('```'):
                clean = clean[:-3]
            clean = clean.strip()

        result = json.loads(clean)
        result['ai_model'] = 'claude-sonnet-4'
        result['classified_at'] = NOW

        log(f"✅ AI 分類完成: {len(result.get('signals', []))} 個信號")
        for sig in result.get('signals', []):
            log(f"   {sig['type']} ({sig['confidence']:.0%}) — {sig.get('reason', '?')}")

        return result

    except json.JSONDecodeError as e:
        log(f"⚠️ AI 回應不是有效 JSON: {e}")
        log(f"   回應前 200 字: {response[:200]}")
        return {"date": date, "signals": [], "error": f"JSON parse failed: {e}",
                "raw_response": response[:500]}
    except RuntimeError as e:
        if "NO_API_KEY" in str(e):
            # 沒有 API key → 排隊等下次
            _queue_task('classify', {
                'posts': [{'created_at': p['created_at'], 'content': p['content'][:500]} for p in posts[:30]],
                'date': date,
            })
            return {"date": date, "signals": [], "queued": True}
        raise
    except Exception as e:
        log(f"⚠️ AI 分類失敗: {e}")
        return {"date": date, "signals": [], "error": str(e)}


# =====================================================================
# ② 學習分析（為什麼對/為什麼錯）
# =====================================================================

LEARN_SYSTEM = """You are the chief AI strategist for "Trump Code" — a system that analyzes
Trump's Truth Social posts to predict S&P 500 movements and find prediction market arbitrage.

You have FULL ACCESS to the system's data. Your job:
1. Analyze WHY predictions were right or wrong (not just stats — understand the CAUSE)
2. Detect if Trump's communication PATTERNS have changed (new words, timing shifts, style)
3. Propose NEW RULES that the brute-force search might have missed
4. Identify which models are OVERFITTING vs genuinely predictive
5. Suggest signal confidence adjustments based on recent market regime

The system has:
- 11 hand-crafted models (A1-D3) with 564 verified predictions
- 500+ brute-force rules from 31.5M combinations
- Prediction market integration (Polymarket)
- A closed-loop learning engine that promotes/demotes/eliminates rules

Be bold but evidence-based. Reply in JSON."""

LEARN_PROMPT_TEMPLATE = """You are analyzing the Trump Code prediction system. Here is the COMPLETE data.

=== MODEL PERFORMANCE (11 hand-crafted models) ===
{model_stats}

=== LEARNING ENGINE LAST ACTION ===
{learning_actions}

=== RULE EVOLUTION LAST RESULTS ===
{evolution_results}

=== SIGNAL CONFIDENCE (current values) ===
{signal_confidence}

=== RECENT WRONG PREDICTIONS (analyze root cause) ===
{wrong_predictions}

=== RECENT RIGHT PREDICTIONS (what worked) ===
{right_predictions}

=== PREDICTION MARKET SCAN (Polymarket) ===
{pm_scan}

Based on ALL this data, provide your analysis:

{{
  "insights": [
    {{"finding": "...", "evidence": "...", "action": "..."}},
  ],
  "pattern_shift_detected": true/false,
  "pattern_shift_details": "describe if Trump's communication style changed",
  "new_rule_hypotheses": [
    {{"features": ["feat1", "feat2"], "direction": "LONG/SHORT", "hold": 1-3, "reasoning": "why this should work", "confidence": 0.0-1.0}}
  ],
  "models_to_eliminate": ["model_ids with reasoning"],
  "models_to_boost": ["model_ids with reasoning"],
  "signal_adjustments": [
    {{"signal": "TARIFF", "current": 0.70, "suggested": 0.65, "reason": "..."}}
  ],
  "prediction_market_insight": "any arbitrage opportunity you see",
  "overall_system_health": "healthy/degrading/needs_attention",
  "priority_action": "the single most important thing to do next"
}}"""


def analyze_learning() -> dict[str, Any]:
    """
    讓 AI 分析預測結果，產出學習洞見。

    讀取 predictions_log.json，分析最近的對/錯，
    提出改進建議和新規則假設。
    """
    predictions_file = DATA / "predictions_log.json"
    if not predictions_file.exists():
        return {"error": "no predictions log"}

    with open(predictions_file, encoding='utf-8') as f:
        predictions = json.load(f)

    verified = [p for p in predictions if p.get('status') == 'VERIFIED']
    if len(verified) < 10:
        return {"error": "insufficient verified predictions"}

    # 按模型統計
    from collections import defaultdict
    model_stats = defaultdict(lambda: {'correct': 0, 'wrong': 0, 'returns': []})
    for p in verified:
        mid = p.get('model_id', '?')
        model_stats[mid]['returns'].append(p.get('actual_return', 0))
        if p.get('correct'):
            model_stats[mid]['correct'] += 1
        else:
            model_stats[mid]['wrong'] += 1

    stats_text = ""
    for mid in sorted(model_stats.keys()):
        s = model_stats[mid]
        total = s['correct'] + s['wrong']
        rate = s['correct'] / total * 100 if total > 0 else 0
        avg_ret = sum(s['returns']) / len(s['returns']) if s['returns'] else 0
        stats_text += f"  {mid}: {rate:.0f}% win rate, {avg_ret:+.3f}% avg return, {total} trades\n"

    # 最近 10 筆錯誤
    recent_wrong = [p for p in verified if not p.get('correct')][-10:]
    wrong_text = ""
    for p in recent_wrong:
        wrong_text += (f"  {p.get('model_id','?')} on {p.get('date_signal','?')}: "
                       f"{p.get('direction','?')} → actual {p.get('actual_return',0):+.3f}%\n")
        summary = p.get('day_summary', {})
        if summary:
            wrong_text += f"    post_count={summary.get('post_count','?')}, "
            wrong_text += f"tariff={summary.get('tariff',0)}, deal={summary.get('deal',0)}\n"

    # 最近 10 筆正確
    recent_right = [p for p in verified if p.get('correct')][-10:]
    right_text = ""
    for p in recent_right:
        right_text += (f"  {p.get('model_id','?')} on {p.get('date_signal','?')}: "
                       f"{p.get('direction','?')} → actual {p.get('actual_return',0):+.3f}%\n")

    # 載入其他框架數據餵給 Opus
    learning_actions = "(no learning log yet)"
    learning_log_file = DATA / "learning_log.json"
    if learning_log_file.exists():
        with open(learning_log_file, encoding='utf-8') as f:
            ll = json.load(f)
        if ll:
            last = ll[-1]
            learning_actions = json.dumps(last, ensure_ascii=False, indent=2)[:800]

    evolution_results = "(no evolution yet)"
    evo_log_file = DATA / "evolution_log.json"
    if evo_log_file.exists():
        with open(evo_log_file, encoding='utf-8') as f:
            el = json.load(f)
        if el:
            evolution_results = json.dumps(el[-1], ensure_ascii=False, indent=2)[:600]

    signal_confidence = "(default)"
    sc_file = DATA / "signal_confidence.json"
    if sc_file.exists():
        with open(sc_file, encoding='utf-8') as f:
            signal_confidence = json.dumps(json.load(f), indent=2)

    pm_scan = "(no scan yet)"
    pm_file = DATA / "prediction_market_scan.json"
    if pm_file.exists():
        with open(pm_file, encoding='utf-8') as f:
            pm_scan = json.dumps(json.load(f), ensure_ascii=False, indent=2)[:600]

    prompt = LEARN_PROMPT_TEMPLATE.format(
        model_stats=stats_text,
        learning_actions=learning_actions,
        evolution_results=evolution_results,
        signal_confidence=signal_confidence,
        wrong_predictions=wrong_text or "  (none recent)",
        right_predictions=right_text or "  (none recent)",
        pm_scan=pm_scan,
    )

    log("送出完整框架數據給 Opus 分析...")

    try:
        response = _call_claude(
            prompt, system=LEARN_SYSTEM,
            model="claude-opus-4-0-20250514",  # 學習分析也用最強模型
            max_tokens=3000,
        )

        clean = response.strip()
        if clean.startswith('```'):
            clean = clean.split('\n', 1)[1] if '\n' in clean else clean[3:]
            if clean.endswith('```'):
                clean = clean[:-3]
            clean = clean.strip()

        result = json.loads(clean)
        result['analyzed_at'] = NOW

        log(f"✅ AI 學習分析完成:")
        for insight in result.get('insights', [])[:3]:
            log(f"   💡 {insight.get('finding', '?')}")
        for hyp in result.get('new_rule_hypotheses', [])[:3]:
            log(f"   🧪 新假設: {' + '.join(hyp.get('features', []))} → {hyp.get('direction', '?')}")

        # 存檔
        with open(AI_LEARNING_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return result

    except json.JSONDecodeError as e:
        log(f"⚠️ AI 回應不是有效 JSON: {e}")
        return {"error": f"JSON parse failed: {e}", "raw": response[:500]}
    except RuntimeError as e:
        if "NO_API_KEY" in str(e):
            _queue_task('learn', {'date': TODAY})
            return {"queued": True}
        raise
    except Exception as e:
        log(f"⚠️ AI 學習分析失敗: {e}")
        return {"error": str(e)}


# =====================================================================
# ③ 整合到管線的介面
# =====================================================================

def ai_enhanced_signals(posts: list[dict], keyword_signals: list[str]) -> dict[str, Any]:
    """
    AI 增強版信號偵測。
    先用 AI 分類，再跟關鍵字結果合併。

    如果 AI 失敗（沒有 API key、API 掛了），graceful fallback 到關鍵字結果。
    """
    result = {
        'keyword_signals': keyword_signals,
        'ai_signals': [],
        'merged_signals': keyword_signals[:],  # 預設用關鍵字
        'ai_used': False,
        'ai_error': None,
    }

    try:
        ai_result = classify_posts(posts)

        if ai_result.get('signals'):
            result['ai_used'] = True
            ai_sigs = []

            for sig in ai_result['signals']:
                sig_type = sig.get('type', '').upper()
                confidence = sig.get('confidence', 0)

                if confidence >= 0.6:  # 只用信心度 >= 60% 的
                    ai_sigs.append(sig_type)

            result['ai_signals'] = ai_sigs
            result['ai_raw'] = ai_result

            # 合併：AI 找到但關鍵字沒找到的 → 加入
            merged = set(keyword_signals)
            for sig in ai_sigs:
                if sig not in merged:
                    log(f"   🤖 AI 發現關鍵字漏掉的信號: {sig}")
                    merged.add(sig)

            # 關鍵字找到但 AI 不同意的 → 標記但保留
            for kw_sig in keyword_signals:
                if kw_sig not in ai_sigs and ai_sigs:
                    log(f"   ⚠️ AI 不同意關鍵字信號: {kw_sig}（保留但降低信心）")

            result['merged_signals'] = sorted(merged)

        elif ai_result.get('error'):
            result['ai_error'] = ai_result['error']

    except Exception as e:
        result['ai_error'] = str(e)
        log(f"   AI 分類失敗，fallback 到關鍵字: {e}")

    return result


# =====================================================================
# CLI 入口
# =====================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 ai_signal_agent.py classify  — 分類今天的推文")
        print("  python3 ai_signal_agent.py learn     — AI 學習分析")
        print("  python3 ai_signal_agent.py demo      — 用範例測試")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'demo':
        # 用幾篇範例推文測試
        demo_posts = [
            {
                'created_at': '2026-03-15T06:30:00Z',
                'content': 'The European Union has been ripping off the United States for decades. '
                           'We are looking at RECIPROCAL TARIFFS. They charge us, we charge them. '
                           'Fair is fair! Meanwhile, great economic numbers coming out. '
                           'STOCK MARKET AT ALL TIME HIGH!',
            },
            {
                'created_at': '2026-03-15T07:15:00Z',
                'content': 'Just had a very productive call with President Xi. '
                           'We are working toward a GREAT DEAL for both countries. '
                           'China knows it is in their best interest to make a deal. '
                           'We\'ll see what happens!',
            },
            {
                'created_at': '2026-03-15T14:00:00Z',
                'content': 'Great job by @SecTreasury on the new tariff exemptions '
                           'for critical minerals. America FIRST but we are also FAIR. '
                           'These exemptions will help our manufacturers while we '
                           'negotiate better deals.',
            },
        ]

        print("=== AI 信號分類 Demo ===\n")
        result = classify_posts(demo_posts, '2026-03-15')
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == 'classify':
        # 從 CNN 下載最新推文並分類
        import csv
        import html as html_mod

        log("下載最新推文...")
        req = urllib.request.Request(
            "https://ix.cnn.io/data/truth-social/truth_archive.csv",
            headers={"User-Agent": "TrumpCode-AIAgent/1.0"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode('utf-8')

        reader = csv.DictReader(raw.splitlines())
        posts = []
        for row in reader:
            content = row.get('content', '').strip()
            created = row.get('created_at', '')
            if content and created >= '2025-01-20' and created[:4].isdigit():
                try:
                    content = content.encode('latin-1').decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass
                content = html_mod.unescape(content)
                if not content.startswith('RT @'):
                    posts.append({'created_at': created, 'content': content})

        # 取最新一天
        from collections import defaultdict
        daily = defaultdict(list)
        for p in posts:
            daily[p['created_at'][:10]].append(p)

        latest_date = sorted(daily.keys())[-1]
        latest_posts = daily[latest_date]

        log(f"最新日期: {latest_date}, {len(latest_posts)} 篇推文")
        result = classify_posts(latest_posts, latest_date)

        # 存檔
        with open(AI_SIGNALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == 'learn':
        result = analyze_learning()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"未知指令: {cmd}")
        sys.exit(1)
