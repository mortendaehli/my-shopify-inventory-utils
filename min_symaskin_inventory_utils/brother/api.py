# import pandas as pd
import requests

API_BASE = "https://sewingcraft.brother.eu/api"


def search_model_by_category(category_id: str) -> dict:
    requests.get(f"{API_BASE}/sitecore/SuppliesSearchBox/SearchModelByCategory?CategoryId={category_id}")


if __name__ == "__main__":
    r = search_model_by_category(category_id="{948E7E1D-6127-4153-BDEE-C05FC0A2C8F0}")
    pass
