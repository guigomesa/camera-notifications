from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)

CAMERA_IP, CONFIRMATION, ADD_CAMERA = range(3)


def newCamera(update: Update, context: CallbackContext) -> int:
    message = update.message

    if (update.callback_query):
        message = update.callback_query.message
        update.callback_query.answer()

    message.reply_text(
        'Para adicionar a camera, informe o nome para identificar ela',
        reply_markup=ReplyKeyboardRemove()
    )

    return CAMERA_IP


def cameraIp(update: Update, context: CallbackContext) -> int:  
    context.user_data['new-camera-name'] = update.message.text

    update.message.reply_text(
        'Informe o IP da camera',
        reply_markup=ReplyKeyboardRemove(),
    )

    return CONFIRMATION


def confirmation(update: Update, context: CallbackContext) -> int:
    context.user_data['new-camera-ip'] = update.message.text

    keyboard = [
        [InlineKeyboardButton("Sim", callback_data='yes')],
        [InlineKeyboardButton("Nao", callback_data='no')]
    ]

    update.message.reply_text(
        'Deseja adicionar a camera {0} com o ip {1}?'.format(
            context.user_data['new-camera-name'], context.user_data['new-camera-ip']),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return ADD_CAMERA


def addCamera(update: Update, context: CallbackContext) -> int:
    
    query = update.callback_query;
    query.answer()

    query.message.reply_text(
        'Adicionar camera {0} ip {1}'.format(
           context.user_data['new-camera-name'], context.user_data['new-camera-ip']),
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END



def createConversation(onCancel):
    convHandler = ConversationHandler(
        entry_points=[CommandHandler('newcamera', newCamera), CallbackQueryHandler(
            newCamera, pattern='newcamera')],
        states={
            CAMERA_IP: [MessageHandler(Filters.text & ~Filters.command, cameraIp)],
            CONFIRMATION: [MessageHandler(Filters.text & ~Filters.command, confirmation)],
            ADD_CAMERA: [CallbackQueryHandler(addCamera, pattern='yes'), CallbackQueryHandler(onCancel, pattern='no')],
        },
        fallbacks=[CommandHandler('cancel', onCancel)],
    )

    return convHandler
