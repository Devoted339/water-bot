import asyncio
import logging
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime, timedelta
from typing import Dict
import io
import os
aqw="8081316889:AAF2W-kI2SMz14YEThfC3_G7-_08lp2FWPA"
logging.basicConfig(level=logging.INFO)
qwe=logging.getLogger(__name__)
class rew(StatesGroup):
    rty=State()
    tyu=State()
    yui=State()
asd={
    "вода": 1.0, "чай": 0.9, "кава": 0.5,
    "кава з молоком": 0.6, "сік": 0.8, "молоко": 0.7,
    "лимонад": 0.4, "кола": 0.3
}
class zxc:
    def __init__(self):
        self.vbn=None
        self.mnb=2000
        self.nbv=0
        self.bvc=0
        self.cxz=[]
        self.xza={}
        self.zxcx=datetime.now().strftime('%Y-%m-%d')
        self.asdd=False
        self.qwer=0
        self.erty=[]
        self.tyui=None
        self.yuio=False
    def uiop(self):
        asdfg=datetime.now().strftime('%Y-%m-%d')
        if self.zxcx!=asdfg:
            self.cxz.append(f"{self.zxcx}: {self.nbv}")
            self.xza[self.zxcx]=self.nbv
            if self.nbv>=self.mnb:
                self.qwer+=1
                self.hjkl()
            else:
                self.qwer=0
            self.nbv=0
            self.zxcx=asdfg
    def zxcv(self,qw,et,rt):
        yt=et*rt
        self.nbv+=yt
        self.bvc+=yt
    def hjkl(self):
        tyuio={
            3:"3 дні поспіль 🥉",
            7:"7 днів поспіль 🥈",
            14:"14 днів поспіль 🥇",
            30:"30 днів поспіль 🏆"
        }
        if self.qwer in tyuio and tyuio[self.qwer] not in self.erty:
            self.erty.append(tyuio[self.qwer])
            return tyuio[self.qwer]
        return None
    def ghjk(self):
        if not self.erty:
            return "Поки немає досягнень"
        return "\n".join(self.erty)
bnm=Bot(token=aqw)
vbn=Dispatcher(storage=MemoryStorage())
nmnb={}
dfg={}
sdf={}
def cvb(bnmn):
    if bnmn not in nmnb:
        nmnb[bnmn]=zxc()
    nmnb[bnmn].uiop()
    return nmnb[bnmn]
def plk(wer):
    if wer<30:
        wer=30
    if wer>200:
        wer=200
    return int(wer*33)
def qaz(edc):
    if not edc.xza:
        return None
    rfv=[]
    tgb=[]
    yhn=datetime.now()
    for ujm in range(6,-1,-1):
        ikm=(yhn-timedelta(days=ujm)).strftime('%Y-%m-%d')
        rfv.append(ikm)
        tgb.append(edc.xza.get(ikm,0))
    plt.figure(figsize=(10,6))
    plt.bar(rfv,tgb,color='#4CAF50',alpha=0.7)
    plt.axhline(y=edc.mnb,color='red',linestyle='--',label=f'Норма ({edc.mnb} мл)')
    plt.xlabel('Дата')
    plt.ylabel('Випито води (мл)')
    plt.title('Ваша статистика споживання води')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    olp=io.BytesIO()
    plt.savefig(olp,format='png')
    olp.seek(0)
    plt.close()
    return olp
async def mko(plo):
    await asyncio.sleep(1)
    while True:
        iuy=cvb(plo)
        if iuy.yuio and iuy.tyui:
            nhy=datetime.now().strftime("%H:%M")
            if nhy==iuy.tyui:
                await bnm.send_message(plo,f"Нагадування! Час випити води! Поточна норма: {iuy.nbv:.0f}/{iuy.mnb} мл 💧")
                await asyncio.sleep(60)
        await asyncio.sleep(30)
def bgv(jkl):
    if jkl in sdf:
        sdf[jkl].cancel()
    sdf[jkl]=asyncio.create_task(mko(jkl))
def qweasd():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="250 💧",callback_data="zxc1"),
         InlineKeyboardButton(text="500 💧",callback_data="zxc2")],
        [InlineKeyboardButton(text="1000 💧",callback_data="zxc3"),
         InlineKeyboardButton(text="2000 💧",callback_data="zxc4")],
        [InlineKeyboardButton(text="Напій 🥤",callback_data="zxc5")],
        [InlineKeyboardButton(text="Статистика 📊",callback_data="zxc6"),
         InlineKeyboardButton(text="Досягнення 🏆",callback_data="zxc7")],
        [InlineKeyboardButton(text="Нагадування ⏰",callback_data="zxc8"),
         InlineKeyboardButton(text="Допомога ℹ️",callback_data="zxc9")]
    ])
