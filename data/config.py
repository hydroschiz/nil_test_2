from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
ADMINS: list = env.list("ADMINS")
IP: str = env.str("ip")

