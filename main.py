import asyncio
from aiogram import Bot, Dispatcher
import logging
import schedule
import datetime
import sys
import config.token as token
from src.TWR import ThreadWithReturn
from scripts.handlers import router
from scripts.admin_handlers import router as admin_router
import src.FSM as FSM
#===========================================================
# Объект бота
bot = Bot(token=token.TOKEN)
# Диспетчер
dp = Dispatcher(storage=FSM.storage)


def default_timer():
    # Настраиваем исполнение задачи каждый час
    schedule.every().day.at("00:00", tz="Europe/Moscow").do(switch_logfile, datetime.datetime.now().date())
    # Бесконечный цикл, чтобы гарантировать выполнение
    while True:
        schedule.run_pending()

def switch_logfile(date: datetime.date):
    logging.basicConfig(filename=f"src/logs/{date}.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        switch_logfile(datetime.datetime.now().date())
        logging.info("Timer started!")
        print()

        threads = [
            ThreadWithReturn(target=default_timer)
        ]

        for thread in threads:
            thread.daemon = True
            thread.start()
  
        print("Started!")
        logging.info("Bot started!")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Stopped!")
        sys.exit()