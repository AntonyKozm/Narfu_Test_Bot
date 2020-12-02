from aiogram import executor
from misc import dp
import handlers
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=True)