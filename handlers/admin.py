from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import bot

from keyboards.keyboard_admin import start_admin,admin_scripts_,admin_delete_scripts,admin_refactor_scripts,admin_choose_refactor,admin_ban_users,admin_choose_projects,admin_delete_projects,admin_jokes,admin_delete_jokes
from class_group.states import ScriptsInsert,Refactor,AdminAllMess,AdminOneMess,AdminInsertProjects,AdminJokes

from db.connect import connection



async def insert_scripts(state):
    global base, cur
    base, cur = await connection()

    async with state.proxy() as data:
        cur.execute('INSERT INTO Scripts(name,description,price,img) VALUES (?,?,?,?)',
                    tuple(data.values()))
        base.commit()

async def insert_projects(state):
    global base, cur
    base, cur = await connection()
    async with state.proxy() as data:
        cur.execute('INSERT INTO Projects(name,img) VALUES (?,?)',
                    tuple(data.values()))
        base.commit()

async def insert_jokes(state):
    global base, cur
    base, cur = await connection()
    async with state.proxy() as data:
        cur.execute('INSERT INTO Jokes(name,joke) VALUES (?,?)',
                    tuple(data.values()))
        base.commit()


async def admin(message:types.Message,state:FSMContext):


    global base, cur
    base, cur = await connection()
    await bot.send_message(message.chat.id,f"Ты в Админке\n\nВыбери опцию:",reply_markup=start_admin)

async def admin_choose_option(callback:types.CallbackQuery,state:FSMContext):

    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "scripts":
        await bot.send_message(callback.from_user.id,f"Выбери опцию",reply_markup=admin_scripts_)
    if str == "allmess":
        await bot.send_message(callback.from_user.id,f"Отправь сообщение, которое разошлется всем пользователям:\n\nДля отмены нажмите: /adminstop")
        await AdminAllMess.messAll.set()
    if str == "onemess":
        await bot.send_message(callback.from_user.id,f"Отправь callback пользователя\n\nДля отмены нажмите: /adminstop")
        await AdminOneMess.call.set()
    if str == "ban":
        await bot.send_message(callback.from_user.id,f"Выбери кого забанить",reply_markup=await admin_ban_users())
    if str == "stat":
        sum_kol_noban_users = 0
        sum_kol_ban_users = 0
        for ret in cur.execute(f"SELECT id FROM Users WHERE ban == 0"):
            if ret:
                sum_kol_noban_users+=1
        for ret in cur.execute(f"SELECT id FROM Users WHERE ban == 1"):
            if ret:
                sum_kol_ban_users+=1
        for start,info,channels,button_about,button_ourProjects,button_consultate,button_contacts,button_scripts,button_jokes in cur.execute(f"SELECT "
                                                                                                                                f"start,info,channels,button_about,"
                                                                                                                                f"button_ourProjects,button_consultate,"
                                                                                                                                f"button_contacts,button_scripts,button_jokes FROM Statisticks"):
            await bot.send_message(callback.from_user.id,f"Количество пользователей НЕ в бане: {sum_kol_noban_users}"
                                                     f"\n\nКоличество пользователей В бане: {sum_kol_ban_users}\n\n"
                                                         f"Нажали старт: {start}\n\n"
                                                         f"Нажали инфо: {info}\n\n"
                                                         f"Нажали каналы: {channels}\n\n"
                                                         f"Нажали о нас: {button_about}\n\n"
                                                         f"Нажали проекты: {button_ourProjects}\n\n"
                                                         f"Нажали консультацию: {button_consultate}\n\n"
                                                         f"Нажали контакты: {button_contacts}\n\n"
                                                         f"Нажали скрипт: {button_scripts}\n\n"
                                                         f"Нажали анекдоты: {button_jokes}",reply_markup=start_admin)
    if str == "projects":
        await bot.send_message(callback.from_user.id, f"Выбери опцию", reply_markup=admin_choose_projects)
    if str == "jokes":
        await bot.send_message(callback.from_user.id,f"Выбери опцию",reply_markup=admin_jokes)
async def admin_choose_scripts(callback:types.CallbackQuery,state:FSMContext):

    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "insert":
        await bot.send_message(callback.from_user.id,f"Введите название продукта:\n\nДля отмены нажмите: /adminstop")
        await ScriptsInsert.name.set()
    if str == "refactor":
        await bot.send_message(callback.from_user.id,"Выбери, какой скрипт изменить:",reply_markup=await admin_refactor_scripts())
        await Refactor.refactor.set()
    if str == "delete":
        await bot.send_message(callback.from_user.id,"Выбери, какой скрипт удалить:",reply_markup=await admin_delete_scripts())

