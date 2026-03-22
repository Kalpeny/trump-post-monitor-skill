<div align="center">

# 🔐 TRUMP POST MONITOR

**Real-time Trump Truth Social monitor with market-aware alerts.**  
**一个面向市场提醒的川普 Truth Social 实时监控器。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Data](https://img.shields.io/badge/Data-Open-FF6F00?style=flat-square)](data/)
[![Runtime](https://img.shields.io/badge/Runtime-Python-2962FF?style=flat-square)](requirements.txt)

</div>

---

## What This Repo Is / 这个仓库现在是干什么的

This repo is now focused on a **practical real-time monitoring pipeline**:

- fetch Trump posts from multiple sources
- detect newly published posts every few minutes
- classify market impact
- turn high/medium-signal posts into readable alerts
- enrich alerts with Polymarket / market context
- support wrapper-based cron delivery

这个仓库现在聚焦在一条**实用型实时监控链路**上：

- 从多个来源抓取川普帖子
- 每隔几分钟检测是否有新帖
- 判断帖文的市场影响
- 把高/中信号内容整理成可读提醒
- 结合 Polymarket 和市场上下文补充说明
- 支持通过 wrapper + cron 做自动投递

It is no longer positioned as a giant all-in-one research archive. The repo has been trimmed to keep the **live monitoring path** clearer and easier to maintain.

它不再定位成一个“大而全”的研究档案仓库，而是收缩成一个**更清晰、可维护的实时监控项目**。

---

## Current Core Workflow / 当前核心流程

```text
Truth Social / archive sources
        ↓
multi_source_fetcher.py
        ↓
realtime_loop.py
        ↓
market_context.py
        ↓
notify_wrapper.sh
        ↓
cron / chat delivery
```

### Core files / 核心文件

- `realtime_loop.py` — polling loop and new-post detection  
  轮询主循环与新帖检测
- `market_context.py` — market-theme classification, bias/urgency scoring, watchlist extraction  
  市场主题分类、方向/紧急度打分、关注标的提取
- `notify_wrapper.sh` — wrapper for cron/manual runs; outputs alert text / `NO_REPLY` / error  
  cron/手动运行包装器；输出提醒正文、`NO_REPLY` 或错误
- `multi_source_fetcher.py` — combines multiple post sources  
  聚合多个帖子来源
- `trump_monitor.py` — monitoring-related utilities and older monitor flow  
  监控相关工具与较旧监控流程
- `chatbot_server.py` — lightweight dashboard/API server  
  轻量 dashboard / API 服务
- `trump_code_cli.py` — local CLI entrypoints  
  本地命令行入口

---

## What Was Improved Recently / 最近做过的优化

### Monitoring reliability / 监控可靠性

- fixed wrapper path bugs
- fixed silent failure cases
- added explicit `NO_REPLY` behavior for no-signal runs
- added explicit `🚨 TRUMP MONITOR ERROR` output for real failures
- added runtime artifact ignores for lock/log/state junk

对应中文：

- 修复了 wrapper 路径错误
- 修复了“静默失败”问题
- 对无信号场景显式输出 `NO_REPLY`
- 对真实运行异常显式输出 `🚨 TRUMP MONITOR ERROR`
- 补充忽略规则，避免锁文件/日志/运行垃圾污染仓库

### Signal quality / 信号质量

- expanded market mapping rules
- added tiered alert routing (`alert` / `watch` / `silent`)
- improved dedupe behavior for repeated posts
- added `FORCE_REPLAY_SINCE` for replay/backtesting specific historical windows

对应中文：

- 扩大了市场映射规则
- 增加分级提醒（`alert` / `watch` / `silent`）
- 优化重复帖去重逻辑
- 增加 `FORCE_REPLAY_SINCE`，方便回放历史窗口做测试

### Delivery / 投递链路

- wrapper output is now suitable for cron/chat relay
- message formatting is optimized for short, readable monitoring alerts

对应中文：

- wrapper 输出已经适合接入 cron / 聊天投递链路
- 提醒格式针对短消息阅读做了优化

---

## Alert Semantics / 提醒输出语义

The wrapper returns one of three outcomes:

### 1. `NO_REPLY`
No meaningful new post, or low-signal content that should stay silent.  
没有值得提醒的新帖，或者只是低信号噪音，应该静默。

### 2. Alert text
A real monitoring message with:
- catalyst/theme
- market bias
- urgency
- watchlist
- translated / summarized explanation
- optional original quote excerpts

也就是一条真正要发出去的提醒，通常会包含：
- 催化剂 / 主题
- 市场方向
- 紧急程度
- 关注标的
- 中文翻译 / 中文总结
- 必要时附英文原文摘录

### 3. `🚨 TRUMP MONITOR ERROR`
Something operational broke and should be surfaced instead of failing silently.  
说明运行链路出错，不应该静默吞掉，而应该直接暴露出来。

---

## Quick Start / 快速开始

```bash
git clone https://github.com/Kalpeny/trump-post-monitor-skill.git
cd trump-post-monitor-skill
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run one real-time pass / 跑一次实时检测

```bash
python3 realtime_loop.py --once
```

### Run wrapper manually / 手动跑 wrapper

```bash
bash ./notify_wrapper.sh
```

### Replay historical posts for testing / 回放历史帖子做测试

```bash
FORCE_REPLAY_SINCE='2026-03-21T18:00:00.000Z' bash ./notify_wrapper.sh
```

### Start local dashboard/API / 启动本地 dashboard/API

```bash
python3 chatbot_server.py
```

---

## Main Data Files / 当前主要数据文件

These are the key files still relevant to the active monitor flow:

- `data/trump_posts_all.json` — full Trump post archive used for extraction/replay  
  完整帖子归档，用于提取与回放
- `data/trump_posts_lite.json` — lighter derived view  
  轻量衍生视图
- `data/rt_last_seen.txt` — last processed timestamp for real-time flow  
  实时流最后处理到的时间戳
- `data/rt_predictions.json` — recent real-time signal output  
  最近实时信号输出
- `data/polymarket_live.json` — latest prediction market snapshot  
  最新预测市场快照
- `data/trump_coin_history.json` — related market context data  
  相关市场上下文数据
- `data/trump_playbook.json` — playbook / scenario reference  
  剧本 / 情景参考

---

## API / UI

`chatbot_server.py` provides a lightweight dashboard/API layer for local use.  
`chatbot_server.py` 提供轻量本地 dashboard / API 服务。

Examples / 例子:

- `/api/status`
- `/api/dashboard`
- `/api/signals`
- `/api/recent-posts`
- `/api/data`

The public HTML dashboard lives in / 前端页面位置：

- `public/insights.html`

---

## Repo Cleanup Notes / 仓库精简说明

The repo has already been pruned to remove:

- temporary test files
- wrapper runtime junk
- legacy Musk/X comparison artifacts
- dead download links pointing to removed files

这个仓库已经做过一轮精简，删除了：

- 临时测试文件
- wrapper 运行垃圾
- 旧的 Musk / X 对照研究残留
- 指向已删除文件的无效下载链接

The goal is to keep this repository centered on the **current Trump monitoring and alerting pipeline**, not a sprawling research dump.

目标是让仓库围绕**当前可用的监控与提醒主链路**，而不是继续维持一个臃肿的研究大杂烩。

---

## Development Notes / 开发说明

If you change the monitor flow, validate at least these paths:

```bash
python3 realtime_loop.py --once
bash ./notify_wrapper.sh
FORCE_REPLAY_SINCE='2026-03-21T18:00:00.000Z' bash ./notify_wrapper.sh
```

Recommended checks / 建议验证：

- no new posts → `NO_REPLY`
- real catalyst posts → readable alert
- operational failure → `🚨 TRUMP MONITOR ERROR`

对应中文：

- 没有新帖 → `NO_REPLY`
- 真正的市场催化帖 → 能生成可读提醒
- 运行失败 → `🚨 TRUMP MONITOR ERROR`

---

## License / 许可证

MIT
