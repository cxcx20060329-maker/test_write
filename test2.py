import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.cosrx.com/collections/all/products.json?limit=250"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 获取所有商品
res = requests.get(url, headers=headers)
products = res.json()["products"]

datas = []

for product in products:

    # 商品名称
    name = product["title"]

    # 原价
    variant = product["variants"][0]

    price = variant["compare_at_price"] or variant["price"]

    # 图片
    images = []

    for image in product["images"]:
        images.append(image["src"])

    images = ",".join(images)

    # Size
    sizes = ""

    for option in product["options"]:

        if option["name"].lower() == "size":
            sizes = ",".join(option["values"])

    # ---------------------
    # Key Ingredients
    # ---------------------

    product_url = (
        "https://www.cosrx.com/products/"
        + product["handle"]
    )

    res = requests.get(product_url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    key_ingredients = ""

    start = text.lower().find("key ingredients")
    end = text.lower().find("full ingredients", start)

    if start != -1 and end != -1:
        key_ingredients = text[
            start + len("key ingredients"):end
        ].strip()

    # 保存数据
    data = {
        "name": name,
        "price": price,
        "images": images,
        "Key Ingredients": key_ingredients,
        "Size": sizes
    }

    datas.append(data)

    print(name)


# 保存 CSV
with open(
    "cosrx.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "name",
            "price",
            "images",
            "Key Ingredients",
            "Size"
        ]
    )

    writer.writeheader()
    writer.writerows(datas)


print("爬取完成！")