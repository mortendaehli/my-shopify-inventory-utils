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


class GoogleTranslator:
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
        """Need to accept"""
        if not self.driver:
            self.driver = webdriver.Chrome()  # options=self.chrome_options)

        url = f"https://translate.google.com/?sl={self.language_from}&tl={self.language_to}&text={quote('Some dummy text')}"

        self.driver.get(url)

        @retry(exceptions=TimeoutException, tries=10, delay=1, max_delay=5)
        def _agree_terms():
            # Need to accept the Google terms
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Godta")]'))
            ).click()
            #  Alternative XPATH: f'//*[text()="Godta"]')))

        if "consent" in self.driver.current_url:
            _agree_terms()

    @property
    def _supported_languages(self) -> List[str]:
        return [Language.DANISH, Language.NORWEGIAN]

    def quit(self) -> None:
        self.driver.quit()

    def close(self) -> None:
        self.driver.close()

    def _translate(self, text: str) -> str:
        @retry(exceptions=TimeoutException, tries=10, delay=1, max_delay=5)
        def _get_translation() -> str:
            try:
                if element.text != "":
                    return element.text
                else:
                    raise TimeoutException("Could not find translated text.")
            except ValueError as e:
                logger.exception(e)
                raise ValueError(e)

        url = f"https://translate.google.com/?sl={self.language_from}&tl={self.language_to}&text={quote(text)}"
        self.driver.get(url)

        element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, f'//span[@lang="{self.language_to}"]'))
        )
        #  Alternative XPATH: f'//div[@data-language="{self.language_to}"]'  # Note: This also includes the buttons.
        try:
            translated_text = _get_translation()
            return translated_text
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
