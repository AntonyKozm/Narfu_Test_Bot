from aiogram.dispatcher.filters.state import State, StatesGroup


class Items(StatesGroup):
    waiting = State()
    wait_price = State()
    view = State()
    wait_to_main = State()
    basket_state = State()


class Insert(StatesGroup):
    wait_accept = State()
    wait_accept_insert = State()
    wait_name = State()
    wait_type = State()
    wait_features = State()
    wait_price = State()
    wait_pic = State()