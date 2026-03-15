# 交接文件
> 日期：2026-03-15 | 摘要：川普密碼從「開源分析工具」升級成「AI 閉環預測系統 + 預測市場套利 + 群眾智慧平台」

## 身份
你是 tkman 的 AI CTO。這個 session 對 trump-code 做了全面升級：審查 → 修復 → 預測市場 → 閉環學習 → AI Agent → 聊天機器人 → 即時引擎。

## 已完成（25+ commits，20 個新檔案）

### 審查與修復
- [x] 4 AI 交叉審查（Gemini+Grok+Claude+4 背景 Agent）→ 找到 48 個問題
- [x] FIXSPEC.md — 48 項改進規格書（Phase 0~6），另一邊已執行到 Phase 4
- [x] JWT Token 洩漏清除、本機路徑洩漏修復、LICENSE 加上
- [x] C1 模型情緒過濾修復（attack > positive 時不觸發做多）
- [x] 信號信心度調整（DEAL↓0.55、RELIEF↑0.80、THREAT↑0.60）

### 預測市場對接
- [x] polymarket_client.py — Polymarket API（Gamma + CLOB，即時價格、訂單簿）
- [x] kalshi_client.py — Kalshi API（公開端點，跨平台價差偵測）
- [x] signal_market_mapper.py — 5 種信號→市場映射
- [x] arbitrage_engine.py — 信號強度 × 低估程度 → 套利分數

### 閉環學習
- [x] learning_engine.py — 自動升級/降級/淘汰模型（D3↑連對9、C3🗑️37.5%）
- [x] rule_evolver.py — 規則進化：交配/突變/精煉（+46 條新規則，500→546）
- [x] pm_feedback_loop.py — 預測市場結果追蹤→自動調信號信心度

### AI Agent
- [x] ai_signal_agent.py — 本機 Opus 當大腦，產簡報包→分析→寫回
- [x] Opus 第一次分析完成（C1 根因、模式變化偵測、3 條新規則假設）

### 即時引擎（核心！）
- [x] realtime_loop.py — 每 5 分鐘偵測新推文→分類→雙軌追蹤（PM+美股）
- [x] 重大波動過濾（PM ±3¢、SPY ±0.5%，小的不學）
- [x] PM 和美股的 divergence 偵測（反應不同 = 套利信號）

### 對外介面
- [x] trump_code_cli.py — CLI 8 個指令（signals/models/predict/json...）
- [x] chatbot_server.py — Gemini Flash×3 key 聊天機器人 + 群眾智慧回收
- [x] 每日額度（500 次/天全站、15 次/人、匿名、防濫用）
- [x] README 更新（CLI/API/聊天機器人使用指引）

## 進行中
- [ ] 「事件級別」定義 — tkman 說不只看漲跌幅，要看有沒有「造成一個事件」
- [ ] Polymarket 市場搜尋優化 — tag 搜尋回 0，需改用 keyword search
- [ ] 群眾洞見→自動回測 — 用戶邏輯存了但還沒自動驗證
- [ ] Opus 建議的新規則→自動加入規則庫

## 已知問題
- 另一邊同時在改 repo，經常 git conflict（已用 rebase 處理，但要注意分工）
- Kalshi 目前 0 個 Trump 市場（CFTC 限制），client 就位但沒數據可追蹤
- realtime_loop.py 的 PM 追蹤回 0 個市場（Gamma API tag 搜尋問題）
- CNN Archive 的 CSV 有髒資料（URL 出現在 created_at 欄位）

## 下一步（按優先順序）

### 🔴 最重要：「事件」定義
tkman 說的：不是漲跌幅，是「有沒有造成一件事」。需要定義：
- PM 價格跳變 ≥10¢ = 事件
- SPY 日內波動 ≥1% = 事件
- 其他國家/機構回應 = 事件（需要新聞 API）
```python
# 在 realtime_loop.py 加入事件偵測
EVENT_THRESHOLDS = {'pm_jump': 0.10, 'spy_intraday': 1.0}
```

### 🔴 修 Polymarket 搜尋
```bash
# 測試不同搜尋方式
cd /tmp/trump-code && python3 -c "
from polymarket_client import search_markets
# 嘗試用 keyword 而非 tag
print(search_markets('tariff'))
"
```

### 🟡 部署聊天機器人到 VPS
```bash
# 需要 tkman 說「部署」
python3 chatbot_server.py  # 目前只能本機跑
# 部署後需要 Caddy 反代 + 域名
```

### 🟡 跑一輪完整管線測試
```bash
cd /tmp/trump-code && python3 daily_pipeline.py
# 確認 10 步都跑得過
```

### 🟢 群眾洞見公開頁面
目前 `/api/insights` 有 JSON，但沒有好看的網頁讓人瀏覽

## 關鍵路徑
```
/tmp/trump-code/
├── daily_pipeline.py        ← 每日管線（10 步）
├── realtime_loop.py         ← 即時引擎（每 5 分鐘）
├── learning_engine.py       ← 閉環學習
├── rule_evolver.py          ← 規則進化
├── ai_signal_agent.py       ← Opus 簡報包
├── pm_feedback_loop.py      ← 預測市場回饋
├── polymarket_client.py     ← Polymarket API
├── kalshi_client.py         ← Kalshi API
├── arbitrage_engine.py      ← 套利引擎
├── signal_market_mapper.py  ← 信號→市場映射
├── trump_code_cli.py        ← CLI 工具
├── chatbot_server.py        ← 聊天機器人
├── trump_monitor.py         ← 即時監控（11 模型）
├── overnight_search.py      ← 暴力搜索
├── analysis_01~12_*.py      ← 12 個分析模組
├── FIXSPEC.md               ← 改進規格書
└── data/                    ← 所有數據（39 個檔案）
    ├── opus_briefing.txt    ← 給 Opus 的簡報
    ├── opus_analysis.json   ← Opus 的分析結果
    ├── signal_confidence.json
    ├── surviving_rules.json ← 546 條存活規則
    ├── rt_predictions.json  ← 即時預測紀錄
    └── crowd_insights.json  ← 群眾智慧
```

## GitHub
https://github.com/sstklen/trump-code (public)

## 系統規模
- 34 個 Python 檔案，13,251 行代碼
- 546 條存活規則 + 11 個命名模型
- 564 筆已驗證預測
- 對接 2 個預測市場（Polymarket + Kalshi）
- 3 把 Gemini key 輪用