async def admin_projects(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "insert":
        await bot.send_message(callback.from_user.id, "Отправь название продукта:")
        await AdminInsertProjects.name.set()
    if str == "delete":
        await bot.send_message(callback.from_user.id, "Выбери, какой проект удалить:",reply_markup= await admin_delete_projects())


async def admin_choose_delete_projects(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    cur.execute(f"DELETE FROM Projects WHERE id == ?",(str,))
    base.commit()
    cur.execute(f"UPDATE Projects SET id = id - 1 WHERE id > ?", (str,))
    base.commit()
    cur.execute(f"UPDATE sqlite_sequence SET seq = seq - 1 WHERE name == 'Projects'")
    base.commit()
    await bot.send_message(callback.from_user.id, f"Успешно удален выбранный проект!\n\nТы в Админке\n\nВыбери опцию:",
                           reply_markup=start_admin)

# async def admin_projects_insert_name(message:types.Message,state:FSMContext):
#     async with state.proxy() as data:
#         data['name'] = message.text
#     await bot.send_message(message.chat.id, "Введи описание продукта:")
#     await AdminInsertProjects.description.set()


# async def admin_projects_insert_description(message:types.Message,state:FSMContext):
#     async with state.proxy() as data:
#         data['description'] = message.text
#     await bot.send_message(message.chat.id, "Отправь картинку продукта:")
#     await AdminInsertProjects.img.set()
async def admin_projects_insert_name(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(message.chat.id, "Отправь картинку продукта:")
    await AdminInsertProjects.img.set()
async def admin_projects_insert_img(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['img'] = message.photo[0].file_id
    await insert_projects(state)
    await state.finish()
    await bot.send_message(message.chat.id, "Проект успешно внесен!\n\nТы в Админке\n\nВыбери опцию:",reply_markup=start_admin)
async def name_scripts_insert(message:types.Message,state:FSMContext):

    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id,f"Ты в Админке\n\nВыбери опцию:",reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        await bot.send_message(message.chat.id,f"Введи описание продукта:\n\nДля отмены нажмите: /adminstop")
        await ScriptsInsert.description.set()

async def descriptions_scripts_insert(message:types.Message,state:FSMContext):

    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id,f"Ты в Админке\n\nВыбери опцию:",reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            data['description'] = message.text
        await bot.send_message(message.chat.id,f"Введи цену продукта:\n\nДля отмены нажмите: /adminstop")
        await ScriptsInsert.price.set()

async def price_scripts_insert(message:types.Message,state:FSMContext):

    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id,f"Ты в Админке\n\nВыбери опцию:",reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            data['price'] = message.text
        await bot.send_message(message.chat.id,f"Отправь картинку продукта:\n\nДля отмены нажмите: /adminstop")
        await ScriptsInsert.img.set()

async def img_scripts_insert(message:types.Message,state:FSMContext):

    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id,f"Ты в Админке\n\nВыбери опцию:",reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            data['img'] = message.photo[0].file_id

        await insert_scripts(state)
        await bot.send_message(message.chat.id,f"Добавлено!",reply_markup=start_admin)
        await state.finish()

async def admin_delete_callback_scripts(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    cur.execute(f"DELETE FROM Scripts WHERE id = ?",(str,))
    base.commit()
    #UPDATE Scripts SET id = id - 1 WHERE id >4
    cur.execute(f"UPDATE Scripts SET id = id - 1 WHERE id > ?",(str,))
    base.commit()
    cur.execute(f"UPDATE sqlite_sequence SET seq = seq - 1 WHERE name == 'Scripts'")
    base.commit()
    await bot.send_message(callback.from_user.id,f"Успешно удалено!\n\nТы в Админке\n\nВыбери опцию:",reply_markup=start_admin)

async def admin_refactor_callback_scripts(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    async with state.proxy() as data:
        data['id'] = str
    await bot.send_message(callback.from_user.id,f"Выбери, что изменить в этом скрипте:",reply_markup=admin_choose_refactor)
    await Refactor.choose.set()

async def admin_choose_refactor_of_scripts(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "name":
        await bot.send_message(callback.from_user.id,f"Введи новое название продукта:\n\nДля отмены нажмите: /adminstop")
        await Refactor.name.set()
    if str == "description":
        await bot.send_message(callback.from_user.id, f"Введи новое описание продукта:\n\nДля отмены нажмите: /adminstop")
        await Refactor.description.set()
    if str == "price":
        await bot.send_message(callback.from_user.id, f"Введи новую цену продукта:\n\nДля отмены нажмите: /adminstop")
        await Refactor.price.set()
    if str == "img":
        await bot.send_message(callback.from_user.id, f"Отправь новую картинку продукта:\n\nДля отмены нажмите: /adminstop")
        await Refactor.img.set()

async def name_refactor(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            cur.execute(f"UPDATE Scripts SET name = ? WHERE id == ?",(message.text,data['id']))
            base.commit()
        await bot.send_message(message.chat.id, f"Название успешно обновлено!\n\nТы в Админке\n\nВыбери опцию:", reply_markup=start_admin)
        await state.finish()

async def description_refactor(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            cur.execute(f"UPDATE Scripts SET description = ? WHERE id == ?", (message.text, data['id']))
            base.commit()
        await bot.send_message(message.chat.id, f"Описание успешно обновлено!\n\nТы в Админке\n\nВыбери опцию:",
                               reply_markup=start_admin)
        await state.finish()
async def price_refactor(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            cur.execute(f"UPDATE Scripts SET price = ? WHERE id == ?", (message.text, data['id']))
            base.commit()
        await bot.send_message(message.chat.id, f"Цена успешна обновлена!\n\nТы в Админке\n\nВыбери опцию:",
                               reply_markup=start_admin)
        await state.finish()
async def img_refactor(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            cur.execute(f"UPDATE Scripts SET img = ? WHERE id == ?", (message.photo[0].file_id, data['id']))
            base.commit()
        await bot.send_message(message.chat.id, f"Картинка успешна обновлена!\n\nТы в Админке\n\nВыбери опцию:",
                               reply_markup=start_admin)
        await state.finish()

async def admin_send_all_message(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        if message.content_type == "text":
            async with state.proxy() as data:
                data['message'] = message.text
                for (ret,) in cur.execute(f"SELECT callback FROM Users WHERE ban == 0"):
                    try:
                        await state.finish()
                        await bot.send_message(ret, f"{data['message']}")
                    except:
                        continue
            await state.finish()
            await bot.send_message(message.chat.id, f"Успешно отправилось!\n\nТы в Админке\n\nВыбери опцию:",
                                   reply_markup=start_admin)
        if message.content_type == "photo":
            async with state.proxy() as data:
                data['message'] = message.caption
                data['img'] = message.photo[0].file_id
                for (ret,) in cur.execute(f"SELECT callback FROM Users"):
                    try:
                        await state.finish()
                        await bot.send_photo(ret, data['img'],f"{data['message']}")
                    except:
                        continue
            await state.finish()
            await bot.send_message(message.chat.id, f"Успешно отправилось!\n\nТы в Админке\n\nВыбери опцию:",
                                   reply_markup=start_admin)

async def admin_send_call_one_message(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id,f"Ты в Админке\n\nВыбери опцию:",reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            data['call'] = message.text
        await bot.send_message(message.chat.id, f"Хорошо, теперь отправь сообщение для этого пользователя:\n\nДля отмены нажмите: /adminstop")
        await AdminOneMess.messOne.set()

async def admin_send_one_message(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        if message.content_type == "text":
            async with state.proxy() as data:
                data['message'] = message.text
                try:
                    await state.finish()
                    await bot.send_message(data['call'], f"{data['message']}")
                    await bot.send_message(message.chat.id, f"Успешно отправилось!\n\nТы в Админке\n\nВыбери опцию:",
                                           reply_markup=start_admin)
                except:
                    await state.finish()
                    await bot.send_message(message.chat.id,
                                           f"Не удалось отправить сообщение пользователю. Или такого callback не существует или пользователь заблокировал бота.\n\nТы в Админке\n\nВыбери опцию:",
                                           reply_markup=start_admin)


        if message.content_type == "photo":
            async with state.proxy() as data:
                data['message'] = message.caption
                data['img'] = message.photo[0].file_id
                try:
                    await state.finish()
                    await bot.send_photo(data['call'], data['img'],f"{data['message']}")
                    await bot.send_message(message.chat.id, f"Успешно отправилось!\n\nТы в Админке\n\nВыбери опцию:",
                                           reply_markup=start_admin)
                except:
                    await state.finish()
                    await bot.send_message(message.chat.id,
                                           f"Не удалось отправить сообщение пользователю. Или такого callback не существует или пользователь заблокировал бота.\n\nТы в Админке\n\nВыбери опцию:",
                                           reply_markup=start_admin)

async def admin_choose_ban_users(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    cur.execute(f"UPDATE Users SET ban = 1 WHERE callback == ?",(str,))
    base.commit()
    await bot.send_message(callback.from_user.id, f"Бан для пользователя под callback {str} активирован. Получить разбан можно только написав в поддержку и вносом изменений в базу данных!\n\nТы в Админке\n\nВыбери опцию:",
                           reply_markup=start_admin)

async def admin_choose_jokes(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "insert":
        await bot.send_message(callback.from_user.id,f"Введи название анекдота:\n\nНапример: Про питон\n\nДля отмены нажмите: /adminstop")
        await AdminJokes.name.set()
    if str == "delete":
        await bot.send_message(callback.from_user.id,f"Выбери, какой анекдот удалить и нажми на него:",reply_markup=await admin_delete_jokes())

async def admin_choose_delete_jokes(callback:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    cur.execute(f"DELETE FROM Jokes WHERE id = ?", (str,))
    base.commit()
    # UPDATE Jokes SET id = id - 1 WHERE id >4
    cur.execute(f"UPDATE Jokes SET id = id - 1 WHERE id > ?", (str,))
    base.commit()
    cur.execute(f"UPDATE sqlite_sequence SET seq = seq - 1 WHERE name == 'Jokes'")
    base.commit()
    await bot.send_message(callback.from_user.id, f"Успешно удалено!\n\nТы в Админке\n\nВыбери опцию:",
                           reply_markup=start_admin)

async def admin_input_name_jokes(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            data['joke_name'] = message.text
        await bot.send_message(message.chat.id,f"Теперь введи сам анекдот:\n\nДля отмены нажмите: /adminstop")
        await AdminJokes.joke.set()

async def admin_input_joke_jokes(message:types.Message,state:FSMContext):
    if message.text == "/adminstop":
        await state.finish()
        await bot.send_message(message.chat.id, f"Ты в Админке\n\nВыбери опцию:", reply_markup=start_admin)
    else:
        async with state.proxy() as data:
            data['joke_joke'] = message.text
        await insert_jokes(state)
        await state.finish()
        await bot.send_message(message.chat.id, f"Анекдот успешно внесен!\n\nТы в Админке\n\nВыбери опцию:", reply_markup=start_admin)



def setup(dp):
    dp.register_message_handler(admin,commands='adminRusIT_042023MAMQ',state=None)
    dp.register_message_handler(name_scripts_insert,content_types='text', state=ScriptsInsert.name)
    dp.register_message_handler(descriptions_scripts_insert, content_types='text', state=ScriptsInsert.description)
    dp.register_message_handler(price_scripts_insert, content_types='text', state=ScriptsInsert.price)
    dp.register_message_handler(img_scripts_insert, content_types='photo', state=ScriptsInsert.img)

    dp.register_message_handler(name_refactor,content_types='text',state = Refactor.name)
    dp.register_message_handler(description_refactor, content_types='text', state=Refactor.description)
    dp.register_message_handler(price_refactor, content_types='text', state=Refactor.price)
    dp.register_message_handler(img_refactor, content_types='photo', state=Refactor.img)

    dp.register_message_handler(admin_send_all_message, content_types=['photo','text'], state=AdminAllMess.messAll)

    dp.register_message_handler(admin_send_call_one_message, content_types='text', state=AdminOneMess.call)
    dp.register_message_handler(admin_send_one_message, content_types=['photo','text'], state=AdminOneMess.messOne)

    # dp.register_message_handler(admin_projects_insert_name, content_types='text',
    #                             state=AdminInsertProjects.name)

    # dp.register_message_handler(admin_projects_insert_description, content_types='text', state=AdminInsertProjects.description)

    dp.register_message_handler(admin_projects_insert_name, content_types='text',
                                state=AdminInsertProjects.name)
    dp.register_message_handler(admin_projects_insert_img, content_types='photo',
                                state=AdminInsertProjects.img)
    dp.register_message_handler(admin_input_name_jokes, content_types='text',
                                state=AdminJokes.name)
    dp.register_message_handler(admin_input_joke_jokes, content_types='text',
                                state=AdminJokes.joke)

    dp.register_callback_query_handler(admin_choose_option,Text(startswith="admin_"),state=None)
    dp.register_callback_query_handler(admin_choose_scripts, Text(startswith="scripts2_"), state=None)
    dp.register_callback_query_handler(admin_delete_callback_scripts,Text(startswith="delete_"),state=None)
    dp.register_callback_query_handler(admin_refactor_callback_scripts, Text(startswith="refactor_"), state=Refactor.refactor)
    dp.register_callback_query_handler(admin_choose_refactor_of_scripts, Text(startswith="AdminChoose_"),
                                       state=Refactor.choose)

    dp.register_callback_query_handler(admin_choose_ban_users, Text(startswith="banning_"),
                                       state=None)

    dp.register_callback_query_handler(admin_projects, Text(startswith="admprojects_"),
                                       state=None)
    dp.register_callback_query_handler(admin_choose_delete_projects, Text(startswith="deleteProjects_"),
                                       state=None)
    dp.register_callback_query_handler(admin_choose_jokes, Text(startswith="jokes_"),
                                       state=None)
    dp.register_callback_query_handler(admin_choose_delete_jokes, Text(startswith="deleteJokes_"),
                                       state=None)