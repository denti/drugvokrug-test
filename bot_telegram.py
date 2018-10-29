# #! /usr/bin/env python2.7
# # -*- coding: utf-8 -*-
import io
import hashlib
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


USERS_DICT, USERS_SORTED = {}, []


######################## Main handlers ########################
def start(bot, update):
    update.message.reply_text(
        'Привет, я тестовый бот. Используйте одну из команд для управления списком пользователей: ["/save", "/list", "/del" ]')


def echo(bot, update):
    update.message.reply_text(
        'Для общения со мной используйте одну из команд для управления списком пользователей: ["/save", "/list", "/del" ]')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('При попытке выполнить комадну "%s" произошла ошибка "%s"', update, error)


######################## Action handlers ########################
def save(bot, update, args):
    global USERS_DICT, USERS_SORTED
    print('SAVE')
    user_data = ''
    for arg in args:
        user_data += " %s" % arg

    if user_data:
        key = hashlib.md5(user_data.encode('utf-8')).hexdigest()
        USERS_DICT[key] = user_data

        if not key in USERS_SORTED:
            USERS_SORTED.append(key)
            # sort users
            USERS_SORTED = array_sort(USERS_SORTED)

        update.message.reply_text('Пользователь успешно сохранен')
    else:
        update.message.reply_text('Для добавления пользователя введите команды /save user_data1, user_data2...')


def list(bot, update, args):
    global USERS_DICT, USERS_SORTED
    if len(USERS_SORTED):
        update.message.reply_text('Отсортированный список пользователей:')
        response = '\n'.join(['%s: %s' % (key, USERS_DICT[key]) for key in USERS_SORTED])
    else:
        response = 'На сервере нет пользователей'
    update.message.reply_text(response)


def delete(bot, update, args):
    user_id = args[0]
    global USERS_DICT, USERS_SORTED
    if user_id in USERS_SORTED:
        del USERS_DICT[user_id]
        USERS_SORTED.remove(user_id)
        update.message.reply_text('Пользователь успешно удален')
    else:
        update.message.reply_text('Пользователь не найден')


######################## Additional Functions ########################
def array_sort(arr):
    """
    Merge sort

    :param arr:
    :return sorted_arr:
    """
    if len(arr) < 2:
        return arr

    middle_index = len(arr) // 2
    arr1 = array_sort(arr[0:middle_index])
    arr2 = array_sort(arr[middle_index:])
    new_arr = []
    while len(arr1) and len(arr2):
        new_arr = [(arr1.pop() if (arr1[-1] > arr2[-1]) else arr2.pop())] + new_arr
    return arr1 + arr2 + new_arr


######################## Main ########################
def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ['API_TELEGRAM_TOKEN'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

    # Base handlers
    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(echo_handler)

    # Action handlers
    save_handler = CommandHandler('save', save, pass_args=True)
    dp.add_handler(save_handler)
    list_handler = CommandHandler('list', list, pass_args=True)
    dp.add_handler(list_handler)
    delete_handler = CommandHandler('del', delete, pass_args=True)
    dp.add_handler(delete_handler)

    # log all errors
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
