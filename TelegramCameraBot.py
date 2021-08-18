from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from CamerasData import CamerasData, CameraData
import TelegramNewCameraConversation

def onCancel(update: Update, context: CallbackContext):
    if (update.callback_query):
        update.callback_query.answer()

    return ConversationHandler.END

def start(update: Update, context: CallbackContext):

    keyboard = [
        [InlineKeyboardButton("Adicionar Camera", callback_data='newcamera')],
        [InlineKeyboardButton(
            "Nova Camera", callback_data='/addcamera')]
    ]
    replyMarkup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text="Bem-vindo",
        reply_markup=replyMarkup
    )


def teste(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Oloco!!",
        reply_markup=ReplyKeyboardRemove()
    )


def addHanlders(updater) -> None:
    newCameraConversation = TelegramNewCameraConversation.createConversation(onCancel)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(newCameraConversation)
    dispatcher.add_handler(CommandHandler("start", start))
    # updater.dispatcher.add_handler(CommandHandler("mycameras", mycameras))
    # updater.dispatcher.add_handler(CommandHandler("addcamera", addcamera))
    # updater.dispatcher.add_handler(CallbackQueryHandler(buttonCallback))
    # updater.dispatcher.add_error_handler(onError)


def createTelegramUpdater():
    updater = Updater(telegramToken)
    addHanlders(updater)
    return updater


def main():
    global telegramToken, camerasData
    telegramToken = 'TELEGRAM-TOKEN'
    camerasData = CamerasData.load("cameras.data")
    updater = createTelegramUpdater()
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
