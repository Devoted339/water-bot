import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime, timedelta
from typing import Dict

API_TOKEN = "8081316889:AAF2W-kI2SMz14YEThfC3_G7-_08lp2FWPA"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WaterStates(StatesGroup):
    waiting_for_weight = State()
    waiting_for_drink_amount = State()
    waiting_for_reminder_time = State()

DRINKS = {
    "вода": 1.0, "чай": 0.9, "кава": 0.5,
    "кава з молоком": 0.6, "сік": 0.8, "молоко": 0.7,
    "лимонад": 0.4, "кола": 0.3
}

class UserData:
    def __init__(self):
        self.weight = None
        self.daily_goal = 2000
        self.consumed = 0
        self.total = 0
        self.history = []
        self.daily_history = {}
        self.last_date = datetime.now().strftime('%Y-%m-%d')
        self.setup_completed = False
        self.streak = 0
        self.achievements = []
        self.reminder_time = None
        self.reminder_enabled = False

    def check_new_day(self):
        today = datetime.now().strftime('%Y-%m-%d')
        if self.last_date != today:
            self.history.append(f"{self.last_date}: {self.consumed}")
            self.daily_history[self.last_date] = self.consumed
            if self.consumed >= self.daily_goal:
                self.streak += 1
                self.check_achievements()
            else:
                self.streak = 0
            self.consumed = 0
            self.last_date = today

    def add_drink(self, name, amount, coef):
        water = amount * coef
        self.consumed += water
        self.total += water

    def check_achievements(self):
        achievements_map = {
            3: "3 дні поспіль 🥉",
            7: "7 днів поспіль 🥈",
            14: "14 днів поспіль 🥇",
            30: "30 днів поспіль 🏆"
        }
        if self.streak in achievements_map and achievements_map[self.streak] not in self.achievements:
            self.achievements.append(achievements_map[self.streak])
            return achievements_map[self.streak]
        return None

    def get_achievements(self):
        if not self.achievements:
            return "Поки немає досягнень"
        return "\n".join(self.achievements)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
users = {}
pending_drinks = {}
reminder_tasks = {}

def get_user(uid):
    if uid not in users:
        users[uid] = UserData()
    users[uid].check_new_day()
    return users[uid]

def calculate_goal(weight):
    if weight < 30:
        weight = 30
    if weight > 400:
        weight = 400
    return int(weight * 33)

async def send_reminder(user_id):
    await asyncio.sleep(1)
    while True:
        user = get_user(user_id)
        if user.reminder_enabled and user.reminder_time:
            now = datetime.now().strftime("%H:%M")
            if now == user.reminder_time:
                await bot.send_message(user_id, f"Нагадування! Час випити води! Поточна норма: {user.consumed:.0f}/{user.daily_goal} мл 💧")
                await asyncio.sleep(60)
        await asyncio.sleep(30)

def start_reminder(user_id):
    if user_id in reminder_tasks:
        reminder_tasks[user_id].cancel()
    reminder_tasks[user_id] = asyncio.create_task(send_reminder(user_id))

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="250 💧", callback_data="w250"),
         InlineKeyboardButton(text="500 💧", callback_data="w500")],
        [InlineKeyboardButton(text="1000 💧", callback_data="w1000"),
         InlineKeyboardButton(text="2000 💧", callback_data="w2000")],
        [InlineKeyboardButton(text="Напій 🥤", callback_data="drink")],
        [InlineKeyboardButton(text="Статистика 📊", callback_data="stats"),
         InlineKeyboardButton(text="Досягнення 🏆", callback_data="achievements")],
        [InlineKeyboardButton(text="Нагадування ⏰", callback_data="reminder"),
         InlineKeyboardButton(text="Допомога ℹ️", callback_data="help")]
    ])

