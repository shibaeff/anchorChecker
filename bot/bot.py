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



translation = gettext.translation('counter', 'pot`s', fallback=True)
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
except:
    token = os.getenv("KEY")

bot = AsyncTeleBot(
    token,
    parse_mode="MARKDOWN",
    state_storage=StatePickleStorage(),
)


class BotStates(StatesGroup):  # noqa: R0903
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
    asyncio.gather(
        bot.set_state(
            message.from_user.id, BotStates.monitoring_state, message.chat.id
        ),
        bot.send_message(
            message.chat.id,
            _("""
Hi! Welcome to anchorChecker bot!
Right now it supports notifies for the following commands:
/apy - add a new APY notifier
/reserve - 
/list - list all current notifiers
/help - show this help
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
async def name_notifier(message: telebot.types.Message) -> None:
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
        await asyncio.sleep(3600)


async def main() -> None:
    """Gather all needed tasks in bot loop."""
    await asyncio.gather(bot.infinity_polling(), scheduler_process())
