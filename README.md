<div align="center">

# 🔐 TRUMP POST MONITOR

**Real-time Trump Truth Social monitor with market-aware alerts.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Data](https://img.shields.io/badge/Data-Open-FF6F00?style=flat-square)](data/)
[![Runtime](https://img.shields.io/badge/Runtime-Python-2962FF?style=flat-square)](requirements.txt)

</div>

---

## What This Repo Is

This repo is now focused on a **practical real-time monitoring pipeline**:

- fetch Trump posts from multiple sources
- detect newly published posts every few minutes
- classify market impact
- turn high/medium-signal posts into readable alerts
- enrich alerts with Polymarket / market context
- support wrapper-based cron delivery

It is no longer positioned as a giant all-in-one research archive. The repo has been trimmed to keep the **live monitoring path** clearer and easier to maintain.

---

## Current Core Workflow

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

### Core files

- `realtime_loop.py` — polling loop and new-post detection
- `market_context.py` — market-theme classification, bias/urgency scoring, watchlist extraction
- `notify_wrapper.sh` — wrapper for cron/manual runs; outputs alert text / `NO_REPLY` / error
- `multi_source_fetcher.py` — combines multiple post sources
- `trump_monitor.py` — monitoring-related utilities and older monitor flow
- `chatbot_server.py` — lightweight dashboard/API server
- `trump_code_cli.py` — local CLI entrypoints

---

## What Was Improved Recently

### Monitoring reliability

- fixed wrapper path bugs
- fixed silent failure cases
- added explicit `NO_REPLY` behavior for no-signal runs
- added explicit `🚨 TRUMP MONITOR ERROR` output for real failures
- added runtime artifact ignores for lock/log/state junk

### Signal quality

- expanded market mapping rules
- added tiered alert routing (`alert` / `watch` / `silent`)
- improved dedupe behavior for repeated posts
- added `FORCE_REPLAY_SINCE` for replay/backtesting specific historical windows

### Delivery

- wrapper output is now suitable for cron/chat relay
- message formatting is optimized for short, readable monitoring alerts

---

## Alert Semantics

The wrapper returns one of three outcomes:

### 1. `NO_REPLY`
No meaningful new post, or low-signal content that should stay silent.

### 2. Alert text
A real monitoring message with:
- catalyst/theme
- market bias
- urgency
- watchlist
- translated / summarized explanation
- optional original quote excerpts

### 3. `🚨 TRUMP MONITOR ERROR`
Something operational broke and should be surfaced instead of failing silently.

---

## Quick Start

```bash
git clone https://github.com/Kalpeny/trump-post-monitor-skill.git
cd trump-post-monitor-skill
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run one real-time pass

```bash
python3 realtime_loop.py --once
```

### Run wrapper manually

```bash
bash ./notify_wrapper.sh
```

### Replay historical posts for testing

```bash
FORCE_REPLAY_SINCE='2026-03-21T18:00:00.000Z' bash ./notify_wrapper.sh
```

### Start local dashboard/API

```bash
python3 chatbot_server.py
```

---

## Main Data Files

These are the key files still relevant to the active monitor flow:

- `data/trump_posts_all.json` — full Trump post archive used for extraction/replay
- `data/trump_posts_lite.json` — lighter derived view
- `data/rt_last_seen.txt` — last processed timestamp for real-time flow
- `data/rt_predictions.json` — recent real-time signal output
- `data/polymarket_live.json` — latest prediction market snapshot
- `data/trump_coin_history.json` — related market context data
- `data/trump_playbook.json` — playbook / scenario reference

---

## API / UI

`chatbot_server.py` provides a lightweight dashboard/API layer for local use.

Examples:

- `/api/status`
- `/api/dashboard`
- `/api/signals`
- `/api/recent-posts`
- `/api/data`

The public HTML dashboard lives in:

- `public/insights.html`

---

## Repo Cleanup Notes

The repo has already been pruned to remove:

- temporary test files
- wrapper runtime junk
- legacy Musk/X comparison artifacts
- dead download links pointing to removed files

The goal is to keep this repository centered on the **current Trump monitoring and alerting pipeline**, not a sprawling research dump.

---

## Development Notes

If you change the monitor flow, validate at least these paths:

```bash
python3 realtime_loop.py --once
bash ./notify_wrapper.sh
FORCE_REPLAY_SINCE='2026-03-21T18:00:00.000Z' bash ./notify_wrapper.sh
```

Recommended checks:

- no new posts → `NO_REPLY`
- real catalyst posts → readable alert
- operational failure → `🚨 TRUMP MONITOR ERROR`

---

## License

MIT
