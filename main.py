from aiogram import executor
from config import dp
from handlers.users import setup as users_setup
from handlers.admin import setup as admin_setup
from db.connect import connection

async def on_startup(_):
    print("BOT IS ONLINE")
    await connection()



if __name__ == '__main__':
    users_setup(dp)
    admin_setup(dp)
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)




