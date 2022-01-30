import logging
from typing import List
from urllib.parse import quote

from retry import retry
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from minsymaskin.translate.types import Language

logger = logging.getLogger(__name__)

OUTPUT_AREA_CSS_SELECTOR = """
#dl_translator >
 div.lmt__text >
 div.lmt__sides_container >
 section.lmt__side_container.lmt__side_container--target.df2217 >
 div.lmt__textarea_container >
 div.lmt__inner_textarea_container >
 textarea
    """


class DeepTranslator:
    def __init__(self, language_from: Language = Language.GERMAN, language_to: Language = Language.DANISH):
        if language_from in self._supported_languages:
            self.language_from = language_from
        else:
            raise ValueError(f"{language_from} is not a supported language.")
        if language_from in self._supported_languages:
            self.language_to = language_to
        else:
            raise ValueError(f"{language_from} is not a supported language.")

        # Start a Selenium driver
        # driver_path = Path(minsymaskin.__file__).parent.parent / "data" / "chromedriver"

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--lang=no")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self._init_session()

    def _init_session(self):
        if not self.driver:
            self.driver = webdriver.Chrome()  # options=self.chrome_options)

    @property
    def _supported_languages(self) -> List[str]:
        return [Language.GERMAN, Language.DANISH]

    def quit(self) -> None:
        self.driver.quit()

    def close(self) -> None:
        self.driver.close()

    def _translate(self, text: str) -> str:
        @retry(exceptions=TimeoutException, tries=10, delay=1, max_delay=5)
        def _get_translation() -> str:
            try:
                if element.get_attribute("value") != "":
                    value: str = element.get_attribute("value")
                    return value
                else:
                    raise TimeoutException("Could not find translated text.")
            except ValueError as e:
                logger.exception(e)
                raise ValueError(e)

        deepl_url = f"https://www.deepl.com/translator#{self.language_from}/{self.language_to}/{quote(text)}"
        self.driver.get(deepl_url)

        element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, OUTPUT_AREA_CSS_SELECTOR))
        )
        try:
            return _get_translation()
        except TimeoutException as e:
            msg = "Translation request timed out after "
            logger.exception(msg, e)
            raise TimeoutException(msg)

    def translate(self, text_to_translate: str) -> str:
        if not isinstance(text_to_translate, str) and len(text_to_translate) == 0:
            raise ValueError("Can only translate str with length > 0")
        if not self.driver:
            self._init_session()

        translated_text = self._translate(text=text_to_translate)

        return translated_text