def rtyuio():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вода 💧",callback_data="plm_вода"),
         InlineKeyboardButton(text="Чай 🍵",callback_data="plm_чай")],
        [InlineKeyboardButton(text="Кава ☕",callback_data="plm_кава"),
         InlineKeyboardButton(text="Кава з молоком ☕",callback_data="plm_кава з молоком")],
        [InlineKeyboardButton(text="Сік 🧃",callback_data="plm_сік"),
         InlineKeyboardButton(text="Молоко 🥛",callback_data="plm_молоко")],
        [InlineKeyboardButton(text="Лимонад 🥤",callback_data="plm_лимонад"),
         InlineKeyboardButton(text="Кола 🥤",callback_data="plm_кола")],
        [InlineKeyboardButton(text="Назад ◀️",callback_data="wsx")]
    ])
@vbn.message(Command("start"))
async def asdfgh(msg:types.Message,state:FSMContext):
    await state.clear()
    user=cvb(msg.from_user.id)
    await msg.answer("Вітаю! Я бот для відстеження водного балансу! 💧\n\nВведіть вашу вагу:")
    if not user.vbn:
        await state.set_state(rew.rty)
    else:
        await msg.answer("Головне меню 📋",reply_markup=qweasd())
@vbn.message(rew.rty)
async def qwerty(msg:types.Message,state:FSMContext):
    user=cvb(msg.from_user.id)
    try:
        w=float(msg.text)
        if w<30:
            await msg.answer("Вага не може бути менше 30 кг! Введіть реальну вагу ❌")
            return
        if w>400:
            await msg.answer("Вага не може бути більше 400 кг! Введіть реальну вагу ❌")
            return
        user.vbn=w
        user.mnb=plk(w)
        user.asdd=True
        await state.clear()
        await msg.answer(f"Вага збережена: {w} кг ✅\nДенна норма: {user.mnb} мл 💧\n\nГоловне меню 📋",reply_markup=qweasd())
    except:
        await msg.answer("Помилка! Введіть число ❌")
