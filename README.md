<div align="center">

# 🔐 TRUMP CODE
### 川普密碼 ・ トランプ・コード

**Brute-force cryptanalysis of presidential communications × stock market.**

[![Models Tested](https://img.shields.io/badge/Models_Tested-31.5M-FF0000?style=for-the-badge&logo=pytorch&logoColor=white)](data/surviving_rules.json)
[![Surviving Rules](https://img.shields.io/badge/Survivors-50%2C872-00C853?style=for-the-badge&logo=checkmarx&logoColor=white)](data/surviving_rules.json)
[![Features](https://img.shields.io/badge/Features-316-2962FF?style=for-the-badge&logo=databricks&logoColor=white)](analysis_11_brute_force.py)
[![Data](https://img.shields.io/badge/Data-Open-FF6F00?style=for-the-badge&logo=openaccessbutton&logoColor=white)](data/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

*Can you decode the President's posts before the market moves?*

*川普發文裡藏著股市密碼。你能比市場更早解讀嗎？*

*大統領の投稿に隠された株式市場のシグナル。市場より先に解読できるか？*

[English](#the-hypothesis) · [中文](#核心假設) · [日本語](#仮説)

</div>

---

## 📊 At a Glance

```
Data:     37,000+ Truth Social posts (3 independent sources, cross-verified)
          7,411 post-inauguration originals
          289 S&P 500 / NASDAQ / VIX trading days
          564 verified predictions, 61.3% hit rate (z=5.39, p<0.05)

Engine:   384 features per day
          31,554,180 prediction models tested
          546 active rules (brute-force survivors + evolved rules)
          11 named strategy models + AI-generated rules

AI:       Claude Opus (deep analysis) + Gemini Flash (public chatbot)
          Closed-loop: predict → verify → learn → evolve → repeat
          3-tier event detection: single post → multi-day pattern → dual-platform

Markets:  Polymarket + Kalshi real-time price tracking
          Dual-track: prediction market + S&P 500 simultaneously
          6-hour TS→X arbitrage window (63% bullish historically)

Connect:  MCP Server (9 tools) · CLI (8 commands) · JSON API · Chatbot
```

---

## 🧠 System Architecture

```
Trump posts on Truth Social
         │
         ▼
┌─────────────────────────────────────────────────────┐
│  Real-Time Engine (every 5 min)                      │
│  Detect → Classify → Dual-Platform Boost →           │
│  Event Pattern Check → Snapshot PM + SPY →            │
│  Predict → Track 1h/3h/6h → Learn                    │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  Daily Pipeline (11 steps)                           │
│  Fetch → Analyze → Predict → Verify →                │
│  Circuit Breaker → PM Feedback → Learn →             │
│  Evolve (crossover/mutation/distill) →                │
│  Opus Briefing → Sync                                │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  Three Brains                                        │
│  🧠 Opus: deep causal analysis (local, no API cost)  │
│  🧬 Evolver: breeds new rules from survivors         │
│  🔒 Circuit Breaker: stops if everything is wrong    │
└─────────────────────────────────────────────────────┘
```

## 🔑 Key Discoveries (from data, not assumptions)

| # | Discovery | Evidence | Action |
|---|-----------|----------|--------|
| 1 | **RELIEF is the strongest signal** | Apr 9: +9.52% (largest single-day gain) | Confidence boosted to 0.80 |
| 2 | **TARIFF→SHORT is 70% WRONG** | Circuit breaker found this | Auto-reduced TARIFF weight |
| 3 | **China signals are hidden** | 203 posts on TS, 0 on X | China signals get 1.5x boost |
| 4 | **TS→X delay = 6.2 hours** | 38/39 matched posts, TS first | 6-hour trading window (63% up) |
| 5 | **Pre-event tariff signals = 2.7x normal** | 288 trading days analyzed | Event detector watches multi-day patterns |
| 6 | **Volume spike (131 posts/day) = crash incoming** | Mar 10: -2.70% | Volume spike alert system |
| 7 | **System is degrading** | Recent 50% vs historical 61% | Circuit breaker monitoring |
| 8 | **Errors are data too** | 3 invalid combos found from failures | Elimination learning |

## 📊 Model Leaderboard (564 verified predictions)

| Rank | Model | Win Rate | Avg Return | Trades | Status |
|------|-------|----------|------------|--------|--------|
| ⭐1 | A3 盤前 RELIEF→當天飆 | 72.7% | +1.206% | 11 | Active |
| ⭐2 | D3 發文量暴增→恐慌底部 | 70.2% | +0.306% | 47 | Boosted |
| ⭐3 | D2 簽名切換→正式聲明 | 70.0% | +0.472% | 80 | Boosted |
| 4 | B3 盤前 ACTION+正面情緒 | 66.7% | +0.199% | 33 | Active |
| 5 | C1 轟炸→沉默→做多 | 65.3% | +0.145% | 176 | Fixed (sentiment filter) |
| 6 | B1 三信號齊發→買3天 | 64.7% | +0.597% | 17 | Active |
| ⚠️ | A2 DEAL→隔天漲 | 52.2% | +0.029% | 90 | Demoted |
| ⚠️ | C2 炫耀股市→到頂 | 45.0% | +0.105% | 60 | Eliminate recommended |
| 🗑️ | C3 深夜關稅→跳空 | 37.5% | -0.414% | 8 | Eliminated (anti-indicator!) |

## 🔗 Prediction Markets

| Platform | Volume | Status | Integration |
|----------|--------|--------|-------------|
| **Polymarket** | $56B | ✅ Live | Real-time prices, signal-based arbitrage |
| **Kalshi** | $44B | ✅ Live | Cross-platform spread detection |
| **Truth Predict** | TBD | ⏳ | Waiting for TMTG to launch API |

## 🔐 Dual-Platform Intelligence (TS vs X)

| Finding | Data | Implication |
|---------|------|-------------|
| China = 100% hidden from X | 203 TS / 0 X | China signals are more authentic |
| TS publishes 6.2h before X | 38/39 posts matched | 6-hour arbitrage window |
| X posting day = market up | 63.8% up rate | He posts on X when confident |
| X day +0.109%, next day -0.087% | 168 X days analyzed | Pump effect, fades next day |
| X usage declining | 34→1 posts/month | Shifting to TS-only |

---

## The Hypothesis

> Trump is the only person on Earth who can move global markets with a single post. If there are patterns in his posting behavior — timing, word choice, emotional intensity, keyword combinations — knowing them before the market reacts is pure alpha.

## 核心假設

> 川普是地球上唯一一個「發一段文字就能撼動全球股市」的人。如果他的發文存在規律——時機、用詞、情緒強度、關鍵字組合——比市場更早解讀就是獲利先機。

## 仮説

> トランプは、たった一つの投稿で世界市場を動かせる地球上唯一の人物。投稿のタイミング、言葉選び、感情の強度、キーワードの組み合わせにパターンがあるなら、市場より先に解読することは純粋なアルファになる。

---

## 🔑 Key Discoveries | 核心發現 | 主要発見

### 1. The Tariff-Deal Seesaw | 關稅-Deal 蹺蹺板 | 関税・ディールのシーソー

|  | Signal | S&P 500 Next Day | Interpretation |
|--|--------|-----------------|----------------|
| 🔴 | Tariff during market hours | **-0.113%** | Bearish: sell pressure |
| 🟢 | Pre-market RELIEF | **+1.122%** | **Strongest buy signal found** |
| 🟡 | TARIFF + DEAL + RELIEF same day | **69% win rate** | Reversal: bottom signal |
| ⚪ | He brags about stock market | Next day **flat/down** | Contrarian: short-term top |

> **盤前出現 RELIEF（暫緩/豁免），當天 S&P 平均漲 +1.12%。這是最強的買入信號。**
>
> **市場時間中に RELIEF（一時停止/免除）が出れば、当日のS&Pは平均+1.12%。最強の買いシグナル。**

### 2. The 17-Hour Window | 17 小時操作窗口 | 17時間ウィンドウ

```
TARIFF threat  ───[ 17.4 hours median ]───▶  DEAL confirmation  ───▶  Market rally
關稅威脅        ───[   中位數 17.4 小時   ]───▶  Deal 確認信號        ───▶  股市反彈
関税の脅し      ───[   中央値 17.4 時間   ]───▶  ディール確認          ───▶  市場反発
```

### 3. The Crash Predictor | 大跌預測器 | 暴落予測

The day before S&P drops >1% vs rallies >1%:

| Feature | Before 📈 Rally | Before 📉 Crash | Signal |
|---------|:---:|:---:|--------|
| Deal mention ratio | **43.2%** | 27.7% | More Deals → Rally |
| Tariff mentions | 1.1 | **1.6** | More Tariffs → Crash |
| CAPS ratio | 12.4% | **14.4%** | More emotional → Crash |
| Sentiment score | 1.8 | **2.3** | ⚠️ *More positive before crashes* |

> **最反直覺的發現：大跌前一天他反而語氣更正面。像是在安撫。**
>
> **最も反直感的な発見：暴落の前日、彼はむしろポジティブ。まるで市場をなだめるように。**

### 4. Code Changes Detected | 密碼換碼 | コード変更検出

He changes his patterns. We track it.

| When | What Changed | Mutation Score |
|------|-------------|---------------|
| 2025-08 | New signature "President DJT" (0 → 38/month) | 5.3 |
| 2025-11 | CAPS ratio surged +3.3% (election mode) | **9.5** |
| 2025-12 | Post length dropped 122 chars, CAPS fell 5.5% | **14.1** 🚨 |
| 2026-02 | "Save America Act" — brand new phrase | New cycle |
| 2026-03 | Iran entered top-5 keywords for first time | Geopolitical shift |

---

## ⚙️ Methodology | 方法論 | 方法論

### Phase 1 — Triple-Source Data Collection | 三源資料收集 | 三重データ収集

We don't rely on any single source. Three independent pipelines fetch the same data simultaneously, cross-check each other, and catch deletions.

我們不依賴任何單一資料來源。三條獨立管線同時抓取，互相比對，捕捉刪文。

単一ソースに依存しない。3つの独立パイプラインが同時にデータを取得し、相互検証し、削除を検出する。

| Source | Method | Coverage | Update |
|--------|--------|----------|--------|
| 🔵 **CNN Archive** | Public CSV download | Full history (32K+) | Every 5 min |
| 🟢 **Self-hosted Archive** | Scrape trumpstruth.org by ID | Full history (37K+) | Daily incremental |
| 🟡 **Truth Social API** | Direct Mastodon-compatible API | Latest posts | Real-time capable |

```
Source 1 (CNN) ────────┐
Source 2 (Self-hosted) ──┼──→ Cross-Verify ──→ Merged Dataset (most complete)
Source 3 (Truth Social) ──┘        │
                                   └──→ Deletion Detection
                                         ↓
                                   "What did he post and then delete?"
```

- **Market Data:** S&P 500, NASDAQ, DOW, VIX via Yahoo Finance
- **Period:** 2025-01-20 (Inauguration) → Present (auto-updating)

### 🗑️ Deletion Detection | 刪文偵測 | 削除検出

**The most valuable signal might be what he doesn't want you to see.**

**最有價值的信號，可能是他不想讓你看到的。**

**最も価値あるシグナルは、彼があなたに見せたくないものかもしれない。**

When sources disagree — CNN captured a post but Truth Social returns 404 — that means it was **published then deleted**. We track every deletion.

| Scenario | Meaning |
|----------|---------|
| CNN ✅ + Truth Social ❌ | **Post deleted** — CNN caught it before removal |
| Self-hosted ✅ + CNN ❌ | CNN missed it — our backup saved it |
| All 3 ✅ | Post confirmed to exist |
| Source mismatch in content | Possible edit after posting |

Deletion logs: [`data/deletions.json`](data/deletions.json)

### Phase 2 — Feature Engineering (316 Features) | 特徵工程 | 特徴量エンジニアリング

Every trading day gets **316 binary features** from Trump's posts:

| Category | # | Examples |
|----------|---|---------|
| 🔤 Keyword presence | 92 | `kw_tariff`, `kw_deal`, `kw_china`, `kw_iran` |
| 🔥 Keyword intensity | 46 | `kw_tariffs_2plus`, `kw_great_heavy` |
| ⏰ Time-of-day × keyword | 58 | `pre_tariff`, `open_deal`, `night_post` |
| 📝 Style metrics | 25 | `caps_high`, `excl_extreme`, `long_posts` |
| 📊 Behavioral patterns | 35 | `volume_spike`, `tariff_streak`, `deal_no_tariff` |
| ✍️ Signature tracking | 12 | `sig_djt`, `sig_potus`, `sig_tyfa` |
| 📅 Calendar | 8 | `is_monday`, `is_friday` |
| 📈 Trend | 40 | `volume_rising_3d`, `tariff_rising` |

### Phase 3 — Brute-Force Search (31.5M Models) | 暴力搜索 | 総当たり探索

```
316 features  ×  C(316,2) + C(316,3) combinations
              ×  3 holding periods (1, 2, 3 days)
              ×  2 directions (LONG, SHORT)
              = 31,554,180 models tested
```

### Phase 4 — Two-Stage Validation | 雙段驗證 | 二段階検証

```
Training:   Jan 2025 — Nov 2025  (216 trading days)
Testing:    Dec 2025 — Mar 2026  ( 70 trading days)
Pass both → Survive
Survival rate: 0.16%  (50,872 / 31,554,180)
```

### Phase 5 — Live Monitoring | 即時監控 | ライブモニタリング

Daily automated pipeline on our VPS (Mon-Fri, post US market close):

```
┌─ Source 1: CNN Archive ──────┐
│  Source 2: Self-hosted DB ────┼──→ Cross-Verify ──→ Merged Dataset
│  Source 3: Truth Social API ──┘         │
│                                         ├──→ Deletion Detection
│                                         ↓
│  S&P 500 / NASDAQ / VIX ──→ Market Data
│                                         ↓
│                              Feature Extraction (316 dims)
│                                         ↓
│                              Run 50,872 Surviving Models
│                                         ↓
│                              Verify Yesterday's Predictions
│                                         ↓
│                              Generate Trilingual Report (EN/ZH/JA)
│                                         ↓
└───────────────────── git push ──→ This Repo Auto-Updates
```

---

## Statistical Notes

- **Multiple Testing**: With 31.5M combinations tested, we apply Bonferroni correction (α = 0.05 / 31,500,000 ≈ 1.59e-9) to identify truly significant patterns.
- **Survival Rate Context**: The 0.16% survival rate should be compared against the permutation test baseline (random data produces a baseline for comparison).
- **Minimum sample sizes**: Only models with ≥10 training trades and ≥5 test trades are considered.
- **Permutation test**: A baseline comparison using shuffled date labels is computed to quantify how many "survivors" would appear by chance alone.

---

## 📁 Open Data | 公開資料 | オープンデータ

**Everything is open. Fork it. Improve it. Prove us wrong.**

**全部公開。拿去用、拿去改、拿去打臉我們。**

**全て公開。フォークして、改善して、間違いを証明してほしい。**

### Raw Data — 40 datasets, fully open | 40 組原始資料，完全公開 | 40データセット完全公開

All data is public information scraped from public sources. Use it freely.
**Updated automatically every trading day** — new posts, new market data, new predictions.

全部是公開資料，你拿去算，算出什麼新東西就發 PR。
**每個交易日自動更新**——新推文、新股市資料、新預測結果。

全て公開情報。自由に分析してほしい。
**毎営業日自動更新**——新しい投稿、市場データ、予測結果。

#### 📡 Source Data | 原始資料 | ソースデータ

| File | Description | Records |
|------|-------------|---------|
| [`data/x_posts_full.json`](data/x_posts_full.json) | **Trump's X (Twitter) posts — full 2nd term** | 168 posts |
| [`data/market_SP500.json`](data/market_SP500.json) | S&P 500 daily OHLCV | 289 trading days |
| [`data/market_NASDAQ.json`](data/market_NASDAQ.json) | NASDAQ daily OHLCV | 289 trading days |
| [`data/market_DOW.json`](data/market_DOW.json) | Dow Jones daily OHLCV | 289 trading days |
| [`data/market_VIX.json`](data/market_VIX.json) | VIX volatility index | 289 trading days |
| [`data/daily_features.json`](data/daily_features.json) | 316 binary features per day | 414 days |
| [`data/source_check_report.json`](data/source_check_report.json) | Multi-source cross-check report | daily |

#### 🔐 Analysis Results | 分析結果 | 分析結果

| File | Description |
|------|-------------|
| [`data/results_01_caps.json`](data/results_01_caps.json) | CAPS code analysis — deliberate capitalization patterns |
| [`data/results_02_timing.json`](data/results_02_timing.json) | Posting time patterns — hourly, daily, weekly |
| [`data/results_03_hidden.json`](data/results_03_hidden.json) | Hidden messages — acrostics, number patterns, catchphrases |
| [`data/results_04_entities.json`](data/results_04_entities.json) | Country & people mention frequency + monthly trends |
| [`data/results_05_anomaly.json`](data/results_05_anomaly.json) | Anomaly detection — emotion spikes, style mutations |
| [`data/results_06_market.json`](data/results_06_market.json) | Posts vs S&P 500 correlation (with t-test) |
| [`data/results_07_signal.json`](data/results_07_signal.json) | Signal sequences — TARIFF→DEAL transition timing |
| [`data/results_08_backtest.json`](data/results_08_backtest.json) | Strategy backtesting — 7 rules vs Buy & Hold |
| [`data/results_10_codechange.json`](data/results_10_codechange.json) | Code change detection — when he changes patterns |
| [`data/results_11_bruteforce.json`](data/results_11_bruteforce.json) | Brute-force search — 31.5M models, 50K survivors |
| [`data/results_12_bigmoves.json`](data/results_12_bigmoves.json) | Big move (>1%) prediction features |

#### 🔴 X vs Truth Social Gap | 平台落差分析 | プラットフォーム比較

| File | Description |
|------|-------------|
| [`data/x_independent_analysis.json`](data/x_independent_analysis.json) | **X posts analyzed independently** — timing, topics, market impact |
| [`data/x_truth_cross_analysis.json`](data/x_truth_cross_analysis.json) | **Cross-platform gap** — selection mechanism, hidden topics, time lag |
| [`data/x_truth_full_comparison.json`](data/x_truth_full_comparison.json) | Full post-by-post matching — 39 matched, 5,267 Truth Social exclusive |
| [`data/x_truth_gap.json`](data/x_truth_gap.json) | Gap summary — 98.6% of content stays on Truth Social |

#### 🤖 Prediction Engine | 預測引擎 | 予測エンジン

| File | Description |
|------|-------------|
| [`data/surviving_rules.json`](data/surviving_rules.json) | All 50,872 model rules (features + direction + hold period) |
| [`data/monitor_rules.json`](data/monitor_rules.json) | Top 100 rules for daily monitoring |
| [`data/rules_weighted.json`](data/rules_weighted.json) | Rules with statistical weights |
| [`data/predictions_log.json`](data/predictions_log.json) | Every prediction ever made |
| [`data/daily_report.json`](data/daily_report.json) | Today's signals — trilingual (EN/ZH/JA) |
| [`data/report_history.json`](data/report_history.json) | Historical daily reports |

### Fetch Directly | 直接拉資料 | 直接取得

```bash
# Today's report (trilingual)
curl -s https://raw.githubusercontent.com/sstklen/trump-code/main/data/daily_report.json | python3 -m json.tool

# All surviving rules
curl -s https://raw.githubusercontent.com/sstklen/trump-code/main/data/surviving_rules.json

# In Python
import json, urllib.request
url = "https://raw.githubusercontent.com/sstklen/trump-code/main/data/daily_report.json"
report = json.loads(urllib.request.urlopen(url).read())
print(report['summary']['zh'])  # Chinese
print(report['summary']['ja'])  # Japanese
print(report['summary']['en'])  # English
```

---

## Installation

```bash
git clone https://github.com/sstklen/trump-code.git
cd trump-code
pip install -r requirements.txt
```

---

## 🚀 Run It Yourself | 自己跑 | 自分で実行

```bash
git clone https://github.com/sstklen/trump-code.git
cd trump-code

# Step 1: Download & clean data
python3 clean_data.py

# Step 2: Run any analysis (12 available)
python3 analysis_01_caps.py         # CAPS code analysis        | 大寫密碼    | 大文字コード
python3 analysis_02_timing.py       # Posting time patterns      | 時間規律    | 投稿時間パターン
python3 analysis_03_hidden.py       # Hidden messages (acrostic) | 藏頭詩搜索  | 隠しメッセージ
python3 analysis_04_entities.py     # Country & people mentions  | 國家人物    | 国・人物分析
python3 analysis_05_anomaly.py      # Anomaly detection          | 異常偵測    | 異常検出
python3 analysis_06_market.py       # Posts vs S&P 500           | 推文vs股市  | 投稿vs株式市場
python3 analysis_07_signal_sequence.py  # Signal sequences       | 信號序列    | シグナルシーケンス
python3 analysis_08_backtest.py     # Strategy backtesting       | 策略回測    | バックテスト
python3 analysis_10_code_change.py  # Code change detection      | 換碼偵測    | コード変更検出
python3 analysis_12_big_moves.py    # Big move prediction        | 大波動預測  | 大幅変動予測

# Step 3: Run brute-force search (takes ~25 min)
python3 overnight_search.py

# Step 4: Check today's signals
python3 trump_monitor.py --once
```

---

## 📈 Daily Report Sample | 每日報告範例 | 日次レポートサンプル

```
川普密碼每日報告 — 2026-03-15
今日推文: 11 篇 | 觸發模型: 0 組
偵測信號: Deal, 中國, 伊朗, 只有Deal沒有關稅✅
共識方向: 0 組看多 vs 0 組看空

トランプ・コード日次レポート — 2026-03-15
本日の投稿: 11件 | トリガーモデル: 0組
検出シグナル: ディール, 中国, イラン, Dealのみ（関税無し）✅

Trump Code Daily Report — 2026-03-15
Posts today: 11 | Models triggered: 0
Signals: DEAL, CHINA, IRAN, DEAL_ONLY
```

---

## 🤝 How to Contribute | 怎麼參與 | 参加方法

**We need the world's eyes on this. One team can't decode Trump alone.**

**光靠我們解不完。需要全世界的眼睛一起看。**

**一つのチームだけでは解読できない。世界中の目が必要。**

### 3 Ways to Help | 三種參與方式 | 3つの参加方法

#### 🔍 1. Propose a New Feature | 提出新特徵 | 新特徴量の提案

Think of something we're not tracking. Open an issue with:

```
Title: [FEATURE] Description
Body:
- What to track: (e.g., "count how many times he uses ALL CAPS for country names")
- Why it might matter: (e.g., "he capitalizes countries he's about to sanction")
- How to detect it: (e.g., regex pattern or keyword list)
```

**你覺得我們漏看了什麼？** 比如：「他全大寫寫國家名的時候，是不是要制裁那個國家了？」像這樣的猜測就是新特徵。開一個 issue 告訴我們。

**見逃していることはないか？** 例えば：「国名を全て大文字で書く時、その国に制裁を加えようとしているのでは？」このような仮説が新しい特徴量になる。issueを開いて教えてほしい。

#### 📊 2. Run Your Own Analysis | 跑你自己的分析 | 独自の分析を実行

```bash
git clone https://github.com/sstklen/trump-code.git
cd trump-code
python3 clean_data.py  # Get the data
# Now write your own analysis and submit a PR!
```

Ideas we haven't tried yet:

| Idea | Difficulty | Impact |
|------|-----------|--------|
| Correlate with Bitcoin/Gold/Oil prices | ⭐ Easy | High |
| Analyze image/video posts (not just text) | ⭐⭐ Medium | High |
| Track which accounts he retweets before big moves | ⭐ Easy | Medium |
| NLP sentiment in languages other than English | ⭐⭐ Medium | Medium |
| Compare 1st term tweets vs 2nd term posts | ⭐ Easy | Fun |
| Cross-reference with his public schedule | ⭐⭐ Medium | High |
| Detect if posts are written by him vs staff | ⭐⭐⭐ Hard | Very High |
| **Analyze deleted posts** — what did he delete and why? | ⭐⭐ Medium | **Critical** |
| Correlate deletion timing with market moves | ⭐⭐ Medium | Very High |
| Track post edits (before vs after version) | ⭐⭐ Medium | High |

**下載資料，跑你自己的分析，發現新規律就發 PR。** 上面那些是我們還沒試過的方向。

**データをダウンロードして、自分の分析を実行。新しいパターンを発見したらPRを送ってほしい。**

#### ✅ 3. Verify Our Predictions | 驗證我們的預測 | 予測の検証

Every day we publish predictions in `data/daily_report.json`. You can:

1. **Check if yesterday's prediction was correct** — compare with actual market close
2. **Find patterns in our failures** — when do we fail? Is there a meta-pattern?
3. **Track model decay** — which rules are dying? Which are getting stronger?

**每天看我們的預測對不對。如果發現「我們在某種情況下特別容易錯」，那本身就是一個新發現。**

**毎日の予測が正しいか確認してほしい。「特定の状況で特に間違いやすい」ことを発見すれば、それ自体が新しい発見。**

---

## 🔌 API & CLI

### Quick Start

```bash
git clone https://github.com/sstklen/trump-code.git
cd trump-code
pip install -r requirements.txt
```

### CLI Commands

```bash
python3 trump_code_cli.py signals    # Today's signals
python3 trump_code_cli.py models     # Model leaderboard
python3 trump_code_cli.py predict    # LONG or SHORT consensus
python3 trump_code_cli.py arbitrage  # Prediction market opportunities
python3 trump_code_cli.py health     # System health status
python3 trump_code_cli.py report     # Full daily report
python3 trump_code_cli.py json       # All data as JSON (for integration)
```

### JSON API (for developers)

```python
import json, subprocess
data = json.loads(subprocess.check_output(["python3", "trump_code_cli.py", "json"]))
print(data['signals'])      # Today's detected signals
print(data['models'])       # Model performance rankings
print(data['arbitrage'])    # Prediction market arbitrage opportunities
```

### MCP Server (for Claude Code / Cursor / any MCP client)

Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "trump-code": {
      "command": "python3",
      "args": ["/path/to/trump-code/mcp_server.py"]
    }
  }
}
```

Then just ask your AI:
- *"What are today's Trump Code signals?"*
- *"Show me the model leaderboard"*
- *"Any prediction market arbitrage?"*
- *"Is the system healthy?"*

9 tools available: `signals`, `models`, `predict`, `arbitrage`, `health`, `events`, `dual_platform`, `crowd`, `full_report`

### Chatbot (Gemini Flash, crowd wisdom harvesting)

```bash
export GEMINI_KEYS="your-key-1,your-key-2,your-key-3"
python3 chatbot_server.py
# Open http://localhost:8888
```

- Anonymous, daily quota (500 req/day global, 15/user)
- Share your trading logic — the best ideas get absorbed into the system! 💡
- Crowd insights available at `GET /api/insights`

### Real-Time Monitor

```bash
python3 realtime_loop.py          # Continuous (polls every 5 min)
python3 realtime_loop.py --once   # Single pass
```

Detects new posts → classifies signals → snapshots Polymarket + SPY simultaneously → predicts → verifies at 1h/3h/6h → learns

### Circuit Breaker

```bash
python3 circuit_breaker.py
```

Checks: Are we better than random? Is performance degrading? Too many consecutive errors? Auto-pauses if the system is broken.

---

## ⚠️ Disclaimer | 免責聲明 | 免責事項

> **FOR RESEARCH AND EDUCATIONAL PURPOSES ONLY.**
>
> This project is NOT financial advice. Do NOT make investment decisions based on these findings.
>
> **Statistical Limitations:**
> - The brute-force search tests 31.5 million model combinations. Even with train/test validation, many "surviving" models may be false positives due to multiple comparisons (data snooping bias).
> - Past patterns do NOT guarantee future results. Correlation ≠ causation.
> - Trump can change his communication patterns at any time.
>
> **Legal Notice:**
> - The authors assume NO liability for any financial losses incurred from using this tool.
> - Data sourced from publicly available archives. Users are responsible for compliance with applicable terms of service and local regulations.
> - This project is not affiliated with Truth Social, S&P Global, or any government entity.
>
> **Not Regulated:** This tool is not registered with any financial regulatory authority (SEC, FINRA, FSA, etc.) in any jurisdiction.

---

> **僅供研究與教育用途。**
>
> 本專案不構成投資建議。請勿根據本專案的分析結果做出任何投資決策。
>
> **統計限制：**
> - 暴力搜索測試了 3,150 萬組模型組合。即使經過訓練/測試雙段驗證，由於多重比較問題（data snooping bias），部分「存活」模型仍可能是假陽性。
> - 歷史規律不代表未來表現。相關性不等於因果關係。
> - 川普隨時可能改變發文方式。
>
> **法律免責：**
> - 作者對任何因使用本工具所產生的財務損失不承擔任何責任。
> - 資料來源為公開存檔。使用者須自行確認符合相關服務條款及當地法規。
> - 本專案與 Truth Social、S&P Global 或任何政府機構無任何隸屬關係。
>
> **未受監管：** 本工具未向任何司法管轄區的金融監管機構（SEC、FINRA、FSA 等）註冊。

---

> **研究・教育目的のみ。**
>
> 本プロジェクトは投資助言ではありません。本プロジェクトの分析結果に基づいて投資判断を行わないでください。
>
> **統計的制限：**
> - 総当たり探索では3,150万通りのモデル組み合わせをテストします。訓練/テストの二段階検証を経ても、多重比較の問題（データスヌーピングバイアス）により、一部の「生存」モデルは偽陽性である可能性があります。
> - 過去のパターンは将来の結果を保証しません。相関関係は因果関係を意味しません。
> - トランプはいつでも発信パターンを変える可能性があります。
>
> **法的免責事項：**
> - 著者は、本ツールの使用によって生じたいかなる財務的損失に対しても責任を負いません。
> - データは公開アーカイブから取得しています。ユーザーは、関連する利用規約および現地の規制への準拠について自己責任で確認してください。
> - 本プロジェクトは、Truth Social、S&P Global、または政府機関とは一切関係ありません。
>
> **未登録：** 本ツールは、いかなる司法管轄においても金融規制当局（SEC、FINRA、FSA等）への登録を行っていません。

---

<div align="center">

Built by **[Washin Mura (和心村)](https://washinmura.jp)** — Boso Peninsula, Japan.

Powered by brute-force computation, not gut feeling.

暴力運算驅動，不靠直覺。 | 直感ではなく、力任せの計算で。

---

*If you find patterns we missed, open an issue. Let's decode this together.*

*如果你發現了我們沒看到的規律，歡迎開 issue。一起來解碼。*

*見逃したパターンがあれば issue を。一緒に解読しよう。*

⭐ Star this repo to follow the live decoding.

</div>
