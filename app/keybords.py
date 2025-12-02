from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder



main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Настройки",
                          callback_data="settings")]
])


res_buttons = ["8K✅", "4K", "1440P", "1080P","720P","480P","360P","240P","144P"]

async def reskb():
    keyboard = InlineKeyboardBuilder()
    for button in res_buttons:
        keyboard.add(InlineKeyboardButton(text=button,callback_data=button.replace("✅", "")))
    return keyboard.adjust(1).as_markup()

med_buttons = ["Auto✅","Video + Audio", "Audio", "Video"]

async def medkb():

    keyboard = InlineKeyboardBuilder()
    for button in med_buttons:
        keyboard.add(InlineKeyboardButton(text=button,callback_data=button.replace("✅","")))
    return keyboard.adjust(1).as_markup()