def drinks_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вода 💧", callback_data="drink_вода"),
         InlineKeyboardButton(text="Чай 🍵", callback_data="drink_чай")],
        [InlineKeyboardButton(text="Кава ☕", callback_data="drink_кава"),
         InlineKeyboardButton(text="Кава з молоком ☕", callback_data="drink_кава з молоком")],
        [InlineKeyboardButton(text="Сік 🧃", callback_data="drink_сік"),
         InlineKeyboardButton(text="Молоко 🥛", callback_data="drink_молоко")],
        [InlineKeyboardButton(text="Лимонад 🥤", callback_data="drink_лимонад"),
         InlineKeyboardButton(text="Кола 🥤", callback_data="drink_кола")],
        [InlineKeyboardButton(text="Назад ◀️", callback_data="back")]
    ])

@dp.message(Command("start"))
async def start(msg: types.Message, state: FSMContext):
    await state.clear()
    user = get_user(msg.from_user.id)
    await msg.answer("Вітаю! Я бот для відстеження водного балансу! 💧\n\nВведіть вашу вагу:")
    if not user.weight:
        await state.set_state(WaterStates.waiting_for_weight)
    else:
        await msg.answer("Головне меню 📋", reply_markup=main_keyboard())

@dp.message(WaterStates.waiting_for_weight)
async def get_weight(msg: types.Message, state: FSMContext):
    user = get_user(msg.from_user.id)
    try:
        w = float(msg.text)
        if w < 30:
            await msg.answer("Вага не може бути менше 30 кг! Введіть реальну вагу ❌")
            return
        if w > 200:
            await msg.answer("Вага не може бути більше 400 кг! Введіть реальну вагу ❌")
            return
        user.weight = w
        user.daily_goal = calculate_goal(w)
        user.setup_completed = True
        await state.clear()
        await msg.answer(f"Вага збережена: {w} кг ✅\nДенна норма: {user.daily_goal} мл 💧\n\nГоловне меню 📋", reply_markup=main_keyboard())
    except:
        await msg.answer("Помилка! Введіть число ❌")

@dp.message(WaterStates.waiting_for_drink_amount)
async def get_drink_amount(msg: types.Message, state: FSMContext):
    user = get_user(msg.from_user.id)
    drink_info = pending_drinks.get(msg.from_user.id)
    if not drink_info:
        await state.clear()
        await msg.answer("Будь ласка, оберіть напій з меню 🥤", reply_markup=main_keyboard())
        return
    try:
        amount = float(msg.text)
        if amount <= 0:
            await msg.answer("Кількість має бути більше 0 мл ❌")
            return
        if amount > 2000:
            await msg.answer("Забагато! Максимум 2000 мл за раз ❌")
            return
        name = drink_info["name"]
        coef = drink_info["coef"]
        user.add_drink(name, amount, coef)
        water_amount = amount * coef
        await state.clear()
        if msg.from_user.id in pending_drinks:
            del pending_drinks[msg.from_user.id]
        await msg.answer(f"Додано: {name} ✅\n{amount} мл 🥤 → {water_amount:.0f} мл води 💧\n{user.consumed:.0f}/{user.daily_goal} мл 💧", reply_markup=main_keyboard())
    except:
        await msg.answer("Помилка! Введіть число ❌")

@dp.message(WaterStates.waiting_for_reminder_time)
async def get_reminder_time(msg: types.Message, state: FSMContext):
    user = get_user(msg.from_user.id)
    try:
        time_str = msg.text.strip()
        if re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time_str):
            user.reminder_time = time_str
            user.reminder_enabled = True
            start_reminder(msg.from_user.id)
            await state.clear()
            await msg.answer(f"Нагадування встановлено на {time_str} ✅\nЯ буду нагадувати вам пити воду! ⏰", reply_markup=main_keyboard())
        else:
            await msg.answer("Невірний формат! Введіть час у форматі ГГ:ХХ ❌")
    except:
        await msg.answer("Помилка! Введіть час у форматі ГГ:ХХ ❌")

