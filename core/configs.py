from os import environ
from dotenv import load_dotenv

load_dotenv()


class ConfigEnvs:

    __envs = ["SECRET_KEY", "STAGE"]

    @staticmethod
    def check_env():
        for env in ConfigEnvs.__envs:
            env_value = environ.get(env)
            if env_value == "" or env_value is None:
                raise EnvironmentError("{} variable is missing!".format(env))

    @staticmethod
    def envs(env):
        return environ.get(env)