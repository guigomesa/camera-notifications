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
import abc
import TelegramNewCameraConversation
'''
class TelegramListCamerasButton:
    def __init__(self) -> None:
        pass

class TelegramCommandHandler():
    def replyMessage(self, update, message, replyMarkup = None):
        telegramMessage = update.message or update.callback_query.message
        telegramMessage.reply_text(message, reply_markup=replyMarkup)


class TelegramStartHandler(TelegramCommandHandler):
    def execute(self, update, context) -> None:
        keyboard = [
                    [InlineKeyboardButton("Listar Cameras", callback_data='/mycameras')],
                    [InlineKeyboardButton("Nova Camera", callback_data='/addcamera')]
                ]
        replyMarkup = InlineKeyboardMarkup(keyboard)
        self.replyMessage(update, 'Bem vindo ao central de monitoramento.', replyMarkup)

class TelegramMyCamerasHandler(TelegramCommandHandler):
    def execute(self, update, context, camerasData: CamerasData) -> None:
        keyboard = []
        for cameraData in camerasData.data:
            keyboard.append(cameraData.name, callback_data=f'@{cameraData.name}')

        if (not keyboard):
            self.replyMessage(update, 'Não encontrei nenhuma camera')
            return

        message = 'Selecione a camera.'
        replyMarkup = InlineKeyboardMarkup(keyboard)
        self.replyMessage(update, 'Selecione a camera.', replyMarkup)
        

class TelegramAddCameraHandler(TelegramCommandHandler):
    def execute(self, update, context) -> None:
        self.replyMessage(update, 'Digite o nome da camera.')

class TelegramCameraBot():
    def __init__(self, telegramToken) -> None:
        self.telegramToken = telegramToken
        self.camerasData = CamerasData.load("cameras.data")
        self.updater = Updater(self.telegramToken)
        self.addHanlders()

    def addHanlders(self) -> None:
        self.updater.dispatcher.add_handler(CommandHandler("start", self.start))
        self.updater.dispatcher.add_handler(CommandHandler("mycameras", self.mycameras))
        self.updater.dispatcher.add_handler(CommandHandler("addcamera", self.addcamera))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.buttonCallback))
        # self.updater.dispatcher.add_error_handler(self.onError)

    def start(self, update, context) -> None:
        self.executeCommand(update, context, "/start")

    def mycameras(self, update, context) -> None:
        self.executeCommand(update, context, "/mycameras")
    
    def addcamera(self, update, context) -> None:
        self.executeCommand(update, context, "/addcamera")

    def executeCommand(self, update, context, command) -> None:
        if (command == '/start'):
            TelegramStartHandler().execute(update, context)
        elif (command == '/mycameras'):
            TelegramMyCamerasHandler().execute(update, context, self.camerasData)
        elif (command == '/addcamera'):
            TelegramAddCameraHandler().execute(update, context, self.camerasData)

    def startPooling(self) -> None:
        self.updater.start_polling()
        self.updater.idle()
    
    def buttonCallback(self, update, context):
        update.callback_query.answer()
        data = update.callback_query.data
        if (data.startswith('/')):
            self.executeCommand(update, context, data)
        
        
    def onError(self, update, context):
        chat_id = update.message.chat_id
        update.message.send_message(chat_id, "I'm sorry, I can't do that.")
'''

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
    telegramToken = '1828798794:AAFodbWLQ1gqdatPe5DeamOOzD0bo4JdxFc'
    camerasData = CamerasData.load("cameras.data")
    updater = createTelegramUpdater()
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
