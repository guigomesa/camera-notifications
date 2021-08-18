from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async

class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.token = token

    def sendMessage(self, chatId, message):
        self.updater.bot.send_message(chat_id=chatId, text=message)

    def sendPhoto(self, chatId, imagePath):
        self.updater.bot.send_photo(chat_id=chatId, photo=open(imagePath, 'rb'))        

    def teste(self):
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler('bop', self.bop))
        self.updater.start_polling()
        self.updater.idle()            

    def bop(message, update, context):
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text="ola mundo")        

def teste():
    telegramBot = TelegramBot("TELEGRAM-TOKEN")
    telegramBot.sendMessage(1476103496, "ola mundo")
    telegramBot.sendPhoto(1476103496, "sendimage.jpg")