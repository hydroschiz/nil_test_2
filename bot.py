import asyncio
import logging
import sys

from handlers.users import commands, view_post, edit_post
from loader import dp, bot


async def main() -> None:
    # And the run events dispatching
    dp.include_routers(
        edit_post.router,
        commands.router,
        view_post.router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
