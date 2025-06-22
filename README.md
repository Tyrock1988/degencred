# 🤖 DegenRep Telegram Bot

DegenRep is a Telegram bot that provides crypto loan reputation tracking, access fees, XP leveling, and more, integrated with CWallet transactions.

---

## 🛠 Features

- ✅ Auto-verifies access fees via CWallet bot messages
- 💸 Reputation-based loan levels with interest and repayment terms
- 📊 XP + leaderboard system for community engagement
- 🧾 Admin dashboard with verification controls
- 📡 Health check endpoint via Flask

---

## 🚀 Deploy on Render

### 1. 📦 Setup

Push your code to GitHub and connect your repo to [Render](https://render.com).

### 2. 📁 Required Environment Variables

| Variable | Description |
|---------|-------------|
| `BOT_TOKEN` | Your Telegram Bot token |
| `DATABASE_URL` | PostgreSQL URL (starts with `postgres://`) |

If using SQLite locally, leave `DATABASE_URL` blank.

### 3. 🧪 Health Check

Render will ping the `/health` route to check if your bot is alive.

---

## 🧱 Tech Stack

- `python-telegram-bot`
- `Flask` for web endpoint
- `psycopg2` or `sqlite3` for DB
- `gunicorn` for production server

---

## 📜 License

MIT License
