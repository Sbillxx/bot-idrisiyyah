import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application

TOKEN = os.getenv("BOT_TOKEN")
application = Application.builder().token(TOKEN).build()

def handler(request):
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.process_update(update)
        return "ok"
    return "Hello from webhook!"

# Vercel Python function entrypoint
app = Flask(__name__)

@app.route('/api/webhook', methods=['POST', 'GET'])
def webhook():
    return handler(request)
