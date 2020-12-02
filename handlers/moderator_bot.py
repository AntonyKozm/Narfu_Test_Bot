from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto

from handlers.keyboards import *
from handlers.messages import MOD_MES
from handlers.mystates import Insert
from misc import dp
from handlers.checkers import get_features_template, get_characteristic, shape_and_insert


async def mod_main_menu(message: types.Message):
    await message.answer(MOD_MES["main_menu"], reply_markup=mod_main_kb)
    await Insert.wait_accept.set()


async def answer_name(message: types.Message):
    await message.answer(MOD_MES["answer_name"], reply_markup=mod_back_or_main_kb)
    await Insert.wait_name.set()


async def answer_type(message: types.Message):
    await message.answer(MOD_MES["answer_type"], reply_markup=mod_change_type)
    await message.answer(MOD_MES["if_mistake"])
    await Insert.wait_type.set()


async def answer_features(message: types.Message):
    await message.answer(MOD_MES["answer_features"], reply_markup=mod_back_or_main_kb)
    prod_type = message.text.lower()
    await message.answer(MOD_MES["format_features"].format(prod_type) + get_features_template(prod_type))
    await message.answer(MOD_MES["if_mistake"])
    await Insert.wait_features.set()


async def answer_price(message: types.Message):
    await message.answer(MOD_MES["answer_price"], reply_markup=mod_back_or_main_kb)
    await Insert.wait_price.set()


async def answer_pic(message: types.Message, state: FSMContext):
    await message.answer(MOD_MES["answer_pic"], reply_markup=mod_get_pic_kb)
    await state.update_data(photos=[])
    await Insert.wait_pic.set()


async def finish(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        MOD_MES["finish_form"].format(
            user_data["product_name"], user_data["product_type"],
            get_characteristic(user_data["features"], user_data["product_type"]),
            user_data["price"]))
    media = []
    print(user_data["photos"])
    for ph_id in user_data["photos"]:
        media.append(InputMediaPhoto(ph_id))
    await message.answer_media_group(media=media)
    await message.answer(MOD_MES["accept_form"], reply_markup=mod_accept_form_kb)
    await Insert.wait_accept_insert.set()


@dp.message_handler(state=Insert.wait_accept, content_types=types.ContentTypes.TEXT)
async def first(message: types.Message):
    if message.text.lower() == "добавить товар" or message.text.lower() == "назад":
        if message.text.lower() == "добавить товар":
            await message.answer(MOD_MES["accept"])
            await answer_name(message)
    else:
        await mod_main_menu(message)


@dp.message_handler(state=Insert.wait_name, content_types=types.ContentTypes.TEXT)
async def second(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await mod_main_menu(message)
        return
    await state.update_data(product_name=message.text)
    await answer_type(message)


@dp.message_handler(state=Insert.wait_type, content_types=types.ContentTypes.TEXT)
async def third(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await answer_name(message)
        return
    await state.update_data(product_type=message.text.lower())
    await answer_features(message)


@dp.message_handler(state=Insert.wait_features, content_types=types.ContentTypes.TEXT)
async def fourth(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await answer_type(message)
        return
    await state.update_data(features=message.text)
    await answer_price(message)


@dp.message_handler(state=Insert.wait_price, content_types=types.ContentTypes.TEXT)
async def fifth(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await answer_features(message)
        return
    await state.update_data(price=message.text)
    await answer_pic(message, state)


@dp.message_handler(state=Insert.wait_pic, content_types=types.ContentTypes.TEXT)
async def sixth(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await answer_price(message)
        return
    if message.text.lower() == "готово":
        await finish(message, state)


@dp.message_handler(state=Insert.wait_pic, content_types=types.ContentTypes.PHOTO)
async def sixth(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    photo_id = user_data["photos"]
    photo_id.append(message.photo[len(message.photo) - 1].file_id)
    await state.update_data(photos=photo_id)


@dp.message_handler(state=Insert.wait_accept_insert, content_types=types.ContentTypes.TEXT)
async def seven(message: types.Message, state: FSMContext):
    if message.text.lower() == "подтвердить":
        user_data = await state.get_data()
        shape_and_insert(user_data)

