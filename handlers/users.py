from aiogram import types
from aiogram.types import InputFile , ChatActions
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import bot

from keyboards.keyboard import start_kb,scripts_kb,phone_kb,projects_kb,keyb_develop,kb_collab,kb_jokes
from db.connect import connection
import datetime
from class_group.states import ScriptLeafThrough,Form,Cooperation,CollabWithUser,ChatGPT
import openai

openai.api_key = "" #  

CHANNEL_ID = ""

async def info(message:types.Message,state:FSMContext):
    global base, cur
    base, cur = await connection()
    await state.finish()
    await bot.send_message(message.chat.id,f"Готовы работать по направлениям:\n\n"
                                           f"Разработка нейронных сетей\n"
                                           f"Разработка умных ассистентов\n"
                                           f"Разработка веб - сайтов\n"
                                           f"Разработка Android приложений\n"
                                           f"Разработка Умных Telegram ботов\n"
                                           f"Настройка сервисов\n"
                                           f"Сопровождение проектов\n"
                                           f"Системное администрирование\n\n"
                                           f"Пишите нам по любой вашей задаче или вопросу! Консультация бесплатная🙂")
    cur.execute(f"UPDATE Statisticks SET info = info + 1")
    base.commit()


async def channels(message:types.Message,state:FSMContext):
    global base, cur
    base, cur = await connection()
    await state.finish()
    await bot.send_message(message.chat.id,f"Подписывайтесь в наш канал - https://t.me/rusit_company , там есть много новостей и не только🤲")
    cur.execute(f"UPDATE Statisticks SET channels = channels + 1")
    base.commit()

