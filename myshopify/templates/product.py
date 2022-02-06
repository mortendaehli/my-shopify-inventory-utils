from jinja2 import Environment

from myshopify import dto

PRODUCT_TEMPLATE = """
<!DOCTYPE html>
<html>
<body>

{% if name %}
    <h1>{{ name }}</h1>
{% endif %}

<h2>{{ header }}</h2>
<p>{{ summary }}</p>

{% if features %}
    <h2>{{ features_header }}</h2>
    <ul>
    {% for feature in features %}
        <li>{{feature}}</li>
    {% endfor %}
    </ul>
{% endif %}

{% if standard_accessory %}
    <h2>{{ standard_accessory_header }}</h2>
    <ul>
    {% for accessory in standard_accessory %}
        <li>{{accessory}}</li>
    {% endfor %}
    </ul>
{% endif %}

{% if detailed_description %}
    <h2>{{ detailed_description_header }}</h2>
    <div>{{ detailed_description }}<div>
{% endif %}

{% if optional_accessory %}
    <h2>{{ optional_accessory_header }}</h2>
    <ul>
    {% for accessory in optional_accessory %}
        <li>{{accessory}}</li>
    {% endfor %}
    </ul>
{% endif %}

{% if technical_specification_dict %}
    <h2>{{ technical_specification_header }}</h2>
    <table>
    {% for key, value in technical_specification_dict.items() %}
       <tr>
            <th> {{ key }} </th>
            <td> {{ value }} </td>
       </tr>
    {% endfor %}
    </table>
{% endif %}

</body>
</html>
"""


def render_product_page(product: dto.ProductDescription) -> str:
    env = Environment().from_string(source=PRODUCT_TEMPLATE)
    result = env.render(
        name=product.name,
        header=product.header,
        summary=product.summary,
        features_header=product.features_header,
        features=product.features,
        standard_accessory_header=product.standard_accessory_header,
        standard_accessory=product.standard_accessory,
        detailed_description_header=product.detailed_description_header,
        detailed_description=product.detailed_description,
        optional_accessory_header=product.optional_accessory_header,
        optional_accessory=product.optional_accessory,
        technical_specification_header=product.technical_specification_header,
        technical_specification_dict=product.technical_specification_dict,
    )
    return result
