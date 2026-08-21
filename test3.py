import requests
import csv

url = "https://www.questnutrition.com/collections/protein-bars-all/products.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 请求接口
res = requests.get(url, headers=headers)
data = res.json()

products = data["products"]

datas = []

# 遍历每个商品
for product in products:

    handle = product["handle"]
    title = product["title"]

    # 获取所有变体 id
    ids = []

    for variant in product["variants"]:
        ids.append(str(variant["id"]))

    # 多个 id 用逗号连接
    ids = ",".join(ids)

    result = {
        "handle": handle,
        "title": title,
        "id": ids
    }

    datas.append(result)

    print(result)


# 保存 CSV
with open(
    "quest.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=["handle", "title", "id"]
    )

    writer.writeheader()
    writer.writerows(datas)

print("爬取完成！")