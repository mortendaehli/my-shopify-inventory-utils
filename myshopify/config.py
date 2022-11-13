import logging
import pathlib
from typing import Optional

from pydantic import BaseSettings

logger = logging.getLogger(__name__)


class GlobalConfig(BaseSettings):
    """Global configurations."""

    AMENDO_USERNAME: Optional[str]
    AMENDO_PASSWORD: Optional[str]
    AMENDO_API_KEY: Optional[str]

    MINSYMASKIN_SHOPIFY_KEY: Optional[str]
    MINSYMASKIN_SHOPIFY_PWD: Optional[str]
    MINSYMASKIN_SHOPIFY_NAME: Optional[str]

    QUILTEFRYD_SHOPIFY_KEY: Optional[str]
    QUILTEFRYD_SHOPIFY_PWD: Optional[str]
    QUILTEFRYD_SHOPIFY_NAME: Optional[str]

    FTP_HOST: Optional[str]
    FTP_PORT: Optional[str]
    FTP_USERNAME: Optional[str]
    FTP_PASSWORD: Optional[str]

    SQL_PASSWORD: Optional[str]
    SQL_USERNAME: Optional[str]
    SQL_PORT: Optional[str]
    SQL_HOST: Optional[str]

    class Config:
        """
        Loads the dotenv file.

        Note: if there are already env variables present, then these will take precedence.
        Ref. https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support
        """

        env_file: str = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"
        env_file_encoding = "utf-8"


config = GlobalConfig()