@dp.message()
async def handle_text(msg: types.Message):
    user = get_user(msg.from_user.id)
    text = msg.text.lower()
    found_drink = None
    found_amount = None
    nums = re.findall(r'\d+', text)
    if nums:
        found_amount = float(nums[0])
    for drink in DRINKS:
        if drink in text:
            found_drink = drink
            break
    if found_drink and found_amount:
        if found_amount > 2000:
            await msg.answer("Забагато! Максимум 2000 мл за раз ❌")
            return
        coef = DRINKS[found_drink]
        user.add_drink(found_drink, found_amount, coef)
        water_amount = found_amount * coef
        await msg.answer(f"Додано: {found_drink} ✅\n{found_amount} мл 🥤 → {water_amount:.0f} мл води 💧\n{user.consumed:.0f}/{user.daily_goal} мл 💧")
    elif nums and not found_drink:
        amount = float(nums[0])
        if amount > 2000:
            await msg.answer("Забагато! Максимум 2000 мл за раз ❌")
            return
        user.add_drink("вода", amount, 1)
        await msg.answer(f"Додано {amount} мл води ✅\n{user.consumed:.0f}/{user.daily_goal} мл 💧")

@dp.callback_query(F.data.startswith("w"))
async def water(cb: types.CallbackQuery):
    user = get_user(cb.from_user.id)
    amount = int(cb.data[1:])
    user.add_drink("вода", amount, 1)
    try:
        await cb.message.edit_text(f"Додано {amount} мл води ✅\n{user.consumed:.0f}/{user.daily_goal} мл 💧", reply_markup=main_keyboard())
    except:
        await cb.message.answer(f"Додано {amount} мл води ✅\n{user.consumed:.0f}/{user.daily_goal} мл 💧", reply_markup=main_keyboard())
    await cb.answer()

@dp.callback_query(F.data == "drink")
async def choose_drink(cb: types.CallbackQuery):
    try:
        await cb.message.edit_text("Виберіть напій 🥤", reply_markup=drinks_keyboard())
    except:
        await cb.message.answer("Виберіть напій 🥤", reply_markup=drinks_keyboard())
    await cb.answer()

@dp.callback_query(F.data.startswith("drink_"))
async def drink_selected(cb: types.CallbackQuery, state: FSMContext):
    name = cb.data.split("drink_")[1]
    coef = DRINKS.get(name, 1)
    pending_drinks[cb.from_user.id] = {"name": name, "coef": coef}
    try:
        await cb.message.edit_text(f"Вибрано: {name} 🥤\n\nСкільки мл ви хочете додати? (максимум 2000 мл)")
    except:
        await cb.message.answer(f"Вибрано: {name} 🥤\n\nСкільки мл ви хочете додати? (максимум 2000 мл)")
    await state.set_state(WaterStates.waiting_for_drink_amount)
    await cb.answer()

