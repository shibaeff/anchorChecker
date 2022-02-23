from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup
from anchor_binding.anchor import AnchorAPI
import configparser
import asyncio


config = configparser.ConfigParser()
config.read('config.cfg')


bot = AsyncTeleBot(config['TELEGRAM']['API_TOKEN'], parse_mode='MARKDOWN')
users = dict()


class BotStates(StatesGroup):
    registration = State()


@bot.message_handler(commands=['start'])
async def poll_threshhold(message):
    # TODO: gather theese two tasks
    await bot.set_state(message.from_user.id, BotStates.registration, message.chat.id)
    await bot.send_message(message.chat.id, 'Input your threshold:')


@bot.message(state=BotStates.registration)
async def register_user(message):
    # WARNING: если добавлять еще стейты(вроже коннекта с кошельком, то надо добавлять через retrieve_data(типа как тут https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/asynchronous_telebot/custom_states.py))
    # TODO: проверить что похоже на число и/или процент регэкспом
    users[message.sender] = float(message.text)


async def run_notifications():
    balance = AnchorAPI().get_balance()
    for user, threshhold in users.items():
        if balance['APY'] < threshhold:
            await bot.send_message(user, f'Alarm! APY dropped below {threshhold}')


async def scheduler_process():
    while True:
        await run_notifications()
        await asyncio.sleep(3600)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler_process())

asyncio.run(main())
