# 🎾 SweetSpot Alerts

> Real-time price drop radar and automated affiliate deal bot for high-performance Pickleball, Padel, and court recovery gear.

## 🚀 About the Project
**SweetSpot Alerts** is an automated monitoring system designed to track historical price drops, bulk stock savings, and gear discounts across the US market. The system filters relevant signals and publishes curated deals tailored for serious court players (DupR 4.5+).

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **APIs & Data Sources:** Reddit PRAW / JSON Feeds, Keepa / CamelCamelCamel RSS
* **AI Enrichment:** Google Gemini API (for native English copywriting and gear analysis)
* **Delivery/Distribution:** Discord Webhooks / X (Twitter) API
* **Hosting:** GitHub Pages / Static Frontend

## ⚙️ Core Features
- **Smart Filtering:** Ignores generic marketing noise and flags only All-Time Lows (ATL) or verified coupon stack deals.
- **Insider Copywriting:** Automatically converts raw technical specs (e.g., raw carbon grit, swing weight, core thickness) into engaging 3-line alerts.
- **Affiliate Link Rewriter:** Dynamically cleans and wraps product links with Amazon US associate tags (`?tag=...`).

## 📁 Project Structure
```text
sweetspot-alerts/
├── index.html          # Public landing page & deal showcase
├── bot.py              # Main Python pipeline & price radar script
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
