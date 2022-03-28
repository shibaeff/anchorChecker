"""All bot stuff is in this file."""
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StatePickleStorage
from anchor_binding.anchor import AnchorAPI
from telebot import asyncio_filters
import configparser
import asyncio
import logging

# TODO : THIS IS A BODGE GET RID OF THIS ASAP
users = list()

logging.basicConfig(level=logging.DEBUG)

config = configparser.ConfigParser()
config.read("config.cfg")


bot = AsyncTeleBot(
    config["TELEGRAM"]["API_TOKEN"],
    parse_mode="MARKDOWN",
    state_storage=StatePickleStorage(),
)


class BotStates(StatesGroup):
    """All bot states."""

    registration = State()


@bot.message_handler(commands=["start"])
async def poll_threshhold(message):
    """Write the prompt to enter threshhold, set state to recieving the answer."""
    logging.debug(message.text)
    # TODO: gather theese two tasks
    await bot.set_state(message.from_user.id, BotStates.registration, message.chat.id)
    await bot.send_message(message.chat.id, "Input your threshold:")
    # logging.debug(await bot.get_state(message.from_user, message.chat.id))


@bot.message_handler(state=BotStates.registration)
async def register_user(message):
    """Add user to state backend."""
    # TODO: проверить что похоже на число и/или процент регэкспом
    async with bot.retrieve_data(message.from_user.id) as data:
        logging.debug(message.from_user.id)
        data["threshold"] = float(message.text)
        users.append(message.from_user.id)
    logging.debug(
        f"registered user {message.from_user.id} with threshhold {float(message.text)}"
    )


async def run_notifications():
    """Query the Anchor API and go through users to send if APY drops."""
    balance = AnchorAPI("./anchor_binding/app").get_balance()
    for user_cred in users:
        async with bot.retrieve_data(user_cred) as data:
            # logging.debug(user_cred[0], user_cred[1])
            if balance["APY"] < data["threshold"]:
                await bot.send_message(
                    user_cred, f"Alarm! APY dropped below {data['threshold']}"
                )


async def scheduler_process():
    """Routine to query notifications-wait an hour-repeat."""
    while True:
        await run_notifications()
        await asyncio.sleep(3600)


async def main():
    """Gather all needed tasks in bot loop."""
    await asyncio.gather(bot.infinity_polling(), scheduler_process())


bot.add_custom_filter(asyncio_filters.StateFilter(bot))

asyncio.run(main())
