import telegram
from click import echo
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import configparser
import logging

from ChatGPT_HKBU import HKBU_ChatGPT

import redis
global redis1

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: "+str(update))
    logging.info("context: "+str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context = True)
    dispatcher = updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']),
                        password = (config['REDIS']['PASSWORD']),
                        port = (config['REDIS']['REDISPORT']))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    print("Bot is running")
    #echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)
    global chatgpt
    chatgpt = HKBU_ChatGPT(config_path = './config.ini')
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_text = update.message.text.upper()
    logging.info("Update: "+str(update)+"\nContext: "+str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

def help_command(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    update.message.reply_text('Helping you helping you.')

def add(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for '+redis1.get(msg).decode('utf-8') + ' times.')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <message>')



if __name__ == '__main__':
    main()