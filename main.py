import telebot
from telebot import types
import random
import os
import time
TOKEN = '5062502904:AAFo6tkSfCfYxtJ_N9VdXLUTTUwAHK-RwJ4'



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Играть')
    item2 = types.KeyboardButton('Правила игры')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Привет {0.first_name}!'.format(message.from_user), reply_markup= markup)


@bot.message_handler(content_types = ['text']) #функция принимающая текстовые сообщения боту
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Правила игры': #вывод сообщений бота, если текст сообщения равен данному значению
            bot.send_message(message.chat.id, 'Блэкджек также известен как 21. Суть игры проста: набрать 21 очко или больше, чем в руках у дилера, но ни в коем случае не больше 21. Если игрок собирает больше 21, он «сгорает». В случае ничьей игрок и дилер остаются при своих.')
            bot.send_message(message.chat.id, 'В блэкджеке цена карт не меняется в течение игры. Цель — набрать 21 очко, использовав при этом как можно меньше карт. Карты имеют такие ценовые значения:')
            bot.send_message(message.chat.id, 'Карты с числами: цена — число на карте.')
            bot.send_message(message.chat.id, 'Картинки: цена — 10 очков.')
            bot.send_message(message.chat.id, 'Туз — 1 или 11. Как правило, цена туза составляет 11 очков, но если при таком подсчете сумма очков выше 21, то цена карты становится 1.')
        elif message.text == 'Играть': #выбор игры
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Больше')
            item2 = types.KeyboardButton('Хватит')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Играть', reply_markup = markup) #смена кнопок для режима игры

            class BlackJack:
                def __init__(self):
                    self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'] * 4  #определяем колоду
                    self.score = 0  #счет игрока
                    self.bot_score = 0 #счет бота

                def print_card(self, current, score, bot_score):

                    bot.send_message(message.chat.id, f'Вам попалась карта {current}. У вас {score} очков.')
                    bot.send_message(message.chat.id, f'Крупье попалась карта {current}. У крупье {bot_score} очков')

                def random_card(self, score, bot_score):
                    current = self.deck.pop()
                    if type(current) is int:
                        score += current
                    elif current == 'Ace':
                        if score <= 10:
                            score += 11
                        else:
                            score += 1
                    else:
                        score += 10
                    self.print_card(current, score, bot_score)
                    return score

                @bot.message_handler(content_types=['text'])
                def choice(self):
                    score = self.random_card(self.score, False)
                    bot_score = self.random_card(self.bot_score, True)

                    bot.send_message(message.chat.id, 'Ещё или хватит?')

                    while True:
                        if message.chat.type == 'private':
                            if message.text == 'Больше':
                                score = self.random_card(score, False)
                                if bot_score < 19 and score <= 21:
                                    bot_score = self.random_card(bot_score, True)
                                if score > 21 or bot_score == 21:
                                    bot.send_message(message.chat.id, 'Извините, но вы проиграли')
                                    break
                                elif score == 21 and bot_score == 21:
                                    bot.send_message(message.chat.id, 'ничья')
                                elif score == 21 or bot_score > 21:
                                    bot.send_message(message.chat.id, 'Поздравляю, вы победили!')
                                    break
                            elif message.text == 'Хватит':
                                if score > bot_score and bot_score < 19:
                                    while bot_score < 19:
                                        bot_score = self.random_card(bot_score, True)
                                if score < bot_score <= 21:
                                    bot.send_message(message.chat.id,
                                                     f'Вы проиграли, у вас {score} очков, у крупье {bot_score} очков')
                                else:
                                    bot.send_message(message.chat.id,
                                                     f'Вы победили, у вас {score} очков, у крупье {bot_score} очков')

                                break


                @bot.message_handler(content_types=['text'])
                def start(self): #начало игры и вызов функции выбора
                    random.shuffle(self.deck)
                    bot.send_message(message.chat.id, 'Игра в BlackJack началась')
                    bot.send_message(message.chat.id,
                        'В блэкджеке десятки, валеты, дамы и короли стоят по 10 очков.\nТуз может стоить 1 или 11 очков')
                    self.choice()

                    bot.send_message(message.chat.id, 'До новых встреч!')

            game = BlackJack()
            game.start()




bot.polling(none_stop = True)