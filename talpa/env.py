from environs import Env


def ensure_env():
    env = Env()
    env.read_env()
    return env
