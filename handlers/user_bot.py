from misc import dp
from aiogram import types
from handlers.messages import MESSAGES, MOD_MES
from aiogram.dispatcher import FSMContext
from handlers.product import Product
from handlers.keyboards import *
from handlers.mystates import *
from handlers.checkers import *
from handlers.userbasket import *
from handlers.mysqlhandlers import clear_basket


async def main_menu(message: types.Message, is_moderator=False):
    if is_moderator:
        await message.answer(MOD_MES["main_menu"], reply_markup=mod_main_kb)
        await Insert.wait_accept.set()
    else:
        await message.answer(MESSAGES["main_menu"], reply_markup=main_rep_kb)
        check_and_create_basket(message.from_user.id)
        await Items.waiting.set()


async def view_basket(message: types.Message, state: FSMContext):
    mess = MESSAGES["basket_head"]
    b = Basket()
    products = b.get_names(message.from_user.id)
    if products == "":
        mess += "\nТоваров нет!"
    else:
        mess += products
        mess += "\n<b>Сумма заказа: </b>" + str(b.get_price()) + "руб"
    await message.answer(mess, reply_markup=basket_keyboard)
    await state.update_data(basket=b)
    await Items.basket_state.set()


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message):
    is_moderator = check_moderator(message.from_user.id)
    if is_moderator:
        await message.answer(MOD_MES["hi"])
    else:
        await message.answer(MESSAGES["hi"])
    await main_menu(message, is_moderator)


@dp.message_handler(state=Items.basket_state, content_types=types.ContentTypes.TEXT)
async def wait_cmd_in_basket(message: types.Message, state: FSMContext):
    message.text = message.text.lower()[2:]
    user_data = await state.get_data()
    b = user_data["basket"]
    if not b.products:
        b.get_template_by_id(message.from_user.id)
    if message.text != "в главное меню":
        if message.text in ["подробно", "следующий"]:
            product = b.get_product()
            if product:
                await message.answer_photo(photo=product["picture"], caption=product["template"],
                                           reply_markup=basket_products_kb)
                await state.update_data(basket=b)
            else:
                await view_basket(message, state)
        elif message.text == "отмена":
            await view_basket(message, state)
        elif message.text == "заказать":
            if b.get_names(message.from_user.id) == "":
                await message.answer(MESSAGES["basket_is_empty"])
            else:
                await message.answer("Товары успешно заказаны!")
                clear_basket(message.from_user.id)
            await view_basket(message, state)
        elif message.text == "очистить корзину":
            if b.get_names(message.from_user.id) == "":
                await message.answer(MESSAGES["basket_is_empty"])
            else:
                clear_basket(message.from_user.id)
                await message.answer(MESSAGES["cleared"])
            await view_basket(message, state)
        else:
            await message.answer("Команда мне доселе неизвестна!")
    else:
        await main_menu(message)


@dp.message_handler(state=Items.waiting, content_types=types.ContentTypes.TEXT)
async def change_item(message: types.Message, state: FSMContext):
    message.text = message.text[2:]
    if message.text.lower() != "отмена":
        if message.text.lower() == "корзина":
            await view_basket(message, state)
        elif message.text.lower() not in ["ноутбуки", "планшеты", "мыши", "клавиатуры"]:
            await message.answer("Выберите одну из категорий")
            return
        else:
            await message.answer("Выбрана категория: " + message.text)
            await answer_price(message, state, message.text.lower())
    else:
        await main_menu(message)


@dp.message_handler(state=Items.wait_price, content_types=types.ContentTypes.TEXT)
async def change_price_range(message: types.Message, state: FSMContext):
    if message.text.lower()[2:] != "отмена":
        result = check_price_range(message.text)
        if result:
            min_price, max_price = int(result[0]), int(result[1])
            if max_price <= min_price:
                await message.answer(MESSAGES["get_price_error"]+MESSAGES["format_prices"])
                return
            await state.update_data(price_range={"min": min_price, "max": max_price})
            user_data = await state.get_data()
            await select_product(message, state, user_data["chosen_product"])
        else:
            await message.answer(MESSAGES["get_price_error"] + MESSAGES["format_prices"])
    else:
        await main_menu(message)


async def select_product(message: types.Message, state: FSMContext, item_key):
    user_data = await state.get_data()
    await message.answer(
        MESSAGES["item_mes"].format(item_key, user_data["price_range"]["min"], user_data["price_range"]["max"]))
    await message.answer(MESSAGES["accept"], reply_markup=accept_rep_kb)
    product = Product(user_data["chosen_product"], user_data["price_range"])
    await state.update_data(product=product)
    await Items.view.set()


@dp.message_handler(state=Items.view, content_types=types.ContentTypes.TEXT)
async def view_products(message: types.Message, state: FSMContext):
    message.text = message.text[2:]
    user_data = await state.get_data()
    product = user_data["product"]
    if message.text.lower() == "продолжить" or message.text.lower() == "следующий":
        if product.num_product == 0:
            product.get_template()
        template = product.get_product()
        if template:
            await message.answer_photo(photo=template["picture"], caption=template["template"], reply_markup=next_product_rep_kb)
            await state.update_data(product=product)
        else:
            await message.answer(MESSAGES["list_out"], reply_markup=back_to_menu_rep_kb)
            await Items.wait_to_main.set()
    elif message.text.lower() == "отмена":
        await main_menu(message)
    elif message.text.lower() == "в корзину":
        if get_and_update_basket(message.from_user.id, product.get_current_product()["id"]):
            await message.answer(MESSAGES["success_collect"])
        else:
            await message.answer(MESSAGES["error_collect"])
    else:
        await message.answer("Команда мне не понятна!")


async def answer_price(message: types.Message, state: FSMContext, chosen_product):
    await message.answer(MESSAGES["get_price_range"] + MESSAGES["format_prices"], reply_markup=back_rep_kb)
    await state.update_data(chosen_product=chosen_product)
    await Items.wait_price.set()


@dp.message_handler(state=Items.wait_to_main, content_types=types.ContentTypes.TEXT)
async def what_you_want(message: types.Message, state: FSMContext):
    message.text = message.text[2:]
    if message.text.lower() == "в главное меню":
        await main_menu(message)
    elif message.text.lower() == "повторить поиск":
        user_data = await state.get_data()
        await answer_price(message, state, user_data["chosen_product"])
    else:
        await message.answer("Команда мне не понятна!")
