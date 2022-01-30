import requests

API_BASE = "https://sewingcraft.brother.eu/api"

categories = {
    "Overlock- und Coverstich Maschinen": "5F383FB3-AF53-4094-BE0B-EB94D47A493A",  # Overlock and Coverstitch machines
    "Nähmaschinen": "1114E8E2-500D-4CA2-A9E3-A241FC7180F0",  # Sewing Machines
    "ScanNCut-Maschinen": "2A5EC671-2341-4D06-81EE-10098B420D0A",  # ScanNCut
    "Kombimaschinen": "948E7E1D-6127-4153-BDEE-C05FC0A2C8F0",  # Combination sewing and embroidery machines
    "Stickmaschine": "15BF0F77-FE5D-4655-A514-660E04712BB0",  # Embroidery machines
    "Semiprofessionelle PR-VR Maschinen": "840ECC33-4859-4EBB-8E21-EF3550E3A193",  # Semi-professional Embroidery Machines
}


def search_model_by_category(category_id: str) -> dict:
    r = requests.get(f"{API_BASE}/sitecore/SuppliesSearchBox/SearchModelByCategory?CategoryId={category_id}")
    r.raise_for_status()
    return r.json()


def get_app_models():
    _all_models = {}
    for key, value in categories.items():
        _all_models[key] = {}
        model_accessories = search_model_by_category(category_id=f"{{{value}}}")
        for model in model_accessories["models"]:
            _all_models[key][model["DisplayText"]] = model["Url"]

    return _all_models


if __name__ == "__main__":
    raise DeprecationWarning("The API is probably not needed. We can delete this later.")
