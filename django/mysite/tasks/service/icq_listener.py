import os
from bot.bot import Bot
from bot.handler import MessageHandler

TOKEN = os.getenv("ICQ_TOKEN")
bot = Bot(token=TOKEN)

# bot.send_text(chat_id=chat_id, text="Да, вы справились. It's very good")


def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat, text=event.text)
    print(event)


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()

