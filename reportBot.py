import requests

from config import bot


def report(text):
    for id in bot.get("agents"):
        sendMessage(id, text)


def sendMessage(id, text):
    try:
        requests.get("https://api.telegram.org/bot438887870:AAHWo5ZG_nxtuBbLgZLplEffLRhmubi-INE/sendMessage", params={"chat_id": id, "text": text})
    except requests.HTTPError:
        pass