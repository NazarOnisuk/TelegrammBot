import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from random import randint

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5216319050:AAFusnCu9crditwtu2JMjbzqJfqwPEhspSI'


def echo(update, context):
    update.message.reply_text(update.message.text)


def start(update, context):
    reply_keyboard = [['Помощь'],
                      ['Найти фильм'],
                      ['Топы фильмов'],
                      ['Бросить кубик'],
                      ['Поставить таймер']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    privet = [f'Здравствуйте, {update.message.chat.first_name}',
              f'Доброго времени суток, {update.message.chat.first_name}',
              f'Hi, {update.message.chat.first_name}',
              f'Привет, {update.message.chat.first_name}',
              f'Рад Вас видеть, {update.message.chat.first_name}',
              f'Салют, {update.message.chat.first_name}',
              f'Мое почтение, {update.message.chat.first_name}',
              f'Здравствуй, {update.message.chat.first_name}',
              f'Здорово, {update.message.chat.first_name}']
    update.message.reply_text(
        f'{privet[randint(0, 8)]}, чем я могу помочь?',
        reply_markup=markup)


def help(update, context):
    fp = open("help", encoding="utf-8")
    sp = fp.read()
    update.message.reply_text(
        f"{sp}")
    fp.close()


def search_film(update, context):
    update.message.reply_text("Введите 'Найти: (название фильма)'")


def dice(update, context):
    reply_keyboard = [['Кинуть один шестигранный кубик'],
                      ['Кинуть 2 шестигранных кубика одновременно'],
                      ['Кинуть 20-гранный кубик'],
                      ['Вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Бросим кубик",
        reply_markup=markup)


def timer(update, context):
    reply_keyboard = [['30 секунд'],
                      ['1 минута'],
                      ['5 минут'],
                      ['Вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Поставим таймер",
        reply_markup=markup)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update, context, due=0):
    chat_id = update.message.chat_id
    try:
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='КУКУ!')


def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    update.message.reply_text(text)


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def text_handler_f(update, context):
    global value
    text = update.message.text

    if "Помощь" == text:
        help(update, context)

    if "Найти фильм" == text:
        search_film(update, context)
    if "Найти:" in text:
        poisk = update.message.text
        update.message.reply_text(f"Ищу фильм {poisk[7:]}")

    if "Топы фильмов" == text:
        pass

    if "Бросить кубик" == text:
        dice(update, context)
    if "Кинуть один шестигранный кубик" == text:
        update.message.reply_text(f"Шестигранный кубик показывает: {str(randint(1, 6))}")
        dice(update, context)
    if "Кинуть 2 шестигранных кубика одновременно" == text:
        update.message.reply_text(f"Шестигранные кубики показывают: {str(randint(1, 6))}, {str(randint(1, 6))}")
        dice(update, context)
    if "Кинуть 20-гранный кубик" == text:
        update.message.reply_text(f"Двадцатигранный кубик показывает: {str(randint(1, 20))}")
        dice(update, context)

    if "Поставить таймер" == text:
        timer(update, context)
    if "30 секунд" == text:
        reply_keyboard = [['Отменить таймер'],
                          ['30 секунд'],
                          ['1 минута'],
                          ['5 минут'],
                          ['Вернуться назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Поставим таймер",
            reply_markup=markup)
        set_timer(update, context, 30)
    if "1 минута" == text:
        reply_keyboard = [['Отменить таймер'],
                          ['30 секунд'],
                          ['1 минута'],
                          ['5 минут'],
                          ['Вернуться назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Поставим таймер",
            reply_markup=markup)
        set_timer(update, context, 60)
    if "5 минут" == text:
        reply_keyboard = [['Отменить таймер'],
                          ['30 секунд'],
                          ['1 минута'],
                          ['5 минут'],
                          ['Вернуться назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Поставим таймер",
            reply_markup=markup)
        set_timer(update, context, 300)
    if "Отменить таймер" == text:
        unset(update, context)
        timer(update, context)

    if "Вернуться назад" == text:
        start(update, context)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text & ~Filters.command, text_handler_f)

    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
