from aiogram.types import ReplyKeyboardMarkup


# users keyboards
main_rep_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("💻 Ноутбуки", "📱 Планшеты").add("🖱 Мыши", "⌨ Клавиатуры")\
    .add("🛒 Корзина")

back_rep_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("❌ Отмена")

accept_rep_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("✅ Продолжить", "❌ Отмена")

next_product_rep_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("➡ Следующий", "❌ Отмена", "🛒 В корзину")

back_to_menu_rep_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("💬 В главное меню", "🔄 Повторить поиск")

basket_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("📝 Подробно", "✅ Заказать").add("🗑 Очистить корзину")\
    .add("💬 В главное меню")

basket_products_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("➡ Следующий", "❌ Отмена")

# moderators keyboards
mod_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Добавить товар")

mod_back_or_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("В главное меню", "Назад")

mod_change_type = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add("Ноутбуки", "Планшеты")\
    .add("Мыши", "Клавиатуры")\
    .add("В главное меню", "Назад")

mod_get_pic_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Готово", "В главное меню", "Назад")

mod_accept_form_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Подтвердить", "Повторить")
