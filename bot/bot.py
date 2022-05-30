"""All bot stuff is in this file."""
import asyncio
import configparser
import logging
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StatePickleStorage
import gettext
from anchor_binding.anchor import AnchorAPI
import os

translation = gettext.translation('bot', 'po', fallback=True)
_, ngettext = translation.gettext, translation.ngettext

# cwd = os.getcwd()
# print(cwd)

# TODO : THIS IS A BODGE GET RID OF THIS ASAP
users = set()

logging.basicConfig(level=logging.DEBUG)

config = configparser.ConfigParser()

try:
    with open("config.cfg"):
        config.read("config.cfg")
        token = config["TELEGRAM"]["API_TOKEN"]
except Exception:
    token = os.getenv("KEY")


logging.debug(token)
bot = AsyncTeleBot(
    token,
    parse_mode="MARKDOWN",
    state_storage=StatePickleStorage(),
)

DELTA = 3600


class BotStates(StatesGroup):  # noqa: R0903,D200
    """
    All bot states.
    """

    monitoring_state = State()
    adding_apy = State()
    naming_notifier = State()


@bot.message_handler(commands=["start", "help"])
async def greet_threshhold(message: telebot.types.Message) -> None:
    """Greet a new user and specify all commands

    After starting a bot, display this help message.
    :param message: Telegram message(its content is not relevant)
    :type message: telebot.types.Message
    """
    logging.debug("in greeter")
    asyncio.gather(
        bot.set_state(
            message.from_user.id, BotStates.monitoring_state, message.chat.id
        ),
        bot.send_message(
            message.chat.id,
            _("""
Hi! Welcome to anchorChecker bot!
Right now it supports notifies for the following commands:
This bot can query APY with notifiers, as well as query different prices of associated tokens
Right now the updates it's APY once in an hour
    """),
        ),
    )


@bot.message_handler(commands=["apy"])
async def poll_threshhold(message: telebot.types.Message) -> None:
    """Write the prompt to enter threshhold, set state to recieving the answer.

    :param message: Telegram message(its content is not relevant). Then, state is set to adding_apy.
    :type message: telebot.types.Message
    """
    asyncio.gather(
        bot.set_state(message.from_user.id, BotStates.adding_apy, message.chat.id),
        bot.send_message(message.chat.id, _("Input your threshold:")),
    )


@bot.message_handler(state=BotStates.adding_apy)
async def register_user(message):
    """Add user to state backend.

    :param message: Telegram message(its content consists of the threshold parameter). Then, state is set to naming_notifier.
    :type message: telebot.types.Message
    """
    # TODO: проверить что похоже на число и/или процент регэкспом
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["threshold"] = float(message.text)
        users.add((message.from_user.id, message.chat.id))
    asyncio.gather(
        bot.set_state(message.from_user.id, BotStates.naming_notifier, message.chat.id),
        bot.send_message(message.chat.id, _("Input threshhold's name")),
    )


@bot.message_handler(state=BotStates.naming_notifier)
async def name_notifier(message: telebot.types.Message) -> None:  # noqa: D202
    """Set the name of the notifier.

    :param message: Telegram message(its content consists of the name of the notifier). Then, state is set to monitoring_state.
    :type message: telebot.types.Message
    """

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data.get("threshold"):
            data[message.text] = data["threshold"]
            del data["threshold"]
            logging.debug(
                _("added thershhold name {} with value {}").format(message.text, data[message.text])
            )
        else:
            # TODO: throw exception
            pass
    await bot.set_state(
        message.from_user.id, BotStates.monitoring_state, message.chat.id
    )


@bot.message_handler(state=BotStates.monitoring_state, commands=["list"])
async def list_notifiers(message: telebot.types.Message) -> None:
    """List all notifiers for a user.

    :param message: Telegram message(its content is not relevant). Then, state is set to monitoring_state.
    :type message: telebot.types.Message
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        # logging.debug(data)
        if data:
            for notifier in data.items():
                logging.debug(_("found notifier: {}").format(notifier))
                await bot.send_message(message.chat.id, _("found notifier: {}").format(notifier))
        else:
            await bot.send_message(message.chat.id, _("No notifiers set yet"))


@bot.message_handler(state=BotStates.monitoring_state, commands=["anc_price"])
async def anc_price(message: telebot.types.Message) -> None:
    """
    Get the current price of ANC token and report it to the user.

    :param message: Telegram message(its content is not relevant).
    :type message: telebot.types.Message
    """
    await bot.send_message(message.chat.id, _("Current ANC price is {}").format(AnchorAPI("./anchor_binding/app").get_anc_price()))


@bot.message_handler(state=BotStates.monitoring_state, commands=["luna_price"])
async def luna_price(message: telebot.types.Message) -> None:
    """
    Get the current price of LUNA token and report it to the user.

    :param message: Telegram message(its content is not relevant).
    :type message: telebot.types.Message
    """
    await bot.send_message(message.chat.id, _("Current LUNA price is {}").format(AnchorAPI("./anchor_binding/app").get_luna_price()))


@bot.message_handler(state=BotStates.monitoring_state, commands=["anc_cap"])
async def anc_cap(message: telebot.types.Message) -> None:
    """
    Get the current market cap of ANC token and report it to the user.

    :param message: Telegram message(its content is not relevant).
    :type message: telebot.types.Message
    """
    await bot.send_message(message.chat.id, _("Current ANC market cap is {}").format(AnchorAPI("./anchor_binding/app").get_anc_cap()))


@bot.message_handler(state=BotStates.monitoring_state, commands=["ust_cap"])
async def ust_cap(message: telebot.types.Message) -> None:
    """
    Get the current market cap of UST token and report it to the user.

    :param message: Telegram message(its content is not relevant).
    :type message: telebot.types.Message
    """
    await bot.send_message(message.chat.id, _("Current UST market cap is {}").format(AnchorAPI("./anchor_binding/app").get_ust_cap()))


@bot.message_handler(state=BotStates.monitoring_state, commands=["ust_price"])
async def ust_price(message: telebot.types.Message) -> None:
    """
    Get the current price of UST token and report it to the user.

    :param message: Telegram message(its content is not relevant).
    :type message: telebot.types.Message
    """
    await bot.send_message(message.chat.id, _("Current UST price is {}").format(AnchorAPI("./anchor_binding/app").get_ust_price()))


async def run_notifications() -> None:
    """Query the Anchor API and go through users to send if APY drops."""
    apy = AnchorAPI("./anchor_binding/app").get_balance()
    for user_cred in users:
        async with bot.retrieve_data(*user_cred) as data:
            for notifier, amount in data.items():
                if apy["APY"] < amount:
                    await bot.send_message(
                        user_cred[1], _("Alarm! APY dropped below {} on notifier {}").format(amount, notifier)
                    )


async def scheduler_process() -> None:
    """Routine to query notifications-wait an hour-repeat."""
    while True:
        await run_notifications()
        await asyncio.sleep(DELTA)


async def main() -> None:
    """Gather all needed tasks in bot loop."""
    await asyncio.gather(bot.infinity_polling(), scheduler_process())
