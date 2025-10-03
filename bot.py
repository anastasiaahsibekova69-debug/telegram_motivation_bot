import os
import random
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = os.getenv("BOT_TOKEN")  # токен берём из переменных окружения

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# список подписчиков
subscribers = set()

# функция отправки случайной картинки
async def send_motivation():
    if not subscribers:
        return
    files = os.listdir("motivation")
    if not files:
        return
    photo_path = os.path.join("motivation", random.choice(files))
    for user_id in subscribers:
        try:
            with open(photo_path, "rb") as photo:
                await bot.send_photo(user_id, photo, caption="✨ Твоя карточка на сегодня!")
        except Exception as e:
            print(f"Не удалось отправить {user_id}: {e}")

# /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    subscribers.add(message.chat.id)
    await message.answer("Привет! 🙌 Каждый день я буду присылать тебе случайную карточку ✨")

# /stop
@dp.message_handler(commands=["stop"])
async def stop(message: types.Message):
    subscribers.discard(message.chat.id)
    await message.answer("Ты отписался от рассылки 🚫")

# планировщик — каждый день в 09:00 по Москве
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler.add_job(send_motivation, "cron", hour=9, minute=0)
scheduler.start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
