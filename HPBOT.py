#Импорты

import telebot
from telebot import types
import psycopg2
#from telebot import apihelper



#данные для дб конекта
dbUserName = 'ipsyghxbqjmkvl'
dbPass = 'd4ff61101874c4d8f6b338374d33b7f9505a001d4476cdf6c55e22e9cfe5fbf0'
dbHost = 'ec2-54-228-246-214.eu-west-1.compute.amazonaws.com'
dbPort = '5432'
dbName = 'dci20oi1bfdb7p'

con = psycopg2.connect(user=dbUserName,
                     password=dbPass,
                     host=dbHost,
                     port=dbPort,
                     dbname=dbName,
                     )




#ТОКЕН ПРОКСИ
#apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot('883542941:AAEz9na1uwBvw8bZyCMT_yrBuKtIA-qJVCI')




#клава для кальян
def keyboard():
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('/Список')
    btn2 = types.KeyboardButton('/Добавить')
    btn3 = types.KeyboardButton('/Удалить')
    btn4 = types.KeyboardButton('/УдалитьСписок')


    markup.add(btn1,btn2,btn3,btn4)

    return markup

#клава для старт
def keyboard1():
    markup2 = types.ReplyKeyboardMarkup()

    btn5 = types.KeyboardButton('Бар')
    btn6 = types.KeyboardButton('Кальян')

    markup2.add(btn5, btn6)

    return markup2
#клава для бар
def keyboard2():
    markup3 = types.ReplyKeyboardMarkup()

    btn7 = types.KeyboardButton('/СписокБар')
    btn8 = types.KeyboardButton('/ДобавитьБар')
    btn9 = types.KeyboardButton('/УдалитьБар')
    btn10 = types.KeyboardButton('/УдалитьСписокБар')

    markup3.add(btn7, btn8, btn9, btn10)

    return markup3












#ЛОГИ команд
def log(message):
    print("<!------!>")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                              message.from_user.last_name,
                                                              str(message.from_user.id), message.text))


#Ответ на старт
@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.from_user.id, 'Привет, Бар или Кальян?', reply_markup=keyboard1())
    bot.register_next_step_handler(message, bar)
    log(message)

#выбор кальян или бар

def bar(message):
    if message.text == 'Кальян':
        bot.send_message(message.from_user.id, 'Ниже кнопки по кальянной ветке!',reply_markup=keyboard())
    elif message.text == 'Бар':
        bot.send_message(message.from_user.id, 'Ниже кнопки по барной ветке!', reply_markup=keyboard2())
        

    log(message)


# Блок бота на вывод списка задач
@bot.message_handler(commands=['Список'])
def list(message):

    log(message)


    # Подключение или создание БДы
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS zakuptabaka (id SERIAL PRIMARY KEY NOT NULL, firma TEXT)")


    # Выгрузка и формирование списка БДы
    new = []
    cur.execute("SELECT * FROM zakuptabaka ")
    rows = cur.fetchall()
    for i in rows:
        i = str("{}. {}".format(i[0], i[1]))
        new.append(i)

    # Форматирование списка для вывода
    sp = '\n'.join(new)
    # Дроп базы
    con.commit()
    cur.close()

    # проверка на пустую таблицу
    try:
        bot.send_message(message.chat.id,sp, None)
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, 'Таблица пуста', None)
        log(message)


# Блок бота на добавление задачи
@bot.message_handler(commands=['Добавить'])
def new_task(message):
    bot.send_message(message.chat.id, "Внесите данные:", None)
    log(message)




    # проучаем ответ пользователя
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def task_n(message):
        # Апаем БДу
        answer = message.text
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS zakuptabaka (id SERIAL PRIMARY KEY NOT NULL, firma TEXT)")
        cur.execute("INSERT INTO zakuptabaka(firma)"
                    " VALUES(%r)" %answer)
        con.commit()
        cur.close()
        bot.send_message(message.chat.id, "Позиция добавлена!",reply_markup=keyboard())











# Блок бота на удаление задачи
@bot.message_handler(commands=['Удалить'])
def del_task(message):
    bot.send_message(message.chat.id, "Напиши номер позиции, которую надо удалить", None)
    bot.register_next_step_handler(message, task_d)
    log(message)




    # получаем ответ пользователя

def task_d(message):
        # Апаем БДу
    num = message.text
    cur = con.cursor()
    cur.execute("DELETE FROM zakuptabaka WHERE id=%r" % num)
    con.commit()
    cur.close()
    bot.send_message(message.chat.id, "Позиция удалена", None)

@bot.message_handler(commands=['УдалитьСписок'])
def all_d(message):
    log(message)
    bot.send_message(message.chat.id,"Удаляем?", None)
    bot.register_next_step_handler(message, fdlt)




#полный дропа базы кальян
def fdlt(message):

    cur = con.cursor()
    cur.execute("DROP TABLE zakuptabaka")
    con.commit()
    cur.close()
    bot.send_message(message.chat.id, "Таблица очищена", None)




#вывод базы по бару
@bot.message_handler(commands=['СписокБар'])
def listbar(message):


    # Подключение или создание БДы


    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bar (id SERIAL PRIMARY KEY NOT NULL, zada4a TEXT)")


    # Выгрузка и формирование списка БДы
    new = []
    cur.execute("SELECT * FROM bar ")
    rows = cur.fetchall()
    for i in rows:
        i = str("{}. {}".format(i[0], i[1]))
        new.append(i)

    # Форматирование списка для вывода
    sp = '\n'.join(new)
    # Дроп базы
    con.commit()
    cur.close()

    #проверка на пустую базу
    try:
        bot.send_message(message.chat.id,sp, None)
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, 'Таблица пуста', None)
        log(message)



# Блок бота на добавление задачи бар
@bot.message_handler(commands=['ДобавитьБар'])
def new_taskbar(message):
    bot.send_message(message.chat.id, "Внесите данные:", None)
    log(message)

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def task_nbar(message):
        # Апаем БДу
        answer = message.text
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS bar (id SERIAL PRIMARY KEY NOT NULL, zada4a TEXT)")
        cur.execute("INSERT INTO bar(zada4a)"
                    " VALUES(%r)" % answer)
        con.commit()
        cur.close()
        bot.send_message(message.chat.id, "Позиция добавлена!", None)





# Блок бота на удаление задачи
@bot.message_handler(commands=['УдалитьБар'])
def del_taskbar(message):
    bot.send_message(message.chat.id, "Введите номер удаляемой позиции:", None)
    bot.register_next_step_handler(message, task_dbar)
    log(message)

# Дроп по введеному ид
def task_dbar(message):

    # Апаем БДу
    num = message.text
    cur = con.cursor()
    cur.execute("DELETE FROM bar WHERE id=%r" % num)
    con.commit()
    cur.close()
    bot.send_message(message.chat.id, "Позиция удалена", None)



# полный дроп базы бар
@bot.message_handler(commands=['УдалитьСписокБар'])
def all_dbar(message):
    bot.send_message(message.chat.id,"Удаляем?", None)
    bot.register_next_step_handler(message, fdltbar)






def fdltbar(message):

    cur = con.cursor()
    cur.execute("DROP TABLE bar")
    con.commit()
    cur.close()
    bot.send_message(message.chat.id, "Таблица очищена", None)



if __name__ == '__main__':
    bot.polling(none_stop=True)




