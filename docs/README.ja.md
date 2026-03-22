<div align="center">

# 🔐 TRUMP CODE

**AIによる大統領発言の暗号解析 × 株式市場への影響分析。**

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-trumpcode.washinmura.jp-FFD700?style=for-the-badge&logo=vercel&logoColor=white)](https://trumpcode.washinmura.jp)
[![GitHub Stars](https://img.shields.io/github/stars/sstklen/trump-code?style=for-the-badge&logo=github&color=FFD700)](https://github.com/sstklen/trump-code)

[![Models Tested](https://img.shields.io/badge/Models_Tested-31.5M-FF0000?style=flat-square)](../data/surviving_rules.json)
[![Survivors](https://img.shields.io/badge/Survivors-551-00C853?style=flat-square)](../data/surviving_rules.json)
[![Hit Rate](https://img.shields.io/badge/Hit_Rate-61.3%25-FFD700?style=flat-square)](../data/predictions_log.json)
[![Verified](https://img.shields.io/badge/Verified-566_predictions-2962FF?style=flat-square)](../data/predictions_log.json)
[![Open Data](https://img.shields.io/badge/Data-100%25_Open-FF6F00?style=flat-square)](../data/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](../LICENSE)

*市場が動く前に、大統領の投稿を解読できますか？*

[![☕ Buy Me a Claude Max](https://img.shields.io/badge/Buy_Me_a_Claude_Max-☕_Support-FF6F00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buy.stripe.com/5kQ6oI8Wk2Ui6Q3aww4c80r)

[English](../README.md) · [中文版](README.zh.md)

</div>

---

## このプロジェクトについて

トランプ氏は、SNSへの一投稿だけでグローバル市場を動かすことができる、地球上で唯一の人物です。本プロジェクトでは、ブルートフォース計算を駆使して、彼の投稿行動と株式市場の動きの間に統計的に有意なパターンを探し出します。

**直感でも意見でもなく、純粋なデータで語ります。**

- **7,400件以上の Truth Social 投稿**を分析（3つの独立したソースで相互検証）
- ブルートフォース探索により **3,150万通りのモデル組み合わせ**をテスト
- 訓練・テスト検証を通過した **551件の生存ルール**
- 566件の検証済み予測において **命中率 61.3%**（z=5.39, p<0.05）
- 閉ループシステム：予測 → 検証 → 学習 → 進化 → 毎日繰り返す

## 主な発見

| # | 発見 | 根拠データ | 市場への影響 |
|---|------|-----------|-------------|
| 1 | **寄り付き前の RELIEF = 最強の買いシグナル** | 2025/4/9：S&P +9.52% | 当日平均 +1.12% |
| 2 | **TARIFF → 空売りは70%が外れ** | サーキットブレーカー分析 | 自動的に買いへ反転 |
| 3 | **中国関連シグナルは Truth Social にのみ存在** | TS 203件 / X 0件 | 重み 1.5倍に引き上げ |
| 4 | **Truth Social は X より 6.2時間早く投稿** | 38/39件が一致 | 6時間のトレード窓 |
| 5 | **純粋な関税発表日は最も危険** | 4/3：-4.84%、4/4：-5.97% | 平均 -1.057% |
| 6 | **シグナル4つの組み合わせ = 最高収益** | 12回発生、66.7%が上昇 | 平均 +2.792% |
| 7 | **沈黙の日 = 80%は強気** | 投稿ゼロ日の分析 | 平均 +0.409% |
| 8 | **深夜の関税ツイート = 逆指標** | 62%が外れ → 逆張り = 62%が当たり | 自動反転 |

## システムアーキテクチャ

```
トランプが Truth Social に投稿
         │
         ▼ （5分ごとに検知）
┌─────────────────────────────────────────────────────┐
│  リアルタイムエンジン                                 │
│  検知 → シグナル分類 → デュアルプラットフォーム加重 → │
│  イベントパターン照合 → Polymarket + S&P 500 スナップショット → │
│  予測 → 1h/3h/6h で追跡 → 検証                       │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  デイリーパイプライン（11ステップ）                   │
│  取得 → 分析 → 551ルール実行 → 予測 →                │
│  検証 → サーキットブレーカー → Prediction Market 照合 → │
│  学習（昇格/降格/排除）→                             │
│  進化（交叉/突然変異/蒸留）→                         │
│  AI ブリーフィング → GitHub へ同期                   │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  3つの頭脳                                           │
│  🧠 Opus — 深層因果分析                              │
│  🧬 Evolver — 生存ルールから新ルールを生成            │
│  🔒 Circuit Breaker — システム劣化時に自動停止        │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────┐
│  出力                                                │
│  📊 ダッシュボード  💬 チャットボット  📡 API  💻 CLI  🤖 MCP │
└─────────────────────────────────────────────────────┘
```

## モデルリーダーボード

検証済みパフォーマンスでランク付けされた11の戦略モデル：

| # | モデル | 戦略 | 命中率 | 平均リターン | 取引回数 |
|---|--------|------|--------|-------------|---------|
| 🥇 | A3 | 寄り付き前 RELIEF → 当日急騰 | 72.7% | +1.206% | 11 |
| 🥈 | D3 | 投稿量急増 → パニック底値 | 70.2% | +0.306% | 47 |
| 🥉 | D2 | 署名スタイル変更 → 正式声明 | 70.0% | +0.472% | 80 |
| 4 | B3 | 寄り付き前 ACTION + ポジティブムード → 上昇 | 66.7% | +0.199% | 33 |
| 5 | C1 | 集中投稿 → 長い沈黙 → 買い | 65.3% | +0.145% | 176 |
| 6 | B1 | シグナル3つの組み合わせ → 3日間買い保有 | 64.7% | +0.597% | 17 |
| 7 | B2 | 3日連続関税 → 交渉転換 | 57.9% | +0.721% | 19 |
| 8 | A1 | 取引時間中の関税 → 翌日下落 | 56.5% | -0.758% | 23 |
| ⚠️ | A2 | DEAL シグナル → 翌日上昇 | 52.2% | +0.029% | 90 |
| ⚠️ | C2 | 市場自慢 → 短期天井 | 45.0% | +0.105% | 60 |
| 🗑️ | C3 | 深夜関税 → ギャップオープン（逆指標） | 37.5% | -0.414% | 8 |

## デュアルプラットフォーム分析（Truth Social vs X）

| 発見 | データ | トレードへの示唆 |
|------|--------|----------------|
| 中国シグナルは100% X に出ない | TS 203件 / X 0件 | 中国関連シグナルはより信頼性が高い |
| Truth Social は X より 6.2時間早い | 38/39件が一致 | 6時間のアービトラージ窓 |
| X 投稿は市場と相関 | r=0.35 | 自信があるときに X を使う |
| X 投稿日のリターンは7倍高い | +0.252% vs +0.037% | X 登場 = 確証シグナル |

## Prediction Markets 統合

[Polymarket](https://polymarket.com/search?_q=trump) を通じてトランプ関連の予測市場をリアルタイムで追跡：

- **316件以上のアクティブなトランプ市場**をリアルタイム追跡
- デュアルトラック・スナップショット：Polymarket 価格 + S&P 500 を同時記録
- シグナルと市場の相関分析
- [Kalshi](https://kalshi.com) クロスプラットフォームのスプレッド検知

## ライブダッシュボード

**[→ trumpcode.washinmura.jp](https://trumpcode.washinmura.jp)**

リアルタイムダッシュボードの表示内容：
- トランプ最新投稿とシグナル分析
- 今日のシグナルと市場コンセンサス
- Polymarket トランプ市場のライブ価格
- パフォーマンスバー付きモデルランキング
- 30秒ごとに自動更新

## API エンドポイント

ベース URL：`https://trumpcode.washinmura.jp`

| エンドポイント | 説明 |
|---------------|------|
| `GET /api/dashboard` | 全データを一度に取得 |
| `GET /api/signals` | 最新シグナル + 7日間の履歴 |
| `GET /api/models` | モデルパフォーマンスランキング |
| `GET /api/status` | システム健全性サマリー |
| `GET /api/recent-posts` | 最新20件のトランプ投稿 + シグナル分析 |
| `GET /api/polymarket-trump` | Polymarket トランプ予測市場のライブデータ（316件以上） |
| `GET /api/playbook` | 3つのプレイブック（ヘッジ／ポジション／ポンプ） |
| `GET /api/insights` | クラウドソーシング型トレードインサイト |
| `GET /api/data` | ダウンロード可能なデータセットカタログ |
| `GET /api/data/{file}` | 生データファイルのダウンロード |
| `POST /api/chat` | AI チャットボット（Gemini Flash） |

## オープンデータ

すべてのデータは 100% 公開です。クローンしてすぐに使えます：

| ファイル | 説明 | 更新頻度 |
|----------|------|---------|
| `trump_posts_all.json` | Truth Social 完全アーカイブ（44,000件以上） | 毎日 |
| `trump_posts_lite.json` | シグナルを事前タグ付けした投稿 | 毎日 |
| `x_posts_full.json` | X（Twitter）完全アーカイブ | 毎日 |
| `predictions_log.json` | 566件の検証済み予測と結果 | 毎日 |
| `surviving_rules.json` | 551件のアクティブルール（ブルートフォース + 進化） | 毎日 |
| `daily_report.json` | 毎日の3言語レポート | 毎日 |
| `trump_playbook.json` | 3つのプレイブック（ヘッジ／ポジション／ポンプ） | 毎週 |
| `signal_confidence.json` | シグナル信頼度スコア（自動調整） | 毎日 |
| `opus_analysis.json` | Claude Opus による深層分析 | 随時 |
| `learning_report.json` | 学習エンジンレポート | 毎日 |
| `evolution_log.json` | ルール進化ログ（交叉／突然変異） | 毎日 |
| `circuit_breaker_state.json` | システム健全性 + エラー分析 | 毎日 |
| `daily_features.json` | 384特徴量 × 414取引日 | 毎日 |
| `market_SP500.json` | S&P 500 OHLC 履歴データ | 毎日 |

## クイックスタート

```bash
# クローン
git clone https://github.com/sstklen/trump-code.git
cd trump-code
pip install -r requirements.txt

# 今日のシグナルを確認
python3 trump_code_cli.py signals

# 12種類の分析のいずれかを実行
python3 analysis_06_market.py    # 投稿 vs S&P 500 相関分析
python3 analysis_09_combo_score.py  # マルチシグナルのコンボスコア

# ブルートフォース探索を実行（約25分）
python3 overnight_search.py

# リアルタイムモニターを起動
python3 realtime_loop.py

# Webダッシュボード + チャットボットを起動
export GEMINI_KEYS="key1,key2,key3"
python3 chatbot_server.py
# → http://localhost:8888
```

## CLI コマンド

```bash
python3 trump_code_cli.py signals    # 今日検知されたシグナル
python3 trump_code_cli.py models     # モデルパフォーマンスランキング
python3 trump_code_cli.py predict    # 買い／売りのコンセンサス
python3 trump_code_cli.py arbitrage  # 予測市場のアービトラージ機会
python3 trump_code_cli.py health     # システム健全性チェック
python3 trump_code_cli.py report     # 完全な日次レポート
python3 trump_code_cli.py json       # 全データを JSON 形式で出力
```

## MCP Server（Claude Code / Cursor 向け）

`~/.claude/settings.json` に以下を追加してください：

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

9つのツール：`signals`、`models`、`predict`、`arbitrage`、`health`、`events`、`dual_platform`、`crowd`、`full_report`

## コントリビューション

**このプロジェクトには世界中の目が必要です。一つのチームだけでトランプを解読することはできません。**

### 貢献の方法

1. **新機能を提案する** — Issue を開く：何を追跡したいか、なぜ重要か、どう検知するか
2. **独自の分析を実行する** — データをクローンして、パターンを見つけ、PR を送る
3. **予測を検証する** — `daily_report.json` と実際の終値を照合する
4. **トレードロジックを共有する** — チャットボットでインサイトを共有（優れたものはシステムに取り込まれます）

### まだ試していないアイデア

| アイデア | 難易度 |
|---------|--------|
| ビットコイン／ゴールド／原油との相関分析 | 簡単 |
| 画像・動画投稿の分析 | 中程度 |
| 大きな動きの前にリツイートしたアカウントの追跡 | 簡単 |
| 公開スケジュールとのクロス参照 | 中程度 |
| 本人が書いたのか、スタッフが書いたのかの判別 | 難しい |
| 削除済み投稿と編集履歴の分析 | 中程度 |

## ファイル構成

```
trump-code/
├── public/insights.html          # ダッシュボード（シングルファイル、ビルド不要）
├── chatbot_server.py             # Web サーバー + 全 API エンドポイント
├── realtime_loop.py              # リアルタイムモニター（5分ごと）
├── daily_pipeline.py             # 日次パイプライン（11ステップ）
├── learning_engine.py            # ルールの昇格／降格／排除
├── rule_evolver.py               # 交叉／突然変異／蒸留
├── circuit_breaker.py            # システム健全性 + 自動一時停止
├── event_detector.py             # 複数日イベントパターンの検知
├── polymarket_client.py          # Polymarket API クライアント
├── kalshi_client.py              # Kalshi API クライアント
├── arbitrage_engine.py           # クロスプラットフォームのアービトラージ
├── mcp_server.py                 # MCP サーバー（9ツール）
├── trump_code_cli.py             # CLI インターフェース
├── trump_monitor.py              # 投稿モニター
├── analysis_01_caps.py           # 大文字コード分析
├── analysis_02_timing.py         # 投稿時刻パターン
├── analysis_03_hidden.py         # 隠しメッセージ（頭字語）
├── analysis_04_entities.py       # 国名・人名の言及
├── analysis_05_anomaly.py        # 異常検知
├── analysis_06_market.py         # 投稿 vs S&P 500
├── analysis_07_signal_sequence.py # シグナルシーケンス
├── analysis_08_backtest.py       # 戦略バックテスト
├── analysis_09_combo_score.py    # マルチシグナルスコア
├── analysis_10_code_change.py    # 署名変更の検知
├── analysis_11_brute_force.py    # ブルートフォースルール探索
├── analysis_12_big_moves.py      # 大きな動きの予測
├── data/                         # 全データ（100% 公開）
└── tests/                        # テストスイート
```

## 免責事項

> **本プロジェクトは研究および教育目的のみを対象としています。**
>
> 本プロジェクトは**投資助言を構成するものではありません**。本プロジェクトの分析結果に基づいて投資判断を行わないでください。
>
> **統計上の限界：**
> - 3,150万通りのモデル組み合わせをテストしました。訓練・テスト検証を実施しているものの、多重比較問題（データスヌーピングバイアス）により、生存モデルには偽陽性が含まれる可能性があります。
> - 過去のパターンは将来の結果を**保証しません**。相関関係は因果関係を意味しません。
> - トランプ氏はいつでもコミュニケーションのパターンを変えることができます。
>
> **法的事項：** 本プロジェクトの作者は、いかなる財務上の損失に対しても一切の責任を負いません。データはすべて公開アーカイブから取得しています。Truth Social、S&P Global、または政府機関とは一切関係ありません。また、いかなる金融規制当局にも登録されていません。

---

<div align="center">

**[Washin Mura（和心村）](https://washinmura.jp)** が開発 — 日本・房総半島。

直感ではなく、ブルートフォース計算で動いています。

*もし私たちが見逃したパターンを発見したら、[Issue を開いてください](https://github.com/sstklen/trump-code/issues)。一緒に解読しましょう。*

⭐ **Star を押してライブ解読の最新情報をフォローしてください。**

</div>
