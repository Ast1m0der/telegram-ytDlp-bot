import time
import cv2
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.downloader import yt_download_sync
import os
import asyncio
import app.keybords as kb

router = Router()

class Reg(StatesGroup):
    name = State()
    number = State()

# хендлер /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет, это простой бот для скачивания контента с youtube, отправь ссылку на видео/плейлист/трек и мы попытаемся его скачать",reply_markup=kb.main)

@router.callback_query(F.data == "settings")
async def cmd_settings(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выбери качество для скачивания\nЕсли доступное качество видео меньше выбранного мы скачаем в наилучшем",reply_markup= await kb.reskb())

@router.callback_query((F.data == "8K") | (F.data == "4K") | (F.data == "1440P") | (F.data == "1080P") | (F.data == "720P") | (F.data == "480P") | (F.data == "360P") | (F.data == "240P") | (F.data == "144P"))
async def cmd_setres(callback: CallbackQuery):
    for i,r in enumerate(kb.buttons):
        kb.buttons[i] = kb.buttons[i].replace("✅","")
        if r == callback.data:
            kb.buttons[i] += "✅"

    await callback.message.edit_text(
        "Что скачиваем?",
        reply_markup=await kb.reskb())


@router.message()
async def download(message: Message):
    progress_queue = asyncio.Queue()
    message_s = await message.answer("Начинаем загрузку...")
    try:
        loop = asyncio.get_running_loop()
        coru =  loop.run_in_executor(None, yt_download_sync, message, progress_queue, asyncio.get_running_loop(), str(time.time()), kb.buttons)

        last_percent = None
        last_update = time.time()
        while True:
            percent = await progress_queue.get()
            if percent == "DONE":
                await message_s.edit_text(f"Обработка...")
                break
            if percent != last_percent and time.time() - last_update  > 1:
                last_update = time.time()
                await message_s.edit_text(f"Загрузка: {percent[7:-4]}")
                last_percent = percent
        paths = await coru
        print(paths)
    except Exception as e:
        await message_s.edit_text(f"Ошибка при загрузке: {e}")
        return
    await message_s.edit_text(f"Выгружаем...")
    for path in paths:
        if ".mp4" in path:
            cap = cv2.VideoCapture(path)
            width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            await message_s.answer_video(
                    FSInputFile(path),
                    height = height,
                    width = width,
            )
            cap.release()
        else:
            await message_s.answer_audio(FSInputFile(path))
        await message_s.delete()
        os.remove(path)
    os.system(f"rm -rf {paths[0][:paths[0].rfind("/")]}")
