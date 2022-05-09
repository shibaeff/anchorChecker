Bot documentation
=================

Theese docs are impossible to generate because of bot decorators

.. py:function:: greet_threshhold(message: telebot.types.Message) -> None
    :async:

    Greet a new user and specify all commands

    After starting a bot, display this help message.

    :param message: Telegram message(its content is not relevant)
    :type message: telebot.types.Message

.. py:function:: poll_threshhold(message: telebot.types.Message) -> None
    :async:

    Write the prompt to enter threshhold, set state to recieving the answer.

    :param message: Telegram message(its content is not relevant). Then, state is set to adding_apy.
    :type message: telebot.types.Message

.. py:function:: register_user(message)
    :async:

    Add user to state backend.

    :param message: Telegram message(its content consists of the threshold parameter). Then, state is set to naming_notifier.
    :type message: telebot.types.Message

.. py:function:: name_notifier(message: telebot.types.Message) -> None
    :async:

    Set the name of the notifier.

    :param message: Telegram message(its content consists of the name of the notifier). Then, state is set to monitoring_state.
    :type message: telebot.types.Message

.. py:function:: list_notifiers(message: telebot.types.Message) -> None
    :async:

    List all notifiers for a user.

    :param message: Telegram message(its content is not relevant). Then, state is set to monitoring_state.
    :type message: telebot.types.Message

.. py:function:: run_notifications() -> None
    :async:

    Query the Anchor API and go through users to send if APY drops.

.. py:function:: scheduler_process() -> None
    :async:

    Routine to query notifications-wait an hour-repeat.

.. py:function:: main() -> None
    :async:

    Gather all needed tasks in bot loop.