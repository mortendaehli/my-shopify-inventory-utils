import logging
import pathlib
from typing import Optional

from pydantic import BaseSettings, Field

logger = logging.getLogger(__name__)


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # define global variables with the Field class
    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")

    AMENDO_API_BASE: Optional[str]
    AMENDO_USERNAME: Optional[str]
    AMENDO_PASSWORD: Optional[str]
    AMENDO_API_KEY: Optional[str]

    MINSYMASKIN_SHOPIFY_KEY: str = Field(None, env="MINSYMASKIN_SHOPIFY_KEY")
    MINSYMASKIN_SHOPIFY_PWD: str = Field(None, env="MINSYMASKIN_SHOPIFY_PWD")
    MINSYMASKIN_SHOPIFY_NAME: str = Field(None, env="MINSYMASKIN_SHOPIFY_NAME")

    QUILTEFRYD_SHOPIFY_KEY: str = Field(None, env="QUILTEFRYD_SHOPIFY_KEY")
    QUILTEFRYD_SHOPIFY_PWD: str = Field(None, env="QUILTEFRYD_SHOPIFY_PWD")
    QUILTEFRYD_SHOPIFY_NAME: str = Field(None, env="QUILTEFRYD_SHOPIFY_NAME")

    FTP_HOST: str = Field(None, env="FTP_HOST")
    FTP_PORT: str = Field(None, env="FTP_PORT")
    FTP_USERNAME: str = Field(None, env="FTP_USERNAME")
    FTP_PASSWORD: str = Field(None, env="FTP_PASSWORD")

    SQL_PASSWORD: str = Field(None, env="SQL_PASSWORD")
    SQL_USERNAME: str = Field(None, env="SQL_USERNAME")
    SQL_PORT: str = Field(None, env="SQL_PORT")
    SQL_HOST: str = Field(None, env="SQL_HOST")

    class Config:
        """
        Loads the dotenv file.

        Note: if there are already env variables present, then these will take precedence.
        Ref. https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support
        """

        env_file: str = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"
        env_file_encoding = "utf-8"


class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "DEV":
            logger.info("Loading DEVELOPMENT environment variables")
            return DevConfig()

        elif self.env_state == "PROD":
            logger.info("Loading PRODUCTION environment variables")
            return ProdConfig()

        else:
            logger.info("Invalid environment state variables.")
            raise ValueError


config = FactoryConfig(GlobalConfig().ENV_STATE)()