@vbn.message(rew.tyu)
async def yuiop(msg:types.Message,state:FSMContext):
    user=cvb(msg.from_user.id)
    drink_info=dfg.get(msg.from_user.id)
    if not drink_info:
        await state.clear()
        await msg.answer("Будь ласка, оберіть напій з меню 🥤",reply_markup=qweasd())
        return
    try:
        amount=float(msg.text)
        if amount<=0:
            await msg.answer("Кількість має бути більше 0 мл ❌")
            return
        if amount>2000:
            await msg.answer("Забагато! Максимум 2000 мл за раз ❌")
            return
        name=drink_info["name"]
        coef=drink_info["coef"]
        user.zxcv(name,amount,coef)
        water_amount=amount*coef
        await state.clear()
        if msg.from_user.id in dfg:
            del dfg[msg.from_user.id]
        await msg.answer(f"Додано: {name} ✅\n{amount} мл 🥤 → {water_amount:.0f} мл води 💧\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    except:
        await msg.answer("Помилка! Введіть число ❌")
@vbn.message(rew.yui)
async def asdfg(msg:types.Message,state:FSMContext):
    user=cvb(msg.from_user.id)
    try:
        time_str=msg.text.strip()
        if re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',time_str):
            user.tyui=time_str
            user.yuio=True
            bgv(msg.from_user.id)
            await state.clear()
            await msg.answer(f"Нагадування встановлено на {time_str} ✅\nЯ буду нагадувати вам пити воду! ⏰",reply_markup=qweasd())
        else:
            await msg.answer("Невірний формат! Введіть час у форматі ГГ:ХХ ❌")
    except:
        await msg.answer("Помилка! Введіть час у форматі ГГ:ХХ ❌")
@vbn.message()
async def zxcvb(msg:types.Message):
    user=cvb(msg.from_user.id)
    text=msg.text.lower()
    found_drink=None
    found_amount=None
    nums=re.findall(r'\d+',text)
    if nums:
        found_amount=float(nums[0])
    for drink in asd:
        if drink in text:
            found_drink=drink
            break
    if found_drink and found_amount:
        if found_amount>2000:
            await msg.answer("Забагато! Максимум 2000 мл за раз ❌")
            return
        coef=asd[found_drink]
        user.zxcv(found_drink,found_amount,coef)
        water_amount=found_amount*coef
        await msg.answer(f"Додано: {found_drink} ✅\n{found_amount} мл 🥤 → {water_amount:.0f} мл води 💧\n{user.nbv:.0f}/{user.mnb} мл 💧")
    elif nums and not found_drink:
        amount=float(nums[0])
        if amount>2000:
            await msg.answer("Забагато! Максимум 2000 мл за раз ❌")
            return
        user.zxcv("вода",amount,1)
        await msg.answer(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧")
@vbn.callback_query(F.data=="zxc1")
async def qazwsx(cb:types.CallbackQuery):
    user=cvb(cb.from_user.id)
    amount=250
    user.zxcv("вода",amount,1)
    try:
        await cb.message.edit_text(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    except:
        await cb.message.answer(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="zxc2")
async def edcvfr(cb:types.CallbackQuery):
    user=cvb(cb.from_user.id)
    amount=500
    user.zxcv("вода",amount,1)
    try:
        await cb.message.edit_text(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    except:
        await cb.message.answer(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="zxc3")
async def rfvtgb(cb:types.CallbackQuery):
    user=cvb(cb.from_user.id)
    amount=1000
    user.zxcv("вода",amount,1)
    try:
        await cb.message.edit_text(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    except:
        await cb.message.answer(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="zxc4")
async def yhnujm(cb:types.CallbackQuery):
    user=cvb(cb.from_user.id)
    amount=2000
    user.zxcv("вода",amount,1)
    try:
        await cb.message.edit_text(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    except:
        await cb.message.answer(f"Додано {amount} мл води ✅\n{user.nbv:.0f}/{user.mnb} мл 💧",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="zxc5")
async def ikolp(cb:types.CallbackQuery):
    try:
        await cb.message.edit_text("Виберіть напій 🥤",reply_markup=rtyuio())
    except:
        await cb.message.answer("Виберіть напій 🥤",reply_markup=rtyuio())
    await cb.answer()
@vbn.callback_query(F.data.startswith("plm_"))
async def qscwdv(cb:types.CallbackQuery,state:FSMContext):
    name=cb.data.split("plm_")[1]
    coef=asd.get(name,1)
    dfg[cb.from_user.id]={"name":name,"coef":coef}
    try:
        await cb.message.edit_text(f"Вибрано: {name} 🥤\n\nСкільки мл ви хочете додати? (максимум 2000 мл)")
    except:
        await cb.message.answer(f"Вибрано: {name} 🥤\n\nСкільки мл ви хочете додати? (максимум 2000 мл)")
    await state.set_state(rew.tyu)
    await cb.answer()
@vbn.callback_query(F.data=="zxc6")
async def ewrtyu(cb:types.CallbackQuery):
    user=cvb(cb.from_user.id)
    percent=(user.nbv/user.mnb)*100 if user.mnb>0 else 0
    fire_count=user.qwer
    fire_emoji="🔥"*fire_count if fire_count>0 else ""
    bar='█'*int(percent//10)+'░'*(10-int(percent//10))
    img_buf=qaz(user)
    if img_buf:
        temp_path=f"temp_{cb.from_user.id}.png"
        with open(temp_path,"wb") as f:
            f.write(img_buf.getvalue())
        photo=FSInputFile(temp_path)
        try:
            await cb.message.delete()
        except:
            pass
        await cb.message.answer_photo(photo,caption=f"Статистика за останні 7 днів 📊\n\nСьогодні: {user.nbv:.0f} / {user.mnb} мл 💧\n{bar} {percent:.0f}%\n\nВсього випито: {user.bvc:.0f} мл 🏆\nСерія: {user.qwer} днів {fire_emoji}",reply_markup=qweasd())
        os.remove(temp_path)
    else:
        try:
            await cb.message.edit_text(f"Статистика за сьогодні 📊\n\nВипито: {user.nbv:.0f} / {user.mnb} мл 💧\n{bar} {percent:.0f}%\n\nВсього випито: {user.bvc:.0f} мл 🏆\nСерія: {user.qwer} днів {fire_emoji}\n\nПоки немає даних для графіка",reply_markup=qweasd())
        except:
            await cb.message.answer(f"Статистика за сьогодні 📊\n\nВипито: {user.nbv:.0f} / {user.mnb} мл 💧\n{bar} {percent:.0f}%\n\nВсього випито: {user.bvc:.0f} мл 🏆\nСерія: {user.qwer} днів {fire_emoji}",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="zxc7")
async def bvcxza(cb:types.CallbackQuery):
    user=cvb(cb.from_user.id)
    fire_count=user.qwer
    fire_emoji="🔥"*fire_count if fire_count>0 else ""
    try:
        await cb.message.edit_text(f"Ваші досягнення 🏆\n\nПоточна серія: {user.qwer} днів {fire_emoji}\n\nОтримані нагороди:\n{user.ghjk()}\n\nЯк отримати:\n• 3 дні → Бронза 🥉\n• 7 днів → Срібло 🥈\n• 14 днів → Золото 🥇\n• 30 днів → Платіна 🏆",reply_markup=qweasd())
    except:
        await cb.message.answer(f"Ваші досягнення 🏆\n\nПоточна серія: {user.qwer} днів {fire_emoji}\n\nОтримані нагороди:\n{user.ghjk()}",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="zxc8")
async def lkmjnh(cb:types.CallbackQuery,state:FSMContext):
    user=cvb(cb.from_user.id)
    status="Увімкнено ✅" if user.yuio else "Вимкнено ❌"
    time_str=user.tyui if user.tyui else "Не встановлено"
    keyboard=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Встановити час ⏰",callback_data="zxc10")],
        [InlineKeyboardButton(text="Вимкнути нагадування 🔕",callback_data="zxc11")],
        [InlineKeyboardButton(text="Назад ◀️",callback_data="wsx")]
    ])
    try:
        await cb.message.edit_text(f"Налаштування нагадувань ⏰\n\nСтатус: {status}\nЧас: {time_str}\n\nВиберіть дію:",reply_markup=keyboard)
    except:
        await cb.message.answer(f"Налаштування нагадувань ⏰\n\nСтатус: {status}\nЧас: {time_str}\n\nВиберіть дію:",reply_markup=keyboard)
    await cb.answer()
@vbn.callback_query(F.data=="zxc10")
async def poiuyt(cb:types.CallbackQuery,state:FSMContext):
    await cb.message.edit_text("Введіть час у форматі ГГ:ХХ (наприклад: 14:30) ⏰\n\nЯ буду нагадувати вам пити воду щодня в цей час!")
    await state.set_state(rew.yui)
    await cb.answer()
@vbn.callback_query(F.data=="zxc11")
async def mnbvcx(cb:types.CallbackQuery):
    user=cvb(cb.from_user.id)
    user.yuio=False
    user.tyui=None
    if cb.from_user.id in sdf:
        sdf[cb.from_user.id].cancel()
    await cb.message.edit_text("Нагадування вимкнено! 🔕",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="zxc9")
async def lkjhgf(cb:types.CallbackQuery):
    try:
        await cb.message.edit_text(f"Допомога ℹ️\n\nШвидке додавання:\n• 200 - додати 200 мл води\n• чай 300 - додати 300 мл чаю\n• кава з молоком 200 - додати 200 мл кави з молоком\n\nКнопки:\n• Швидкі об'єми води (250/500/1000/2000) 💧\n• Вибір різних напоїв 🥤\n• Статистика за сьогодні 📊\n• Досягнення 🏆\n• Нагадування ⏰\n\nНорма води: 33 мл на 1 кг ваги\nОбмеження: вага від 30 до 200 кг, максимум 2000 мл за раз\n\nКоефіцієнти напоїв:\nВода: 1.0 | Чай: 0.9 | Кава: 0.5\nСік: 0.8 | Молоко: 0.7 | Лимонад/Кола: 0.3-0.4",reply_markup=qweasd())
    except:
        await cb.message.answer(f"Допомога ℹ️\n\n200 - вода\nчай 300 - чай\n\nНорма 33 мл на кг\nВага 30-200 кг\nМаксимум 2000 мл за раз",reply_markup=qweasd())
    await cb.answer()
@vbn.callback_query(F.data=="wsx")
async def qazxsw(cb:types.CallbackQuery):
    try:
        await cb.message.edit_text("Головне меню 📋",reply_markup=qweasd())
    except:
        await cb.message.answer("Головне меню 📋",reply_markup=qweasd())
    await cb.answer()
async def main():
    print("Бот запущений! 🤖")
    print(f"Бот: @ArtemKIPT_bot ✅")
    await vbn.start_polling(bnm)
if __name__=="__main__":
    asyncio.run(main())
