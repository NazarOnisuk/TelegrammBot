import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from random import randint
from bs4 import BeautifulSoup
import requests

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = 'TOKEN'


def parseFilmByGenre(genres, rating=0):
    title = []
    if rating:
        url = f'https://www.ivi.ru/movies/{genres}?ivi_rating_10_gte={rating}'
    else:
        url = f'https://www.ivi.ru/movies/{genres}'

    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        titles = soup.findAll('div', class_='nbl-slimPosterBlock__title')
        titles = list(map(lambda x: x.text.strip(), titles))
        spisok_tops = titles[:10]
        spisok_tops1 = []
        for i in spisok_tops:
            stroka_tops = i.encode("utf-8")
            spisok_tops1.append(stroka_tops.decode("utf-8"))
        return spisok_tops1


def parseFilmFind(name):
    if ' ' in name:
        names = name.split(' ')
        url = f'https://www.ivi.ru/movies/{"_".join(names)}?ivi_search={"%20".join(names)}'
    else:
        url = f'https://www.ivi.ru/movies/{name}?ivi_search={name}'
    return url


def start(update, context):
    reply_keyboard = [['Помощь'],
                      ['Показать погоду'],
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
    with open("help.txt", encoding="utf-8") as file:
        update.message.reply_text(file.read())


def sreach_weather(update, context):
    update.message.reply_text("В разработке")


def search_film(update, context):
    update.message.reply_text("Введите 'Найди (название фильма)'")


def tops(update, context):
    reply_keyboard = [['Артхаус'],
                      ['Биография'],
                      ['Боевики'],
                      ['Вестерн'],
                      ['Военные'],
                      ['Детективы'],
                      ['Для детей'],
                      ['Документальные'],
                      ['Драмы'],
                      ['Зарубежные'],
                      ['Исторические'],
                      ['Катастрофы'],
                      ['Комедии'],
                      ['Криминал'],
                      ['Мелодрамы'],
                      ['Мистические'],
                      ['По комиксам'],
                      ['Приключения'],
                      ['Русские'],
                      ['Семейные'],
                      ['Советские'],
                      ['Спорт'],
                      ['Триллеры'],
                      ['Ужасы'],
                      ['Фантастика'],
                      ['Фентези'],
                      ['Вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Выберите жанр",
        reply_markup=markup)


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

    if "Показать погоду":
        pass

    if "Найти фильм" == text:
        search_film(update, context)
    if "Найди" in text or 'найди' in text or 'yfqlb' in text or 'Yfqlb' in text:
        poisk = update.message.text
        update.message.reply_text(f"Ищу фильм {poisk[6:]}")
        update.message.reply_text(f'Вот что я нашел: {parseFilmFind(poisk[6:])}')

    if "Топы фильмов" == text:
        tops(update, context)
    if "Артхаус" == text:
        count = 1
        for i in parseFilmByGenre('arthouse', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Биография" == text:
        # update.message.reply_text(parseFilmByGenre('biography', rating=0))
        count = 1
        for i in parseFilmByGenre('biography', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Боевики" == text:
        # update.message.reply_text(parseFilmByGenre('boeviki', rating=0))
        count = 1
        for i in parseFilmByGenre('boeviki', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Вестерн" == text:
        # update.message.reply_text(parseFilmByGenre('western', rating=0))
        count = 1
        for i in parseFilmByGenre('western', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Военные" == text:
        # update.message.reply_text(parseFilmByGenre('voennye', rating=0))
        count = 1
        for i in parseFilmByGenre('voennye', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Детективы" == text:
        # update.message.reply_text(parseFilmByGenre('detective', rating=0))
        count = 1
        for i in parseFilmByGenre('detective', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Для детей" == text:
        # update.message.reply_text(parseFilmByGenre('detskiy', rating=0))
        count = 1
        for i in parseFilmByGenre('detskiy', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Документальные" == text:
        # update.message.reply_text(parseFilmByGenre('documentary', rating=0))
        count = 1
        for i in parseFilmByGenre('documentary', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Драмы" == text:
        # update.message.reply_text(parseFilmByGenre('drama', rating=0))
        count = 1
        for i in parseFilmByGenre('drama', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Зарубежные" == text:
        # update.message.reply_text(parseFilmByGenre('foreign', rating=0))
        count = 1
        for i in parseFilmByGenre('foreign', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Исторические" == text:
        # update.message.reply_text(parseFilmByGenre('istoricheskie', rating=0))
        count = 1
        for i in parseFilmByGenre('istoricheskie', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Катастрофы" == text:
        # update.message.reply_text(parseFilmByGenre('disaster', rating=0))
        count = 1
        for i in parseFilmByGenre('disaster', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Комедии" == text:
        # update.message.reply_text(parseFilmByGenre('comedy', rating=0))
        count = 1
        for i in parseFilmByGenre('comedy', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Криминал" == text:
        # update.message.reply_text(parseFilmByGenre('crime', rating=0))
        count = 1
        for i in parseFilmByGenre('crime', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Мелодрамы" == text:
        # update.message.reply_text(parseFilmByGenre('melodramy', rating=0))
        count = 1
        for i in parseFilmByGenre('melodramy', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Мистические" == text:
        # update.message.reply_text(parseFilmByGenre('misticheskie', rating=0))
        count = 1
        for i in parseFilmByGenre('misticheskie', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "По комиксам" == text:
        # update.message.reply_text(parseFilmByGenre('comics', rating=0))
        count = 1
        for i in parseFilmByGenre('comics', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Приключения" == text:
        # update.message.reply_text(parseFilmByGenre('adventures', rating=0))
        count = 1
        for i in parseFilmByGenre('adventures', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Русские" == text:
        # update.message.reply_text(parseFilmByGenre('rossijskie', rating=0))
        count = 1
        for i in parseFilmByGenre('rossijskie', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Семейные" == text:
        # update.message.reply_text(parseFilmByGenre('dlya_vsej_semi', rating=0))
        count = 1
        for i in parseFilmByGenre('dlya_vsej_semi', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Советские" == text:
        # update.message.reply_text(parseFilmByGenre('sovetskoe_kino', rating=0))
        count = 1
        for i in parseFilmByGenre('sovetskoe_kino', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Спорт" == text:
        # update.message.reply_text(parseFilmByGenre('sport', rating=0))
        count = 1
        for i in parseFilmByGenre('sport', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Триллеры" == text:
        # update.message.reply_text(parseFilmByGenre('thriller', rating=0))
        count = 1
        for i in parseFilmByGenre('thriller', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Ужасы" == text:
        # update.message.reply_text(parseFilmByGenre('horror', rating=0))
        count = 1
        for i in parseFilmByGenre('horror', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Фантастика" == text:
        # update.message.reply_text(parseFilmByGenre('fantastika', rating=0))
        count = 1
        for i in parseFilmByGenre('fantastika', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1
    if "Фентези" == text:
        # update.message.reply_text(parseFilmByGenre('fentezi', rating=0))
        count = 1
        for i in parseFilmByGenre('fentezi', rating=0):
            update.message.reply_text(f'{count}) {i}')
            count += 1

    if "Бросить кубик" == text:
        dice(update, context)
    if "Кинуть один шестигранный кубик" == text:
        # dice(update, context)
        update.message.reply_text(f"Шестигранный кубик показывает: {str(randint(1, 6))}")
        reply_keyboard = [['Кинуть один шестигранный кубик опять'],
                          ['Кинуть 2 шестигранных кубика одновременно'],
                          ['Кинуть 20-гранный кубик'],
                          ['Вернуться назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Бросим кубик",
            reply_markup=markup)
    if "Кинуть 2 шестигранных кубика одновременно" == text:
        update.message.reply_text(f"Шестигранные кубики показывают: {str(randint(1, 6))}, {str(randint(1, 6))}")
        # dice(update, context)
        reply_keyboard = [['Кинуть один шестигранный кубик'],
                          ['Снова кинуть 2 шестигранных кубика одновременно'],
                          ['Кинуть 20-гранный кубик'],
                          ['Вернуться назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Бросим кубик",
            reply_markup=markup)
    if "Кинуть 20-гранный кубик" == text:
        update.message.reply_text(f"Двадцатигранный кубик показывает: {str(randint(1, 20))}")
        # dice(update, context)
        reply_keyboard = [['Кинуть один шестигранный кубик'],
                          ['Кинуть 2 шестигранных кубика одновременно'],
                          ['Опять кинуть 20-гранный кубик'],
                          ['Вернуться назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Бросим кубик",
            reply_markup=markup)

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
