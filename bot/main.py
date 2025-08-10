import os
import logging
import json
import aiohttp
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import asyncio
from utils.pdf_generator import create_cv_pdf
from utils.proper_json import convert_to_clean_json

class CVForm(StatesGroup):
    name = State()
    experience = State()
    education = State()
    tech_stack = State()

load_dotenv()

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_KEY")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("👋 Hi! I'm your CV generation bot. Use /generate_cv to start creating your CV!")

@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply("Here are the available commands:\n"
                       "/start - Start the bot\n"
                       "/help - Show this help message\n"
                       "/generate_cv - Start CV generation process")

@dp.message(Command("generate_cv"))
async def start_cv(message: types.Message, state: FSMContext):
    await state.set_state(CVForm.name)
    await message.reply("Let's create your CV! First, what's your full name?")

@dp.message(CVForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CVForm.experience)
    await message.reply("Great! Now, please describe your work experience:")

@dp.message(CVForm.experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(CVForm.education)
    await message.reply("Perfect! What's your education background?")

@dp.message(CVForm.education)
async def process_education(message: types.Message, state: FSMContext):
    await state.update_data(education=message.text)
    await state.set_state(CVForm.tech_stack)
    await message.reply("Almost done! List your technical skills (comma-separated):")

@dp.message(CVForm.tech_stack)
async def process_tech_stack(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    tech_stack = [skill.strip() for skill in message.text.split(',')]
    
    logging.info(f"Sending request with tech_stack: {tech_stack}")
    
    async with aiohttp.ClientSession() as session:
        try:
            params = {
                'name': user_data['name'],
                'experience': user_data['experience'],
                'education': user_data['education'],
                'tech_stack': tech_stack
            }
            
            async with session.get(
                'http://cv-backend:8000/generate_cv',
                params=params
            ) as response:
                if response.status == 200:
                    cv_data = await response.text()
                    cv_data = convert_to_clean_json(cv_data)
                    
                    logging.info(f"Cleaned response: {cv_data[:200]}")
                    
                    try:
                        cv_json = json.loads(cv_data.strip())
                        required_fields = ['name', 'intro', 'experience', 'education', 
                                        'tech_stack', 'summary', 'wishes']
                        
                        if all(field in cv_json for field in required_fields):
                            pdf_filename = f"cv_{message.from_user.id}.pdf"
                            try:
                                pdf_path = await create_cv_pdf(cv_json, pdf_filename)
                                
                                await message.answer_document(
                                    types.FSInputFile(pdf_path),
                                    caption="Here's your generated CV in PDF format! 📄"
                                )
                            except Exception as e:
                                logging.error(f"PDF generation error: {str(e)}")
                                await message.reply("Sorry, there was an error creating your PDF.")
                            finally:
                                if os.path.exists(pdf_filename):
                                    os.remove(pdf_filename)
                        else:
                            missing_fields = [f for f in required_fields if f not in cv_json]
                            logging.error(f"Missing fields in JSON: {missing_fields}")
                            await message.reply("Invalid CV data format received from the server.")
                    except json.JSONDecodeError as e:
                        logging.error(f"Raw response: {cv_data}")
                        logging.error(f"JSON decode error: {str(e)}")
                        await message.reply("Error: Invalid JSON response from the server.")
                else:
                    logging.error(f"Server responded with status {response.status}")
                    await message.reply(f"Server error: {response.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Connection error: {str(e)}")
            await message.reply("Sorry, couldn't connect to the CV generation service.")
        finally:
            await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())