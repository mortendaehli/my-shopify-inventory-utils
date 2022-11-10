from unittest.mock import MagicMock, patch

import pytest

from myshopify.api.amendo.client import AmendoAPIClient


class TestAmendoAPIClient:

    def setup_class(self):
        self.api = AmendoAPIClient()

    @pytest.mark.integtest
    def test_auth(self):
        self.api._authentication_method._token
