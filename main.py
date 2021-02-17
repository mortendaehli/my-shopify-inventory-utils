import os

import pandas as pd
import shopify
from dotenv import load_dotenv


def get_all_resources(resource_type, **kwargs):
    resource_count = resource_type.count(**kwargs)
    resources = []
    if resource_count > 0:
        page = resource_type.find(**kwargs)
        resources.extend(page)
        while page.has_next_page():
            page = page.next_page()
            resources.extend(page)
    return resources


def main():
    # env_path = Path('.env')
    # load_dotenv(dotenv_path=env_path)
    load_dotenv()
    key = os.getenv('SHOPIFY_KEY')
    pwd = os.getenv('SHOPIFY_PWD')
    name = os.getenv('SHOPIFY_NAME')

    shop_url = f"https://{key}:{pwd}@{name}.myshopify.com/admin"
    shopify.ShopifyResource.set_site(value=shop_url)

    df_inventory = pd.read_excel(os.path.join('.', 'data', 'inventory.xlsx'), engine='openpyxl')

    df_inventory.rename(columns={
        'Varenummer': 'sku',
        'varetekst': 'title',
        'Disponibelt': 'inventory_quantity',
        'Webgr 1 navn': 'product_type',
        'synlig på nett': 'active',
        'Utpris inkl mva': 'price'
    }, inplace=True)

    df_inventory = df_inventory.loc[:, ['sku', 'title', 'inventory_quantity', 'product_type', 'active', 'price']]
    df_inventory = df_inventory.loc[df_inventory['product_type'].map(lambda x: x in ['Symaskiner', 'Symaskintilbehør']), :]
    df_inventory = df_inventory.loc[df_inventory['active'].map(lambda x: x is True)]

    df_inventory.loc[:, 'sku'] = df_inventory.loc[:, 'sku'].map(lambda x: str(x))
    df_inventory.loc[:, 'title'] = df_inventory.loc[:, 'title'].astype(str)
    df_inventory.loc[:, 'inventory_quantity'] = df_inventory.loc[:, 'inventory_quantity'].astype(str)
    df_inventory.loc[:, 'product_type'] = df_inventory.loc[:, 'product_type'].astype(str)
    df_inventory.loc[:, 'active'] = df_inventory.loc[:, 'active'].astype(str)
    df_inventory.loc[:, 'vendor'] = None
    df_inventory.loc[:, 'price'] = \
        df_inventory['price'].map(lambda x: x.__repr__().replace(',', '.').replace(r'\xa0', '').replace("'", '')).astype(float)

    df_inventory.loc[df_inventory.loc[:, 'title'].map(lambda x: 'janome' in str(x).replace(' ', '').lower()), 'vendor'] = 'Janome'
    df_inventory.loc[df_inventory.loc[:, 'title'].map(lambda x: 'babylock' in str(x).replace(' ', '').lower()), 'vendor'] = 'Baby Lock'

    shop = shopify.Shop.current

    products = get_all_resources(shopify.Product)

    skus = []
    # Updating existing products
    for product in products:
        variant = product.variants[0]
        sku = variant.sku
        skus.append(sku)
        if sku in df_inventory['sku'].values:
            df_product = df_inventory.loc[df_inventory['sku'] == sku].iloc[0]
            print(f"Updating: {product.title} - sku: {sku}")
            product.title = df_product['title']
            product.vendor = df_product['vendor']
            product.product_type = df_product['product_type']
            product.inventory_quantity = df_product['inventory_quantity']
            variant.price = df_product['price']
            variant.option1 = "Default Title"
            variant.save()
            product.save()
        else:
            print(f"Deleting - Not matched with POS: {product.title} - sku: {sku}")
            shopify.Variant.delete(variant.id)
            shopify.Product.delete(product.id)

    for _, df_product in df_inventory.iterrows():
        if df_product.sku not in skus:
            print(f"Importing from POS: {df_product.title} - sku: {df_product.sku}")
            new_product = shopify.Product()

            # Creating the product.
            new_product.title = df_product['title']
            new_product.vendor = df_product['vendor']
            new_product.product_type = df_product['product_type']
            new_product.inventory_quantity = df_product['inventory_quantity']
            new_product.save()

            # Then creating the (only) variant and saving....
            new_variant = shopify.Variant(
                {
                    "position": 1,
                    "sku": df_product['sku'],
                    "price": df_product['price'],
                    # "product_id": new_product.id,
                    "requires_shipping": True,
                    "inventory_quantity": df_product['inventory_quantity'],
                    "inventory_policy": "deny",
                    "inventory_management": "shopify",
                    "fulfillment_service": "manual"
                }
            )

            new_product.variants = [new_variant]
            new_product.save()

            # result = new_variant.save()
    print('Complete')


if __name__ == '__main__':
    main()
