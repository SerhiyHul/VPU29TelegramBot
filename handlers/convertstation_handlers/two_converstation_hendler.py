from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters,CallbackQueryHandler

START, READY, HOPPER, DOOR, FRIEND, EARTH, GES_STATION, HOME = range(8)
from handlers.base_handler import BaseHandler


class TwoConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('game', cls.game)],
            states={
                START: [MessageHandler(filters.Regex('^(Так|Ні)$'), cls.start)],
                READY: [MessageHandler(filters.Regex('^(Кукурудза|Сонце|Годинник)$'), cls.ready)],
                HOPPER: [MessageHandler(filters.Regex('^(Так|Ні|)$'), cls.hopper)],
                DOOR: [MessageHandler(filters.Regex('^(Червона|Зелена|Жовта)$'), cls.door)],
                FRIEND: [MessageHandler(filters.Regex('^(Забрати скарби|Спасти колегу)$'), cls.friend)],
                EARTH: [MessageHandler(filters.Regex('^(Забрати скарби|Спасти колегу)$'), cls.friend)],
                GES_STATION: [MessageHandler(filters.Regex('^(Заїхати на заправку та подякувати заправщику|Поїзати додому)$'), cls.ges_station)],
                HOME: [MessageHandler(filters.Regex('^(УРА)$'), cls.home)]

            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def game(update: Update, context):
        keyboard = [
            [KeyboardButton('Так'), KeyboardButton('Ні')],
        ]
        reply_text = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Привіт, {update.effective_user.first_name}! Чудово бачити тебе тут!\n\n"
            "Ти готовий вирушити у захопливу пригоду в таємничому місті, де кожний куток приховує свою таємницю та небезпеку?\n\n"
            "Сюжет:\n"
            "Ти - відважний дослідник, який отримав лист від давнього колеги, що зник безвісти в таємничому місті, відомому своїми загадками та таємницями. Лист містить заклик допомогти відновити загублену історію цього місця, а також розкрити його найбільші таємниці.\n\n"
            "Твоя мета - дослідити кожен куточок міста, розв'язати загадки, зустріти місцевих мешканців і дізнатися, що сталося з колегою. Але будь обережний - місто приховує багато небезпек, і не всі з них видно на перший погляд.\n\n"
            "Ти готовий до цього захопливого виклику?",
            reply_markup=reply_text
        )

        return START

    @staticmethod
    async def start(update: Update, context):
        answer = update.message.text
        context.user_data['1'] = answer
        if answer.lower() == 'ні':
            await update.message.reply_text(
                "Шкода, що ти вирішив не вирушати у цю захоплюючу пригоду. Надіюся, побачимося ще!",  reply_markup=ReplyKeyboardRemove())


            return ConversationHandler.END
        else:
            keyboard = [
                [KeyboardButton('Кукурудза'), KeyboardButton('Сонце'), KeyboardButton('Годинник')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text("""Коли ви вирушили до таємничого міста і потрапили на пусті вулиці, ваші сенсори почали бути насторожені. Прийшовши до АЗС, ви помітили заправщика, що стоїть там, здавалося б, непорушно. Спробувавши почати розпитувати його, ви розчарувалися, коли він не захотів вам відповідати.
            Тимчасом, ваш погляд зачепив табличку біля каси, де була надписана загадка:
            "Відомо, що я вимірюю час, але я не годинник. Я роблю різні звуки, але я не музика. Я можу бути великим або маленьким, але я не ріст. Що я?"
            """, reply_markup=reply_text)

            return READY

    @staticmethod
    async def exit(update: Update, context):
        await update.message.reply_text('Гру закінчено')

        return ConversationHandler.END

    @staticmethod
    async def ready(update: Update, context):
        quote = update.message.text
        context.user_data['2'] = quote

        if quote == 'Кукурудза':
            keyboard = [
                [KeyboardButton('Так'), KeyboardButton('Ні')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text("""Ваша відповідь була правильною. Заправщик розпочав розповідь про місто та вашого колегу. Він зізнався, що ваш колега заїжджав до нього 
            перед виїздом на пошуки скарбів та відправився в секретний бункер. Однак він попередив, що там дуже небезпечно. Чи ризикнете ви поїхати туди?
            
                        """, reply_markup=reply_text)
            return HOPPER
        else:
            await update.message.reply_text("Відповідь була неправильна, вас вбив заправщик.")
            return ConversationHandler.END

    async def hopper(update: Update, context):
        quote = update.message.text
        context.user_data['3'] = quote

        if quote == 'Так':
            keyboard = [
                [KeyboardButton('Червона'), KeyboardButton('Зелена'), KeyboardButton('Жовта')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text("""Ви відправились в бункер міста, для входу в бункер потрібно натиснути
            одну з трьох кнопок
            """,

                                     reply_markup=reply_text)
            return DOOR
        else:
            await update.message.reply_text("""Ви повернулись додому, а ваш друг назавджи пропаде, ваша кар'єра 
            дослідника закінчилась.
                        """)
            return ConversationHandler.END

    async def door(update: Update, context):
        quote = update.message.text
        context.user_data['4'] = quote

        if quote == 'Жовта':
            keyboard = [
                [KeyboardButton('Покинути бункер'), KeyboardButton('Піти на досліди цих звуків'), KeyboardButton('Зачекаю на мить, щоб зрозуміти, чи це потенційна небезпека.')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text("""Ви продовжили свій шлях у глиб бункера і виявили годинник вашого колеги. 
            Під час осмотру ви почали чути дивні звуки, що роблять вас нервовими. Що буде вашим наступним кроком? Можливо, 
            вам варто розглянути дослідження походження цих звуків та виявлення джерела? Чи краще буде швидко покинути 
            це місце і повернутися за допомогою?
                        """,

                                            reply_markup=reply_text)
            return FRIEND
        else:
            await update.message.reply_text("Ви обрали не правильну кнопку! Ви програли.")
            return ConversationHandler.END

    async def friend(update: Update, context):
        quote = update.message.text
        context.user_data['5'] = quote

        if quote == 'Піти на досліди цих звуків' or quote == 'Зачекаю на мить, щоб зрозуміти, чи це потенційна небезпека.':
            keyboard = [
                [KeyboardButton('Спасти колегу'), KeyboardButton('Забрати золото та залишити друга')]
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text("""
Після того як дивні звуки припинилися, я вирішив рушити далі у глиб бункера. Пройшовши кілька метрів, мій погляд зачепив дверцята в стіні. 
Вирішивши ризикувати, я відчинив їх. Переді мною розкрилася комірчина, а в ній — справжні скарби! Скляні банки з непідрахунковими скарбами і 
коштовностями стояли поруч з картами та старовинними книгами. І ось, у кутку, я побачив його — свого колегу! Він був тут, вкрай зосереджений 
на якійсь дрібниці, 
яка виявилася ключем до цієї величезної скарбниці. Насправді, це була прекрасно оформлена сцена, наче з фільму про пригоди. 
Що ви обирете спасти колегу чи забрати золото?""",

                                            reply_markup=reply_text)
            return EARTH
        else:
            await update.message.reply_text("Ви обрали не правильну кнопку! Ви програли.")
            return ConversationHandler.END

    async def earth(update: Update, context):
        quote = update.message.text
        context.user_data['6'] = quote

        if quote == 'Спасти колегу':
            keyboard = [
                [KeyboardButton('Втекти з бункера на вулицю.')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text("""Усвідомивши, що час дорого коштує, я швидко допоміг своєму колезі зібрати 
            скарби та знайдений ключ. Разом ми пройшли назад, де двері комірчини зачинилися за нами з глухим лязгом, нагадуючи 
            про те, що бункер чекав своєї долі. Поспішно повертаючись, ми намагалися втекти, перебігаючи коридори, 
            які мимоволі нагадували про те, як нам пощастило. Нарешті, після декількох хвилин ми вийшли на світло, 
            дихаючи вільним повітрям вільності, і вчасно для нас, бункер почувся лютим громом і затрусився в руїни. """,

                                            reply_markup=reply_text)
            return GES_STATION
        else:
            await update.message.reply_text("Ви програли")
            return ConversationHandler.END

    async def ges_station(update: Update, context):
        quote = update.message.text
        context.user_data['7'] = quote

        if quote == 'Втекти з бункера на вулицю.':
            keyboard = [
                [KeyboardButton('Поїхати додому'), KeyboardButton('Подякувати заправщику')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text("""Ви втекли на вулицю та їдете додому з колегою. Поруч з вами пролягає заправка, 
            і ви маєте можливість заїхати туди та подякувати заправщику за його допомогу. Але можливо, ви втомилися
             і хочете просто повернутися додому і відпочити. Що ви оберете?""",

                                            reply_markup=reply_text)
            return HOME
        else:
            await update.message.reply_text("Ви програли")
            return ConversationHandler.END

    async def home(update: Update, context):
        quote = update.message.text
        context.user_data['8'] = quote

        if quote == 'Подякувати заправщику':
            await update.message.reply_text("""
Отримавши вашу подяку, заправщик раптово змінив свою поведінку, виявивши свої справжні наміри.
 Вибачившись, він вийняв зі свого кармана пістолет і
 намірено наввипередки направив його на вас і вашого колегу. Ви миттєво зрозуміли, що це був підступний план, 
 спрямований проти вас, і тепер вам доведеться діяти швидко і рішуче, щоб врятувати себе та свого товариша.""", reply_markup=ReplyKeyboardRemove)
            return ConversationHandler.END
        else:
            await update.message.reply_text("Ви успішно доїхали додому! Ви перемоли")
            return ConversationHandler.END













