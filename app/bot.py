import asyncio

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.tasks.parse_users_urls import ParseUsersUrlTask
from settings.core import config

from main.handlers import router as main_router
from app.parser.handlers import router as parser_router
from app.admin.handlers import router as admin_router

token = config.TOKEN
bot = Bot(token=token)
dispatcher = Dispatcher()
dispatcher.include_router(main_router)
dispatcher.include_router(parser_router)
dispatcher.include_router(admin_router)
task_scheduler = AsyncIOScheduler()


def schedule_jobs():
    # по желанию можно изменить час, когда таска будет выполняться. Для этого в hour указать час
    task_scheduler.add_job(ParseUsersUrlTask(bot=bot).parse_urls, "cron", hour=0)


async def main():
    schedule_jobs()
    task_scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception:
            pass
