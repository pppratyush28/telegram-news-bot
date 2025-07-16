# Telegram News Bot 

A smart Telegram bot built using **Python**, **Flask**, and **Dialogflow** that provides the top 5 latest news based on user queries — powered by Google News and natural language processing.

## 🔧 Features

- Responds to both **small talk** and **news-related queries**.
- Fetches news by **topic**, **region**, and **language**.
- Uses **Dialogflow** to understand user intent.
- Telegram-compatible and hosted using **Flask webhooks**.
- Supports stickers and basic commands like `/start` and `/help`.

## 🧠 Powered By

- [Google Dialogflow](https://cloud.google.com/dialogflow)
- [Google News API (gnewsclient)](https://github.com/SDM-TIB/gnewsclient)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Flask](https://flask.palletsprojects.com/)

## 📁 Project Structure

```
telegram-news-bot/
│
├── NewsBot.py # Main Flask app and Bot logic
├── NewsBotUtils.py # for handling Dialogflow and for News fetching
├── .gitignore # Ignore sensitive files like client.json
├── requirements.txt # Python dependencies (optional | may contain )
└── README.md # You're reading it!
```

## 🚀 Getting Started

### 1. Clone the Repo

git clone https://github.com/pppratyush28/telegram-news-bot.git

cd telegram-news-bot

### 2. Create a Virtual Environment (Optional but recommended)

python3 -m venv myvenv

source myvenv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Add Your Credentials

Place your client.json (Dialogflow service account key) in the root folder.

Add it to .gitignore to prevent accidental commits.

### 5. Run the Bot

Update WEBHOOK_URL in NewsBot.py to match your ngrok/public URL and run:

python NewsBot.py

### Example Queries
"Give me news from India"

"Show sports news in English"

"Hello!" → (responds to small talk)

### To Do
 Add Docker support

 Add proper error fallback messages

 Deploy to a cloud platform (Render/Heroku/etc.)

### Author
Pratyush Pranjal

https://linkedin.com/in/pratyushpranjal | pppranjalpratyush@gmail.com