from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
							InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from gtts import gTTS

bot = Bot(token="token")
dp = Dispatcher(bot, storage=MemoryStorage())

class ruvoice(StatesGroup):
	text = State()

class envoice(StatesGroup):
	text = State()

@dp.message_handler(commands=["start", "menu"])
async def menu(message: types.Message):
	keyboard = ReplyKeyboardMarkup([[KeyboardButton("🔊 Go")]],resize_keyboard=True)
	await message.answer("🍒 Main menu", reply_markup=keyboard)

@dp.message_handler(commands=["go"])
async def go(message: types.Message):
	support_kb =InlineKeyboardMarkup()
	ru = InlineKeyboardButton('Ru', callback_data='ru')
	en = InlineKeyboardButton('En', callback_data='en')
	support_kb.add(ru, en)
	await message.answer("Choose language.", reply_markup=support_kb)

@dp.callback_query_handler(text_contains="ru")
async def login(callback_query: types.CallbackQuery):
	message = callback_query.message
	keyboard = ReplyKeyboardMarkup([[KeyboardButton("✋ Exit")]], resize_keyboard=True, one_time_keyboard=True)
	await message.answer("Введите текст.", reply_markup=keyboard)
	await ruvoice.text.set()

@dp.callback_query_handler(text_contains="en")
async def login(callback_query: types.CallbackQuery):
	message = callback_query.message
	keyboard = ReplyKeyboardMarkup([[KeyboardButton("✋ Exit")]], resize_keyboard=True, one_time_keyboard=True)
	await message.answer("Enter text.", reply_markup=keyboard)
	await envoice.text.set()

@dp.message_handler(state=ruvoice.text)
async def process_ruvoice(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		if message.text == "✋ Exit":
			await menu(message)
			await state.finish()
		else:
			txt = message.text
			tts = gTTS(text = txt, lang = "ru")
			tts.save("voice.mp3")
			voice = open(r'voice.mp3', 'rb')
			await bot.send_voice(chat_id=message.from_user.id, voice=voice)
			voice.close()
			await menu(message)
			await state.finish()

@dp.message_handler(state=envoice.text)
async def process_ruvoice(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		if message.text == "✋ Exit":
			await menu(message)
			await state.finish()
		else:
			txt = message.text
			tts = gTTS(text = txt, lang = "en")
			tts.save("voice.mp3")
			voice = open(r'voice.mp3', 'rb')
			await bot.send_voice(chat_id=message.from_user.id, voice=voice)
			voice.close()
			await menu(message)
			await state.finish()

@dp.message_handler(content_types=["text"])
async def some_text(message: types.Message):
	if message.text == "🍒 Main menu":
		await menu(message)
	elif message.text == "🔊 Go":
		await go(message)

if __name__ == "__main__":
	executor.start_polling(dp)