async def start(message:types.Message,state: FSMContext):
    await state.finish()
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    global base,cur
    base, cur = await connection()
    user = cur.execute(f"SELECT callback FROM Users WHERE callback == ?",(message.chat.id,)).fetchone()
    if user == None:
        sql_user_insert = """INSERT INTO Users(datatime,callback,link,ban) VALUES(?,?,?,?)"""
        data_insert = (datetime.date.today(),message.chat.id,message.from_user.username,0)
        cur.execute(sql_user_insert,data_insert)
        base.commit()
        photo = InputFile("img/img_start.png")
        await bot.send_photo(message.chat.id,photo,
                               f"Привет! 👋🏼\n\nМы - компания Рус IT 🇷🇺 занимающаяся разработкой и обслуживанием интеллектуальных продуктов на государственном уровне💻"
                               f"\n\nПознакомься с нами поближе!\n\nВыбирай опцию:",
                               reply_markup=start_kb)
    else:
        (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?",(message.chat.id,)).fetchone()
        if ban == 0:
            photo = InputFile("img/img_start.png")
            await bot.send_photo(message.chat.id,photo,
                                   f"Привет! 👋🏼\n\nМы - компания Рус IT 🇷🇺 занимающаяся разработкой и обслуживанием интеллектуальных продуктов на государственном уровне💻"
                                   f"\n\nПознакомься с нами поближе!\n\nВыбирай опцию:",
                                   reply_markup=start_kb)
            cur.execute(f"UPDATE Statisticks SET start = start + 1")
            base.commit()
        elif ban == 1:
            await bot.send_message(message.chat.id,
                                   f"Администратор добавил вас в бан! Обратитесь в поддержку.")


    user_state = cur.execute(f"SELECT callback FROM UserState WHERE callback == ?",(message.chat.id,)).fetchone()
    if user_state == None:
        sql_userState_insert = """INSERT INTO UserState(callback,state) VALUES(?,?)"""
        data_userState_insert = (message.chat.id,1)
        cur.execute(sql_userState_insert,data_userState_insert)
        base.commit()
    else:
        sql_userState_update = """UPDATE UserState SET state = ? WHERE callback == ?"""
        data_userState_update = (1,message.chat.id)
        cur.execute(sql_userState_update,data_userState_update)
        base.commit()
    user_state_project = cur.execute(f"SELECT callback FROM UserStateProjects WHERE callback == ?", (message.chat.id,)).fetchone()
    if user_state_project == None:
        sql_userState_insert = """INSERT INTO UserStateProjects(callback,state) VALUES(?,?)"""
        data_userState_insert = (message.chat.id, 1)
        cur.execute(sql_userState_insert, data_userState_insert)
        base.commit()
    else:
        sql_userState_update = """UPDATE UserStateProjects SET state = ? WHERE callback == ?"""
        data_userState_update = (1, message.chat.id)
        cur.execute(sql_userState_update, data_userState_update)
        base.commit()
    user_state_jokes = cur.execute(f"SELECT callback FROM UserStateJokes WHERE callback == ?",
                                     (message.chat.id,)).fetchone()
    if user_state_jokes == None:
        sql_userState_insert = """INSERT INTO UserStateJokes(callback,state) VALUES(?,?)"""
        data_userState_insert = (message.chat.id, 1)
        cur.execute(sql_userState_insert, data_userState_insert)
        base.commit()
    else:
        sql_userState_update = """UPDATE UserStateJokes SET state = ? WHERE callback == ?"""
        data_userState_update = (1, message.chat.id)
        cur.execute(sql_userState_update, data_userState_update)
        base.commit()


async def callbackKeyboardStart(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    base, cur = await connection()
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (callback.from_user.id,)).fetchone()
    if ban == 1:
        await bot.send_message(callback.from_user.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if str == "whatis":
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass
            photo = InputFile("About2.png")
            await bot.send_photo(callback.from_user.id,photo,reply_markup=start_kb)
            cur.execute(f"UPDATE Statisticks SET button_about = button_about + 1")
            base.commit()
            # await bot.send_message(callback.from_user.id, f"Общие сведения:\n\n"
            #                                               f"Компания образована в феврале 2022 года в Москве несколькими "
            #                                               f"специалистами в области компьютерной науке обработки данных (Data Science)."
            #                                               f"В течение длительного времени основатели, еще до образования компании самостоятельно успешно решили ряд бизнес-задач по"
            #                                               f" предсказанию изменения ценовой политики на различные категории товаров."
            #                                               f"После того, как возник постоянный спрос на подобные решения, в ноябре 2022 года была создана РусАйТи с привлечением специалистов"
            #                                               f" по разработке мобильных приложений и написания программ на различных языках для десктопных приложений."
            #                                               f"\n\nРеализованные проекты:\n\n"
            #                                               f"Санкт-Петербург. Разработан электронный учебник по комплексу вооружения для "
            #                                               f"военной кафедры государственного технического университета для освоения двухлетней "
            #                                               f"учебной программы специалистами. Срок разработки – 120 календарных дней.\n"
            #                                               f"Тверская область. Разработана система мониторинга средних по рынку цен на "
            #                                               f"специализированные товары для компании-производителя моторных масел с возможностью "
            #                                               f"сравнения цен и оповещения при их выходе за установленные параметры с информированием "
            #                                               f"специалистов через телеграм-бот. Срок разработки – 20 календарных дней.\n"
            #                                               f"Разработан умный телеграмм - бот для бизнеса с искусственным интеллектом для "
            #                                               f"автоматизации внутренних и внешних процессов. Вся рутинная работа передалась боту.\n"
            #                                               f"Разработано множество сайтов разной сложности с высоким уровнем безопасности "
            #                                               f"для государственных организаций с интеграцией внешних государственных систем\n"
            #                                               f"Нашими специалистами был разработан бот для помощи беженцам и переселенцам. "
            #                                               f"Данным проектом воспользовались больше  30000 тысячи людей. Проект представлял из себя информирование по вопросам, "
            #                                               f"связанными с миграцией из одного места жительства в другое. Проект помог найти новых друзей и знакомых, "
            #                                               f"найти работу и комфортное место жительство для переселенцев. Также бот позволил снизить нагрузку на горячую линию "
            #                                               f"администрации города, а также на горячие линии государственных учреждений\n"
            #                                               f"Перевод баз данных негосударственного пенсионного фонда на отечественное ПО. "
            #                                               f"Менее чем за месяц перевели 150000 записей с соблюдением законодательства по защите "
            #                                               f"персональных данных на отечественное ПО, настроили миграцию, админку и интеграцию с государственными сервисами.\n\n"
            #                                               f"Почему мы?\n\n"
            #                                               f"1. Нам доверяют государственные организации\n"
            #                                               f"2. Креативные идеи и предложения для заказчика на все задачи\n"
            #                                               f"3. Многолетний опыт разработчиков по всем направлениям\n"
            #                                               f"4. Самые новые и продвинутые технологии. Мы каждый день следим за новостями IT мира\n"
            #                                               f"5. Привлекаем в обсуждение проектов молодых специалистов, для свежих и модных идей\n",reply_markup=start_kb)
            #







        if str == "cooperation":
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass
            photo = InputFile("img/consultate.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Выберите, на какую темы вы бы хотели проконсультироваться:",reply_markup=keyb_develop)
            await Cooperation.what.set()
            cur.execute(f"UPDATE Statisticks SET button_consultate = button_consultate + 1")
            base.commit()
        if str == "contacts":
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass
            await bot.send_message(callback.from_user.id,f"Общество с ограниченной ответственностью «ИНТЕЛЛЕКТУАЛЬНЫЕ ТЕХНОЛОГИИ РУС»\n\nЭлектронная почта: company@rusaiti.ru\n\n"
                                                          f"Телефон: +7(980)496-57-66\n\nИНН: 9724057093", reply_markup=start_kb)
            cur.execute(f"UPDATE Statisticks SET button_contacts = button_contacts + 1")
            base.commit()

        if str == "scripts":
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass

            first_script_unpack = cur.execute(
                f"SELECT id FROM Scripts WHERE id IN (SELECT min(id) FROM Scripts)").fetchone()

            if first_script_unpack == None:
                await bot.send_message(callback.from_user.id, f"На данный момент скрипты отсутствуют, скоро пополним!",
                                       reply_markup=start_kb)
            else:
                (first_script,) = first_script_unpack
                for ret in cur.execute(f"SELECT name,description,price,img FROM Scripts WHERE id = '{first_script}'"):
                    await bot.send_photo(callback.from_user.id, ret[3],
                                         f"Наименование:<b>{ret[0]}</b>\n\nОписание:<b>{ret[1]}</b>\n\nЦена:<b>{ret[2]} рублей</b>\n\nДля того, чтобы вернуться назад - нажмите /start",
                                         parse_mode="HTML", reply_markup=scripts_kb)
            cur.execute(f"UPDATE Statisticks SET button_scripts = button_scripts + 1")
            base.commit()

        if str == "ourprojects":
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass

            first_project_unpack = cur.execute(
                f"SELECT id FROM Projects WHERE id IN (SELECT min(id) FROM Projects)").fetchone()
            if first_project_unpack == None:
                await bot.send_message(callback.from_user.id, f"На данный момент проекты отсутствуют, скоро пополним!",
                                       reply_markup=start_kb)
            else:
                (first_project,) = first_project_unpack
                for ret in cur.execute(f"SELECT img FROM Projects WHERE id = '{first_project}'"):
                    await bot.send_photo(callback.from_user.id, ret[0],
                                         f"Для того, чтобы вернуться назад - нажмите /start",
                                         parse_mode="HTML", reply_markup=projects_kb)
            cur.execute(f"UPDATE Statisticks SET button_ourProjects = button_ourProjects + 1")
            base.commit()
        if str == "joke":
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass
            first_joke_unpack = cur.execute(
                f"SELECT id FROM Jokes WHERE id IN (SELECT min(id) FROM Jokes)").fetchone()
            if first_joke_unpack == None:
                await bot.send_message(callback.from_user.id, f"На данный момент анекдоты отсутствуют, скоро пополним!",
                                       reply_markup=start_kb)
            else:
                (first_joke,) = first_joke_unpack
                for ret in cur.execute(f"SELECT joke FROM Jokes WHERE id = '{first_joke}'"):
                    await bot.send_message(callback.from_user.id,
                                         f"<b>{ret[0]}</b>\n\nДля того, чтобы вернуться назад - нажмите /start",
                                         parse_mode="HTML", reply_markup=kb_jokes)
            cur.execute(f"UPDATE Statisticks SET button_jokes = button_jokes + 1")
            base.commit()
            #photo = InputFile("img/joke.png")
            # await bot.send_photo(callback.from_user.id,photo,
            #                      f"Вы вошли в рубрику анекдотов и шуток про программистов😉\nЭта рубрика постоянно обновляется👍Приятного чтения и смеха😊\n\nИмейте ввиду,"
            #                      f" <b>для того</b>, чтобы вернуться назад - нажмите /start\n\n"
            #                      f"<b>-----1-----</b>\n"
            #                      f"Программист звонит в библиотеку.\n"
            #                      f"— Здравствуйте, Катю можно?\n"
            #                      f"— Она в архиве.\n"
            #                      f"— Разархивируйте ее пожалуйста. Она мне срочно нужна!\n"
            #                      f"<b>-----2-----</b>\n"
            #                      f"— По радио сообщили о переходе на зимнее время, сказав, что «этой ночью, ровно в 03:00 нужно перевести стрелку часов на один час назад, на 02:00».\n"
            #                      f"— У всех программистов эта ночь зависла в бесконечном цикле.\n"
            #                      f"<b>-----3-----</b>\n"
            #                      f"Если бы программисты были врачами, им бы говорили «У меня болит нога», а они отвечали «Ну не знаю, у меня такая же нога, а ничего не болит».\n"
            #                      f"<b>-----4-----</b>\n"
            #                      f"Работа программиста и шамана имеет много общего — оба бормочут непонятные слова, совершают непонятные действия и не могут объяснить, как оно работает.\n",
            #                      parse_mode="HTML")
        if str == "collab":
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass
            photo = InputFile("img/collab.png")
            await bot.send_photo(callback.from_user.id,photo,
                                   f"Если вы являетесь разработчиком и хотите получить новый опыт в проектах, нажмите кнопку <b>Отправить резюме</b> или "
                                   f"отправьте напрямую по почте - company@rusaiti.ru с пометкой <b>Резюме</b>\n\n"
                                   f"Если вы представляете компанию и хотите (или желаете) посотрудничать с нами в "
                                   f"проектах или рекламах,нажмите кнопку <b>Отправить предложение</b>, или отправьте напрямую по почте - company@rusaiti.ru "
                                   f"с пометкой <b>Предложение по сотрудничеству</b> или <b>Предложение по рекламе</b>", parse_mode="HTML",
                                   reply_markup=kb_collab)
        if str == "GPT":
            await bot.send_message(callback.from_user.id,f"Привет! Я - ChatGPT.\n\nМы подружились с компанией RusIT и теперь ты можешь общаться со мной и задавать вопросы"
                                                         f"прямо тут!🔥\n\nПиши свой запрос:\n\nДля того, чтобы вернуться назад нажми - /start")
            await ChatGPT.mess.set()

async def mess_to_chatGPT(message:types.Message,state:FSMContext):
    if message.content_type != "text":
        await bot.send_message(message.chat.id,f"Я принимаю только текстовые сообщения. Давай попробуем еще раз.")
        await ChatGPT.mess.set()
    if message.text == "/start":
        await start(message,state)
        await state.finish()
    else:
        await bot.send_chat_action(chat_id=message.chat.id,action=ChatActions.TYPING)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", # gpt-3.5-turbo text-davinci-003
                messages = [
                    {"role": "system", "content": "/start"},
                    {"role": "user", "content": message.text}
                ]
                # prompt=message.text,
                # temperature=0.7,
                # max_tokens=150,
                # top_p=1,
                # frequency_penalty=0.9,
                # presence_penalty=0.7,
                # stop=None
            )
            await bot.send_message(message.chat.id,
                                   f"{response['choices'][0]['message']['content']}\n\nДля того, чтобы вернуться назад - нажми /start")
            #await bot.send_message(message.chat.id,f"{response['choices'][0]['text']}\n\nДля того, чтобы вернуться назад - нажми /start")
            await ChatGPT.mess.set()
        except:
            await bot.send_message(message.chat.id,f"Извини, слишком много запросов, сейчас не могу ответить. Попробуй позже.\n\nДля того, чтобы вернуться назад - нажми /start")
            await ChatGPT.mess.set()




async def cooperation_what_of_user(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    base, cur = await connection()
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (callback.from_user.id,)).fetchone()
    if ban == 1:
        await bot.send_message(callback.from_user.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if str == "II":
            async with state.proxy() as data:
                data['what'] = "Искусственный Интеллект"
            photo = InputFile("img/II_Bot.png")
            await bot.send_photo(callback.from_user.id,photo,f"Вы выбрали Искусственный Интеллект.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Sys":
            async with state.proxy() as data:
                data['what'] = "Сис. Администрирование"
            photo = InputFile("img/sys_adm.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Вы выбрали Сис. Администрирование.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Bots":
            async with state.proxy() as data:
                data['what'] = "Умный ТГ Бот"
            photo = InputFile("img/tg_bot.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Вы выбрали Умный ТГ Бот.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Android":
            async with state.proxy() as data:
                data['what'] = "Android Приложение"
            photo = InputFile("img/android.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Вы выбрали Android Приложение.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Asists":
            async with state.proxy() as data:
                data['what'] = "Умный Ассистент"
            photo = InputFile("img/assist.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Вы выбрали Умный Ассистент.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Audit":
            async with state.proxy() as data:
                data['what'] = "Аудит цифровых решений"
            photo = InputFile("img/audit.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Вы выбрали Аудит цифровых решений.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Web":
            async with state.proxy() as data:
                data['what'] = "Web Сайт"
            photo = InputFile("img/web-site.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Вы выбрали Web Сайт.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Escort":
            async with state.proxy() as data:
                data['what'] = "Сопровождение проекта"
            photo = InputFile("img/sopr_projects.png")
            await bot.send_photo(callback.from_user.id, photo ,f"Вы выбрали Сопровождение проекта.Введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if str == "Other":
            await bot.send_message(callback.from_user.id, f"Введите, на какую тему вы бы хотели проконсультироваться:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.other.set()
        if str == "back":
            await state.finish()
            try:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                pass
            photo = InputFile("img/img_start.png")
            await bot.send_photo(callback.from_user.id,photo,
                                   f"Привет! 👋🏼\n\nМы - компания Рус IT 🇷🇺 занимающаяся разработкой и обслуживанием интеллектуальных продуктов на государственном уровне💻"
                                   f"\n\nПознакомься с нами поближе!\n\nВыбирай опцию:",
                                   reply_markup=start_kb)

async def user_insert_consult_other(message:types.Message,state:FSMContext):
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (message.chat.id,)).fetchone()
    if ban == 1:
        await bot.send_message(message.chat.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if message.content_type != 'text':
            await bot.send_message(message.chat.id,
                                   f"Можно отправлять только текстовое сообщение!Напишите еще раз\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.other.set()
        if message.text == "/start":
            await start(message, state)
        else:
            async with state.proxy() as data:
                data['what'] = message.text
            await bot.send_message(message.chat.id, f"Хорошо, введите ваш вопрос консультации или описание проекта:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()




async def throughtProjects(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    base, cur = await connection()
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (callback.from_user.id,)).fetchone()
    if ban == 1:
        await bot.send_message(callback.from_user.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if str == "left":
            sql_state_update = """UPDATE UserStateProjects SET state = state - 1 WHERE callback == ?"""
            data_update = (callback.from_user.id,)
            cur.execute(sql_state_update, data_update)
            base.commit()
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            project_unpack = cur.execute(
                f"SELECT id FROM Projects WHERE id IN(SELECT state FROM UserStateProjects WHERE callback == ?)",
                (callback.from_user.id,)).fetchone()
            if project_unpack == None:
                (max_id_project,) = cur.execute(f"SELECT max(id) FROM Projects").fetchone()
                sql_userState_update = """UPDATE UserStateProjects SET state = ? WHERE callback == ?"""
                data_userState_update = (max_id_project, callback.from_user.id)
                cur.execute(sql_userState_update, data_userState_update)
                base.commit()
            for ret in cur.execute(
                    f"SELECT img FROM Projects WHERE id IN(SELECT state FROM UserStateProjects WHERE callback == ?)",
                    (callback.from_user.id,)):
                await bot.send_photo(callback.from_user.id, ret[0],
                                     f"Для того, чтобы вернуться назад - нажмите /start",
                                     parse_mode="HTML", reply_markup=projects_kb)
        if str == "right":
            sql_state_update = """UPDATE UserStateProjects SET state = state + 1 WHERE callback == ?"""
            data_update = (callback.from_user.id,)
            cur.execute(sql_state_update, data_update)
            base.commit()
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            project_unpack = cur.execute(
                f"SELECT id FROM Projects WHERE id IN(SELECT state FROM UserStateProjects WHERE callback == ?)",
                (callback.from_user.id,)).fetchone()
            if project_unpack == None:
                sql_userState_update = """UPDATE UserStateProjects SET state = ? WHERE callback == ?"""
                data_userState_update = (1, callback.from_user.id)
                cur.execute(sql_userState_update, data_userState_update)
                base.commit()
            for ret in cur.execute(
                    f"SELECT img FROM Projects WHERE id IN(SELECT state FROM UserStateProjects WHERE callback == ?)",
                    (callback.from_user.id,)):
                await bot.send_photo(callback.from_user.id, ret[0],
                                     f"Для того, чтобы вернуться назад - нажмите /start",
                                     parse_mode="HTML", reply_markup=projects_kb)




async def throughtScripts(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    base, cur = await connection()
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (callback.from_user.id,)).fetchone()
    if ban == 1:
        await bot.send_message(callback.from_user.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if str == "left":
            sql_state_update = """UPDATE UserState SET state = state - 1 WHERE callback == ?"""
            data_update = (callback.from_user.id,)
            cur.execute(sql_state_update, data_update)
            base.commit()
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            script_unpack = cur.execute(
                f"SELECT id FROM Scripts WHERE id IN(SELECT state FROM UserState WHERE callback == ?)",
                (callback.from_user.id,)).fetchone()
            if script_unpack == None:
                (max_id_script,) = cur.execute(f"SELECT max(id) FROM Scripts").fetchone()
                sql_userState_update = """UPDATE UserState SET state = ? WHERE callback == ?"""
                data_userState_update = (max_id_script, callback.from_user.id)
                cur.execute(sql_userState_update, data_userState_update)
                base.commit()
            for ret in cur.execute(
                    f"SELECT name,description,price,img FROM Scripts WHERE id IN(SELECT state FROM UserState WHERE callback == ?)",
                    (callback.from_user.id,)):
                await bot.send_photo(callback.from_user.id, ret[3],
                                     f"Наименование:<b>{ret[0]}</b>\n\nОписание:<b>{ret[1]}</b>\n\nЦена:<b>{ret[2]} рублей</b>\n\nДля того, чтобы вернуться назад - нажмите /start",
                                     parse_mode="HTML", reply_markup=scripts_kb)
        if str == "right":
            sql_state_update = """UPDATE UserState SET state = state + 1 WHERE callback == ?"""
            data_update = (callback.from_user.id,)
            cur.execute(sql_state_update, data_update)
            base.commit()
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            script_unpack = cur.execute(
                f"SELECT id FROM Scripts WHERE id IN(SELECT state FROM UserState WHERE callback == ?)",
                (callback.from_user.id,)).fetchone()
            if script_unpack == None:
                sql_userState_update = """UPDATE UserState SET state = ? WHERE callback == ?"""
                data_userState_update = (1, callback.from_user.id)
                cur.execute(sql_userState_update, data_userState_update)
                base.commit()
            for ret in cur.execute(
                    f"SELECT name,description,price,img FROM Scripts WHERE id IN(SELECT state FROM UserState WHERE callback == ?)",
                    (callback.from_user.id,)):
                await bot.send_photo(callback.from_user.id, ret[3],
                                     f"Наименование:<b>{ret[0]}</b>\n\nОписание:<b>{ret[1]}</b>\n\nЦена:<b>{ret[2]} рублей</b>\n\nДля того, чтобы вернуться назад - нажмите /start",
                                     parse_mode="HTML", reply_markup=scripts_kb)
        if str == "choose":
            await bot.send_message(callback.from_user.id,
                                   f"Введите свое имя:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Form.name.set()




async def FormName(message: types.Message,state:FSMContext):
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (message.chat.id,)).fetchone()
    if ban == 1:
        await bot.send_message(message.chat.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if message.content_type != 'text':
            await bot.send_message(message.chat.id,
                                   f"Можно отправлять только текстовое сообщение!Напишите ваше имя еще раз:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Form.name.set()
        if message.text == "/start":
            await start(message, state)
        else:
            async with state.proxy() as data:
                data['callback'] = message.chat.id
                data['link'] = message.from_user.username
                data['name'] = message.text
            await bot.send_message(message.chat.id, f"Отлично!Нажмите на кнопку, чтобы отправить ваш номер телефона. Так мы сможем связаться с вами",
                                   reply_markup=phone_kb)
            await Form.phone.set()



async def phone(message: types.Message,state: FSMContext):
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (message.chat.id,)).fetchone()
    if ban == 1:
        await bot.send_message(message.chat.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if message.content_type == 'text':
            if "Вернуться назад" in message.text:
                await state.finish()
                remove_kb = types.ReplyKeyboardRemove()
                await bot.send_message(message.chat.id, f"Отменяю...",
                                       reply_markup=remove_kb)
                await start(message, state)
        else:
            async with state.proxy() as data:
                data['phone'] = message.contact.phone_number
                (script_name,) = cur.execute(
                    f"SELECT name FROM Scripts WHERE id IN(SELECT state FROM UserState WHERE callback == ?)",
                    (message.chat.id,)).fetchone()
                await bot.send_message(CHANNEL_ID,
                                       f"Дата: {datetime.date.today()}\n\nCallback: {data['callback']}\n\nLink: @{data['link']}\n\nИмя: {data['name']}\n\n"
                                       f"Номер телефона: {data['phone']}\n\nПродукт: {script_name}")
            remove_kb = types.ReplyKeyboardRemove()
            await bot.send_message(message.chat.id, f"Мы приняли вашу заявку и ответим в ближайшее время!",
                                   reply_markup=remove_kb)
            await start(message, state)



async def cooperation_answer(message:types.Message,state:FSMContext):
    base, cur = await connection()
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (message.chat.id,)).fetchone()
    if ban == 1:
        await bot.send_message(message.chat.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if message.content_type != 'text':
            await bot.send_message(message.chat.id,
                                   f"Можно отправлять только текстовое сообщение!Напишите еще раз:\n\nДля того,чтобы вернуться назад нажмите /start")
            await Cooperation.answer.set()
        if message.text == "/start":
            await start(message, state)
        else:
            async with state.proxy() as data:
                data['callback'] = message.chat.id
                data['link'] = message.from_user.username
                data['answer'] = message.text
            await bot.send_message(message.chat.id,f"Нажмите на кнопку, чтобы отправить ваш номер телефона",reply_markup=phone_kb)
            await Cooperation.phone.set()


async def cooperation_phone(message:types.Message,state:FSMContext):
    base, cur = await connection()
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (message.chat.id,)).fetchone()
    if ban == 1:
        await bot.send_message(message.chat.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if message.content_type == 'text':
            if "Вернуться назад" in message.text:
                await state.finish()
                remove_kb = types.ReplyKeyboardRemove()
                await bot.send_message(message.chat.id, f"Отменяю...",
                                       reply_markup=remove_kb)
                await start(message, state)
        else:
            async with state.proxy() as data:
                data['phone'] = message.contact.phone_number
                await bot.send_message(CHANNEL_ID,
                                       f"Дата: {datetime.date.today()}\n\nCallback: {data['callback']}\n\nLink: @{data['link']}\n\n"
                                       f"Номер телефона: {data['phone']}\n\nПродукт: {data['what']}\n\nПредложение или вопрос: {data['answer']}")

            remove_kb = types.ReplyKeyboardRemove()
            await bot.send_message(message.chat.id, f"Мы приняли вашу заявку и ответим в ближайшее время!",
                                   reply_markup=remove_kb)
            await start(message, state)

async def collab_with_user(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "rezume":
        await bot.send_message(callback.from_user.id, f"Отправьте ваш документ сюда:\n\nЯ могу принять файлы с расширением .docx .xls .txt .pptx"
                                                      f"\n\nДля того,чтобы вернуться назад нажмите /start")
        await CollabWithUser.doc.set()
    if str == "offer":
        await bot.send_message(callback.from_user.id,
                               f"Отправьте ваш документ сюда:\n\nЯ могу принять файлы с расширением .docx .xls .txt .pptx"
                               f"\n\nДля того,чтобы вернуться назад нажмите /start")
        await CollabWithUser.doc.set()

    if str == "back":
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await state.finish()
        photo = InputFile("img/img_start.png")
        await bot.send_photo(callback.from_user.id, photo,
                             f"Привет! 👋🏼\n\nМы - компания Рус IT 🇷🇺 занимающаяся разработкой и обслуживанием интеллектуальных продуктов на государственном уровне💻"
                             f"\n\nПознакомься с нами поближе!\n\nВыбирай опцию:",
                             reply_markup=start_kb)

async def user_collab_send_document(message:types.Message,state:FSMContext):
    if message.content_type == "text":
        if message.text == "/start":
            await state.finish()
            await start(message,state)
        else:
            await bot.send_message(message.chat.id, f"Я могу принять файлы с расширением .docx .xls .txt .pptx"
                               f"\n\nДля того,чтобы вернуться назад нажмите /start")
            await CollabWithUser.doc.set()
    else:
        async with state.proxy() as data:
            data['link'] = message.from_user.username
            data['call'] = message.chat.id
            data['doc'] = message.document.file_id
            await bot.send_document(CHANNEL_ID,data['doc'],caption=f"Дата: {datetime.date.today()}\n\nCallback: {data['call']}\n\nLink: {data['link']}")
        await state.finish()
        await bot.send_message(message.chat.id,f"Спасибо, Мы приняли ваш документ! Ответим в ближайшее время!",reply_markup=start_kb)

async def throughtJokes(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    base, cur = await connection()
    (ban,) = cur.execute(f"SELECT ban FROM Users WHERE callback == ?", (callback.from_user.id,)).fetchone()
    if ban == 1:
        await bot.send_message(callback.from_user.id,
                               f"Администратор добавил вас в бан! Обратитесь в поддержку.")
    elif ban == 0:
        if str == "left":
            sql_state_update = """UPDATE UserStateJokes SET state = state - 1 WHERE callback == ?"""
            data_update = (callback.from_user.id,)
            cur.execute(sql_state_update, data_update)
            base.commit()
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            joke_unpack = cur.execute(
                f"SELECT id FROM Jokes WHERE id IN(SELECT state FROM UserStateJokes WHERE callback == ?)",
                (callback.from_user.id,)).fetchone()
            if joke_unpack == None:
                (max_id_joke,) = cur.execute(f"SELECT max(id) FROM Jokes").fetchone()
                sql_userState_update = """UPDATE UserStateJokes SET state = ? WHERE callback == ?"""
                data_userState_update = (max_id_joke, callback.from_user.id)
                cur.execute(sql_userState_update, data_userState_update)
                base.commit()
            for ret in cur.execute(
                    f"SELECT joke FROM Jokes WHERE id IN(SELECT state FROM UserStateJokes WHERE callback == ?)",
                    (callback.from_user.id,)):
                await bot.send_message(callback.from_user.id,
                                     f"<b>{ret[0]}</b>\n\nДля того, чтобы вернуться назад - нажмите /start",
                                     parse_mode="HTML", reply_markup=kb_jokes)
        if str == "right":
            sql_state_update = """UPDATE UserStateJokes SET state = state + 1 WHERE callback == ?"""
            data_update = (callback.from_user.id,)
            cur.execute(sql_state_update, data_update)
            base.commit()
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            jokes_unpack = cur.execute(
                f"SELECT id FROM Jokes WHERE id IN(SELECT state FROM UserStateJokes WHERE callback == ?)",
                (callback.from_user.id,)).fetchone()
            if jokes_unpack == None:
                sql_userState_update = """UPDATE UserStateJokes SET state = ? WHERE callback == ?"""
                data_userState_update = (1, callback.from_user.id)
                cur.execute(sql_userState_update, data_userState_update)
                base.commit()
            for ret in cur.execute(
                    f"SELECT joke FROM Jokes WHERE id IN(SELECT state FROM UserStateJokes WHERE callback == ?)",
                    (callback.from_user.id,)):
                await bot.send_message(callback.from_user.id,
                                     f"<b>{ret[0]}</b>\n\nДля того, чтобы вернуться назад - нажмите /start",
                                     parse_mode="HTML", reply_markup=kb_jokes)



def setup(dp):
    dp.register_message_handler(start,commands='start',state = None)
    dp.register_message_handler(info, commands='info', state=None)
    dp.register_message_handler(channels, commands='channels', state=None)
    dp.register_message_handler(FormName,content_types='text', state=Form.name)
    dp.register_message_handler(phone, content_types=['contact','text'], state=Form.phone)
    dp.register_message_handler(cooperation_answer, content_types='text', state=Cooperation.answer)
    dp.register_message_handler(cooperation_phone, content_types=['contact','text'], state=Cooperation.phone)
    dp.register_message_handler(user_insert_consult_other, content_types=['text'], state=Cooperation.other)
    dp.register_message_handler(user_collab_send_document, content_types=['text','document'], state=CollabWithUser.doc)
    dp.register_message_handler(mess_to_chatGPT, content_types='any', state=ChatGPT.mess)


    dp.register_callback_query_handler(callbackKeyboardStart,Text(startswith="start_"),state=None)
    dp.register_callback_query_handler(throughtScripts, Text(startswith="scripts_"),state=None)
    dp.register_callback_query_handler(throughtProjects, Text(startswith="projects_"), state=None)
    dp.register_callback_query_handler(cooperation_what_of_user, Text(startswith="develop_"), state=Cooperation.what)
    dp.register_callback_query_handler(collab_with_user, Text(startswith="collab_"), state=None)
    dp.register_callback_query_handler(throughtJokes, Text(startswith="jokesuser_"), state=None)
