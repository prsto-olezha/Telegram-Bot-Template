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


bot = Bot(token=token.TOKEN)
dp = Dispatcher(storage=FSM.storage)


def log_timer():
    schedule.every().day.at("00:00", tz="Europe/Moscow").do(switch_logfile, datetime.datetime.now().date())
    while True:
        schedule.run_pending()


def switch_logfile(date: datetime.date):
    logging.basicConfig(filename=f"src/logs/{date}.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
            ThreadWithReturn(target=log_timer)
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