@dp.callback_query(F.data == "stats")
async def stats(cb: types.CallbackQuery):
    user = get_user(cb.from_user.id)
    percent = (user.consumed / user.daily_goal) * 100 if user.daily_goal > 0 else 0
    fire_count = user.streak
    fire_emoji = "🔥" * fire_count if fire_count > 0 else ""
    bar = '█' * int(percent//10) + '░' * (10 - int(percent//10))
    try:
        await cb.message.edit_text(f"Статистика за сьогодні 📊\n\nВипито: {user.consumed:.0f} / {user.daily_goal} мл 💧\n{bar} {percent:.0f}%\n\nВсього випито: {user.total:.0f} мл 🏆\nСерія: {user.streak} днів {fire_emoji}", reply_markup=main_keyboard())
    except:
        await cb.message.answer(f"Статистика за сьогодні 📊\n\nВипито: {user.consumed:.0f} / {user.daily_goal} мл 💧\n{bar} {percent:.0f}%\n\nВсього випито: {user.total:.0f} мл 🏆\nСерія: {user.streak} днів {fire_emoji}", reply_markup=main_keyboard())
    await cb.answer()

@dp.callback_query(F.data == "achievements")
async def achievements(cb: types.CallbackQuery):
    user = get_user(cb.from_user.id)
    fire_count = user.streak
    fire_emoji = "🔥" * fire_count if fire_count > 0 else ""
    try:
        await cb.message.edit_text(f"Ваші досягнення 🏆\n\nПоточна серія: {user.streak} днів {fire_emoji}\n\nОтримані нагороди:\n{user.get_achievements()}\n\nЯк отримати:\n• 3 дні → Бронза 🥉\n• 7 днів → Срібло 🥈\n• 14 днів → Золото 🥇\n• 30 днів → Платіна 🏆", reply_markup=main_keyboard())
    except:
        await cb.message.answer(f"Ваші досягнення 🏆\n\nПоточна серія: {user.streak} днів {fire_emoji}\n\nОтримані нагороди:\n{user.get_achievements()}", reply_markup=main_keyboard())
    await cb.answer()

@dp.callback_query(F.data == "reminder")
async def reminder_settings(cb: types.CallbackQuery, state: FSMContext):
    user = get_user(cb.from_user.id)
    status = "Увімкнено ✅" if user.reminder_enabled else "Вимкнено ❌"
    time_str = user.reminder_time if user.reminder_time else "Не встановлено"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Встановити час ⏰", callback_data="set_reminder_time")],
        [InlineKeyboardButton(text="Вимкнути нагадування 🔕", callback_data="disable_reminder")],
        [InlineKeyboardButton(text="Назад ◀️", callback_data="back")]
    ])
    try:
        await cb.message.edit_text(f"Налаштування нагадувань ⏰\n\nСтатус: {status}\nЧас: {time_str}\n\nВиберіть дію:", reply_markup=keyboard)
    except:
        await cb.message.answer(f"Налаштування нагадувань ⏰\n\nСтатус: {status}\nЧас: {time_str}\n\nВиберіть дію:", reply_markup=keyboard)
    await cb.answer()

@dp.callback_query(F.data == "set_reminder_time")
async def set_reminder_time(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.edit_text("Введіть час у форматі ГГ:ХХ (наприклад: 14:30) ⏰\n\nЯ буду нагадувати вам пити воду щодня в цей час!")
    await state.set_state(WaterStates.waiting_for_reminder_time)
    await cb.answer()

@dp.callback_query(F.data == "disable_reminder")
async def disable_reminder(cb: types.CallbackQuery):
    user = get_user(cb.from_user.id)
    user.reminder_enabled = False
    user.reminder_time = None
    if cb.from_user.id in reminder_tasks:
        reminder_tasks[cb.from_user.id].cancel()
    await cb.message.edit_text("Нагадування вимкнено! 🔕", reply_markup=main_keyboard())
    await cb.answer()

@dp.callback_query(F.data == "help")
async def help_command(cb: types.CallbackQuery):
    try:
        await cb.message.edit_text(f"Допомога ℹ️\n\nШвидке додавання:\n• 200 - додати 200 мл води\n• чай 300 - додати 300 мл чаю\n• кава з молоком 200 - додати 200 мл кави з молоком\n\nКнопки:\n• Швидкі об'єми води (250/500/1000/2000) 💧\n• Вибір різних напоїв 🥤\n• Статистика за сьогодні 📊\n• Досягнення 🏆\n• Нагадування ⏰\n\nНорма води: 33 мл на 1 кг ваги\nОбмеження: вага від 30 до 200 кг, максимум 2000 мл за раз\n\nКоефіцієнти напоїв:\nВода: 1.0 | Чай: 0.9 | Кава: 0.5\nСік: 0.8 | Молоко: 0.7 | Лимонад/Кола: 0.3-0.4", reply_markup=main_keyboard())
    except:
        await cb.message.answer(f"Допомога ℹ️\n\n200 - вода\nчай 300 - чай\n\nНорма 33 мл на кг\nВага 30-200 кг\nМаксимум 2000 мл за раз", reply_markup=main_keyboard())
    await cb.answer()

@dp.callback_query(F.data == "back")
async def back(cb: types.CallbackQuery):
    try:
        await cb.message.edit_text("Головне меню 📋", reply_markup=main_keyboard())
    except:
        await cb.message.answer("Головне меню 📋", reply_markup=main_keyboard())
    await cb.answer()

async def main():
    print("Бот запущений! 🤖")
    print(f"Бот: @ArtemKIPT_bot ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())