<div align="center">

# 🔐 TRUMP CODE

**用 AI 解碼總統發文 × 分析股市衝擊。**

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-trumpcode.washinmura.jp-FFD700?style=for-the-badge&logo=vercel&logoColor=white)](https://trumpcode.washinmura.jp)
[![GitHub Stars](https://img.shields.io/github/stars/sstklen/trump-code?style=for-the-badge&logo=github&color=FFD700)](https://github.com/sstklen/trump-code)

[![Models Tested](https://img.shields.io/badge/Models_Tested-31.5M-FF0000?style=flat-square)](../data/surviving_rules.json)
[![Survivors](https://img.shields.io/badge/Survivors-551-00C853?style=flat-square)](../data/surviving_rules.json)
[![Hit Rate](https://img.shields.io/badge/Hit_Rate-61.3%25-FFD700?style=flat-square)](../data/predictions_log.json)
[![Verified](https://img.shields.io/badge/Verified-566_predictions-2962FF?style=flat-square)](../data/predictions_log.json)
[![Open Data](https://img.shields.io/badge/Data-100%25_Open-FF6F00?style=flat-square)](../data/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](../LICENSE)

*你能在市場動之前，先解讀出總統的下一步嗎？*

[![☕ Buy Me a Claude Max](https://img.shields.io/badge/Buy_Me_a_Claude_Max-☕_Support-FF6F00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buy.stripe.com/5kQ6oI8Wk2Ui6Q3aww4c80r)

[English](../README.md) · [日本語](README.ja.md)

</div>

---

## 這是什麼？

川普是地球上唯一一個能用一則社群貼文撼動全球市場的人。這個專案用暴力運算的方式，找出他發文行為與股市走勢之間在統計上顯著的規律。

**不靠直覺，不談看法，只看數據。**

- 分析了 **7,400+ 則 Truth Social 貼文**（三個獨立來源交叉驗證）
- 暴力搜尋測試了 **3,150 萬種模型組合**
- **551 條存活規則**通過訓練集 / 測試集雙重驗證
- **566 筆已驗收預測的命中率達 61.3%**（z=5.39, p<0.05）
- 閉環系統：預測 → 驗收 → 學習 → 進化 → 每日循環

## 重要發現

| # | 發現 | 數據依據 | 市場影響 |
|---|------|----------|----------|
| 1 | **盤前出現 RELIEF = 最強買入訊號** | 2025/4/9：S&P +9.52% | 當日平均 +1.12% |
| 2 | **TARIFF → 放空的正確率只有 30%** | 熔斷器分析 | 自動反轉為做多 |
| 3 | **中國相關訊號只藏在 Truth Social** | 203 篇 TS 貼文 / X 上零篇 | 權重提升 1.5 倍 |
| 4 | **Truth Social 比 X 早 6.2 小時發布** | 38/39 篇貼文吻合 | 6 小時交易時間窗口 |
| 5 | **純關稅日是最危險的交易日** | 4/3：-4.84%，4/4：-5.97% | 平均 -1.057% |
| 6 | **4 訊號組合 = 最高獲利** | 12 次出現，66.7% 上漲 | 平均 +2.792% |
| 7 | **沉默日 = 八成看多** | 零貼文日分析 | 平均 +0.409% |
| 8 | **深夜關稅推文 = 反指標** | 62% 預測錯 → 反向操作 = 62% 正確 | 自動反轉 |

## 系統架構

```
川普在 Truth Social 發文
         │
         ▼ (每 5 分鐘偵測)
┌─────────────────────────────────────────────────────┐
│  即時引擎                                            │
│  偵測 → 分類訊號 → 雙平台加權 →                     │
│  事件模式比對 → 快照 Polymarket + S&P 500 →          │
│  預測 → 1h/3h/6h 追蹤 → 驗收                        │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  每日流水線（11 個步驟）                             │
│  拉資料 → 分析 → 跑 551 條規則 → 預測 →             │
│  驗收 → 熔斷器 → Prediction Market 比對 →           │
│  學習（升級/降級/淘汰）→                            │
│  進化（交叉/突變/提煉）→                            │
│  AI 簡報 → 同步到 GitHub                            │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  三個大腦                                            │
│  🧠 Opus — 深度因果分析                              │
│  🧬 Evolver — 從存活規則中繁殖新規則                 │
│  🔒 Circuit Breaker — 系統退化時自動暫停             │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  輸出                                                │
│  📊 儀表板  💬 聊天機器人  📡 API  💻 CLI  🤖 MCP   │
└─────────────────────────────────────────────────────┘
```

## 模型排行榜

11 個命名策略模型，依實際驗收績效排名：

| # | 模型 | 策略 | 命中率 | 平均報酬 | 交易次數 |
|---|------|------|--------|----------|----------|
| 🥇 | A3 | 盤前 RELIEF → 當日大漲 | 72.7% | +1.206% | 11 |
| 🥈 | D3 | 貼文量驟升 → 恐慌底部 | 70.2% | +0.306% | 47 |
| 🥉 | D2 | 署名方式切換 → 正式聲明 | 70.0% | +0.472% | 80 |
| 4 | B3 | 盤前 ACTION + 正向情緒 → 上漲 | 66.7% | +0.199% | 33 |
| 5 | C1 | 密集發文 → 長時間沉默 → 做多 | 65.3% | +0.145% | 176 |
| 6 | B1 | 3 訊號組合 → 持多 3 天 | 64.7% | +0.597% | 17 |
| 7 | B2 | 連 3 天關稅 → 轉向談判 | 57.9% | +0.721% | 19 |
| 8 | A1 | 盤中關稅 → 隔日下跌 | 56.5% | -0.758% | 23 |
| ⚠️ | A2 | DEAL 訊號 → 隔日上漲 | 52.2% | +0.029% | 90 |
| ⚠️ | C2 | 市場吹噓 → 短期頭部 | 45.0% | +0.105% | 60 |
| 🗑️ | C3 | 深夜關稅 → 跳空開盤（反指標） | 37.5% | -0.414% | 8 |

## 雙平台情報（Truth Social vs X）

| 發現 | 數據 | 交易含義 |
|------|------|----------|
| 中國訊號 100% 不出現在 X | TS 203 篇 / X 0 篇 | 中國相關訊號更真實可信 |
| Truth Social 比 X 早 6.2 小時 | 38/39 篇吻合 | 6 小時套利時間窗口 |
| X 發文與市場走勢有相關性 | r=0.35 | 他在有把握時才用 X |
| X 發文當日報酬高出 7 倍 | +0.252% vs +0.037% | X 出現 = 確認訊號 |

## 預測市場整合

透過 [Polymarket](https://polymarket.com/search?_q=trump) 即時追蹤川普相關預測市場：

- 即時追蹤 **316+ 個活躍川普市場**
- 雙軌快照：Polymarket 價格 + S&P 500 同步紀錄
- 訊號與市場走勢的相關性分析
- [Kalshi](https://kalshi.com) 跨平台價差偵測

## 即時儀表板

**[→ trumpcode.washinmura.jp](https://trumpcode.washinmura.jp)**

即時儀表板顯示：
- 最新川普貼文及訊號解析
- 今日訊號與市場共識
- Polymarket 川普市場即時行情
- 模型排名與績效長條圖
- 每 30 秒自動更新

## API Endpoints

Base URL：`https://trumpcode.washinmura.jp`

| Endpoint | 說明 |
|----------|------|
| `GET /api/dashboard` | 一次取得所有資料 |
| `GET /api/signals` | 最新訊號 + 7 天歷史 |
| `GET /api/models` | 模型績效排名 |
| `GET /api/status` | 系統健康摘要 |
| `GET /api/recent-posts` | 最新 20 則川普貼文 + 訊號解析 |
| `GET /api/polymarket-trump` | Polymarket 川普預測市場即時資料（316+） |
| `GET /api/playbook` | 三本操作手冊（避險 / 建倉 / 拉盤） |
| `GET /api/insights` | 群眾眾包交易洞察 |
| `GET /api/data` | 可下載資料集目錄 |
| `GET /api/data/{file}` | 下載原始資料檔案 |
| `POST /api/chat` | AI 聊天機器人（Gemini Flash） |

## 開放資料

所有資料 100% 公開。Clone 下來直接用：

| 檔案 | 說明 | 更新頻率 |
|------|------|----------|
| `trump_posts_all.json` | Truth Social 完整存檔（44,000+ 篇） | 每日 |
| `trump_posts_lite.json` | 已預標記訊號的貼文 | 每日 |
| `predictions_log.json` | 566 筆已驗收預測含結果 | 每日 |
| `surviving_rules.json` | 551 條活躍規則（暴力搜尋 + 進化產出） | 每日 |
| `daily_report.json` | 每日三語報告 | 每日 |
| `trump_playbook.json` | 三本操作手冊（避險 / 建倉 / 拉盤） | 每週 |
| `signal_confidence.json` | 訊號置信度分數（自動調整） | 每日 |
| `opus_analysis.json` | Claude Opus 深度分析 | 隨需產出 |
| `learning_report.json` | 學習引擎報告 | 每日 |
| `evolution_log.json` | 規則進化記錄（交叉 / 突變） | 每日 |
| `circuit_breaker_state.json` | 系統健康 + 錯誤分析 | 每日 |
| `daily_features.json` | 384 個特徵 × 414 個交易日 | 每日 |
| `market_SP500.json` | S&P 500 OHLC 歷史資料 | 每日 |

## 快速開始

```bash
# Clone 專案
git clone https://github.com/sstklen/trump-code.git
cd trump-code
pip install -r requirements.txt

# 查看今日訊號
python3 trump_code_cli.py signals

# 跑任一分析腳本（共 12 個）
python3 analysis_06_market.py    # 貼文 vs S&P 500 相關性
python3 analysis_09_combo_score.py  # 多訊號組合評分

# 跑暴力搜尋（約 25 分鐘）
python3 overnight_search.py

# 啟動即時監控
python3 realtime_loop.py

# 啟動網頁儀表板 + 聊天機器人
export GEMINI_KEYS="key1,key2,key3"
python3 chatbot_server.py
# → http://localhost:8888
```

## CLI 指令

```bash
python3 trump_code_cli.py signals    # 今日偵測到的訊號
python3 trump_code_cli.py models     # 模型績效排行榜
python3 trump_code_cli.py predict    # 做多/做空共識
python3 trump_code_cli.py arbitrage  # 預測市場套利機會
python3 trump_code_cli.py health     # 系統健康狀態
python3 trump_code_cli.py report     # 完整每日報告
python3 trump_code_cli.py json       # 以 JSON 格式輸出所有資料
```

## MCP Server（給 Claude Code / Cursor 用）

在 `~/.claude/settings.json` 加入：

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

共 9 個工具：`signals`、`models`、`predict`、`arbitrage`、`health`、`events`、`dual_platform`、`crowd`、`full_report`

## 一起來貢獻

**我們需要全世界的眼睛一起盯著這件事。一個團隊解碼不了川普。**

### 可以怎麼幫

1. **提新功能建議** — 開 issue：想追蹤什麼、為什麼重要、怎麼偵測
2. **自己跑分析** — Clone 資料，找出規律，提 PR
3. **驗收預測** — 對照 `daily_report.json` 與實際收盤
4. **分享交易邏輯** — 用聊天機器人分享洞察（最好的會被系統吸收）

### 還沒試過的方向

| 方向 | 難度 |
|------|------|
| 與比特幣 / 黃金 / 石油做相關性分析 | 容易 |
| 分析圖片 / 影片貼文 | 中等 |
| 追蹤他在大行情前轉推了哪些帳號 | 容易 |
| 與他的公開行程交叉比對 | 中等 |
| 辨別貼文是他本人寫的還是幕僚代筆 | 困難 |
| 分析已刪除貼文及編輯記錄 | 中等 |

## 檔案結構

```
trump-code/
├── public/insights.html          # 儀表板（單一檔案，免打包）
├── chatbot_server.py             # Web 伺服器 + 所有 API endpoints
├── realtime_loop.py              # 即時監控（每 5 分鐘）
├── daily_pipeline.py             # 每日流水線（11 個步驟）
├── learning_engine.py            # 升級 / 降級 / 淘汰規則
├── rule_evolver.py               # 交叉 / 突變 / 提煉
├── circuit_breaker.py            # 系統健康 + 自動暫停
├── event_detector.py             # 多日事件模式偵測
├── polymarket_client.py          # Polymarket API 客戶端
├── kalshi_client.py              # Kalshi API 客戶端
├── arbitrage_engine.py           # 跨平台套利引擎
├── mcp_server.py                 # MCP server（9 個工具）
├── trump_code_cli.py             # CLI 介面
├── trump_monitor.py              # 貼文監控器
├── analysis_01_caps.py           # 大寫密碼分析
├── analysis_02_timing.py         # 發文時間規律
├── analysis_03_hidden.py         # 隱藏訊息（藏頭詩式）
├── analysis_04_entities.py       # 國家與人名提及
├── analysis_05_anomaly.py        # 異常偵測
├── analysis_06_market.py         # 貼文 vs S&P 500
├── analysis_07_signal_sequence.py # 訊號序列分析
├── analysis_08_backtest.py       # 策略回測
├── analysis_09_combo_score.py    # 多訊號評分
├── analysis_10_code_change.py    # 署名變化偵測
├── analysis_11_brute_force.py    # 暴力搜尋規則
├── analysis_12_big_moves.py      # 大行情預測
├── data/                         # 所有資料（100% 公開）
└── tests/                        # 測試套件
```

## 免責聲明

> **僅供研究與教育用途。**
>
> 本專案**不構成任何投資建議**。請勿依據本專案的研究結果做出任何投資決策。
>
> **統計局限性：**
> - 本專案測試了 3,150 萬種模型組合。即使經過訓練集 / 測試集驗證，存活模型仍可能因多重比較問題（資料挖掘偏差）而包含偽陽性結果。
> - 過去的規律**不保證**未來的表現。相關性不等於因果關係。
> - 川普隨時可能改變他的溝通方式。
>
> **法律聲明：** 本專案作者對任何財務損失概不負責。資料來源均為公開存檔，與 Truth Social、S&P Global 或任何政府機構無關，亦未向任何金融監管機構登記。

---

<div align="center">

由 **[Washin Mura（和心村）](https://washinmura.jp)** 打造 — 日本房總半島。

靠暴力運算，不靠直覺。

*如果你發現了我們遺漏的規律，[歡迎開 issue](https://github.com/sstklen/trump-code/issues)。一起來解碼。*

⭐ **按下 Star 追蹤即時解碼進度。**

</div>
div>
