"""AnchorBot bot entry point..."""
import logging
from bot.bot import bot, main, asyncio_filters
import asyncio

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Anchor bot app started...")
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.run(main())
